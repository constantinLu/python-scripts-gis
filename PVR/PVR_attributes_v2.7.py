import datetime, arcpy,os
   
# Input variables    
pointFeat=arcpy.GetParameterAsText(0)
table=arcpy.GetParameterAsText(1)
spoorFeat=arcpy.GetParameterAsText(2)
spoorField=arcpy.GetParameter(3)
geocodeFeat=arcpy.GetParameterAsText(4)
scratchWorkspace=arcpy.GetParameterAsText(5)

geoSpJoin=os.path.join(scratchWorkspace,"subgeoSpJoin")

# Needed functions
def checkDuplicates(i,lista,listaDupl):
    if lista.count(i)>1:
        if i not in listaDupl:
            listaDupl.append(i)
        else:
            pass
log=[] # list of items to print in the log file
def pr(x):
    arcpy.AddMessage(x)
    log.append(x)
    
# Environment Settings
arcpy.env.overwriteOutput = True

##### Determine the GEOCODE and GEOSUBCODE
pr("\nProcess 1: Determine the right Geocode and Geosubcode\n")
pr("FYI: The script does not add the Geocode or Geosubgeocode if the point is situated on more than one polygons\n")
# Determine if there there are more than one geocode/geosubcode per object
arcpy.SpatialJoin_analysis(pointFeat, geocodeFeat, geoSpJoin, "JOIN_ONE_TO_MANY", "KEEP_ALL")

# Determine if there there are more than one geocode/geosubcode per object
issueGeocode=[]
issueGeosubcode=[]
d_countSubgeo={}

cursor=arcpy.da.SearchCursor(geoSpJoin,["TARGET_FID","GEOSUBCODE_1", "GEOCODE_1","Bron"])
for row in cursor:
    if row[3]=="to process":
        if row[0] not in d_countSubgeo :
            d_countSubgeo[row[0]]=[1, row[1], row[2]]
        else:
            d_countSubgeo[row[0]][0]=d_countSubgeo[row[0]][0]+1
            if row[2] not in d_countSubgeo[row[0]][2:]:
                d_countSubgeo[row[0]].append(row[2])           
del cursor, row

for obj in d_countSubgeo:
    if d_countSubgeo[obj][0]>1:
        issueGeosubcode.append(obj)
        if len(d_countSubgeo[obj][2:])>1:
            issueGeocode.append(obj)
cursor=arcpy.da.UpdateCursor(pointFeat,["OID@", "Geosubcode", "Geocode","Bron"])
for row in cursor:
    if row[3]=="to process":
        if row[0] not in issueGeosubcode and row[0] not in issueGeocode:
            row[1]=d_countSubgeo[row[0]][1]
            row[2]=d_countSubgeo[row[0]][2]

        elif row[0] not in issueGeosubcode and  row[0] in issueGeocode:
            row[1]=d_countSubgeo[row[0]][1]
        elif row[0] in issueGeosubcode and  row[0] not in issueGeocode:
            row[2]=d_countSubgeo[row[0]][2]
        else:
            pass
        cursor.updateRow(row)
del row, cursor

# Process 2: Update the fields fields "UniekNummer" and "Foto"
pr("Process 2: Update the fields fields 'UniekNummer', 'Foto' and 'Tijd'\n")
null_geocodes=[]
d_listaUnique={} #dictionary of all "UniekNummer" field values for each geocode
d_listaFoto={} #dictionary of all "Foto" field values in pointFeat for each geocode
d_duplUnique={}#dictionary of the Unique numbers duplicates for each geocode
d_duplFoto={} #dictionary of the Foto duplicates in pointFeat for each geocode 
d_available={} #dictionary with all the unused Unique numbers for each geocode

listaGeo=[] #list of all the geocodes present in the dataset

cursorGeo=arcpy.da.SearchCursor(pointFeat,["Geocode","OID@"])
for row in cursorGeo:
    if row[0] is None or row[0]=="":
        if row[0] not in null_geocodes:
            null_geocodes.append(row[1])
    else:
        if row[0] not in listaGeo:
            listaGeo.append(row[0])
del row, cursorGeo

listaGeo=map(str,listaGeo)
for geocode in listaGeo:        #setting the values for each geocode in the dictionaries to be a list
    d_listaUnique[geocode]=[] 
    d_listaFoto[geocode]=[]
    d_duplUnique[geocode]=[]
    d_duplFoto[geocode]=[]
    d_available[geocode]=[]

cursor=arcpy.da.SearchCursor(pointFeat,["OID@","UniekNummer","Foto","Bron","Geocode"]) # Make lists with all the used values in the "UniekNummer" and "Foto" fields
for row in cursor:
    if row[3]<>"to process":
        for geocode in listaGeo:
            if geocode==row[4]:
                if row[1] is not None:                
                    d_listaUnique[geocode].append(row[1])
                if row[2] is not None:
                    d_listaFoto[geocode].append(row[2])
                checkDuplicates(row[1],d_listaUnique[geocode],d_duplUnique[geocode])
                checkDuplicates(row[2],d_listaFoto[geocode],d_duplFoto[geocode])
del row, cursor

for geocode in listaGeo: #Populate the lists of available uniek numbers for each geocode. If all the uniek numbers per geocode are NULL, then the corresponding available list is empty
    if len(d_listaUnique[geocode])>0:        
        for i in range(1,max(d_listaUnique[geocode])+1):
            if i not in d_listaUnique[geocode]:
                d_available[geocode].append(i)          

# Open an Updatecursor for the input feature to update the "UniekNummer", "tijd" and "Foto" fields
cursor1=arcpy.da.UpdateCursor(pointFeat,["OID@","UniekNummer","Geocode","DatumTijd","Foto","Bron","Tijd"])
for row in cursor1:
    if row[5]=="to process" and row[2] is not None and row[2]<>"":     
        # Add the unique number
        if len(d_listaUnique[row[2]])==0: #if per each geocode there are no assigned unieq numbers (therefore neither there are elements in the available list)=>assign "1"
            row[1]=1
            d_listaUnique[row[2]].append(1)
        else:
            
            if len(d_available[row[2]])==0:
                row[1]=max(d_listaUnique[row[2]])+1
            else:
                row[1]=d_available[row[2]][0] 
                del d_available[row[2]][0]
        d_listaUnique[row[2]].append(row[1])
            
        pr("{}. Unique number {} for Geocode {} was created".format(row[0],row[1],row[2]))       

        # Update the "Foto" field with a valid name
        if row[2] is not None:
            fotoName=str(row[2])+"-"+str(row[3].year)+"-"+str(row[3].isocalendar()[1])+"-"+str(row[1]).rjust(4,'0')
            row[4]=fotoName
            d_listaFoto[row[2]].append(fotoName)
            checkDuplicates(fotoName,d_listaFoto[row[2]],d_duplFoto[row[2]])                                  
        else:
            pass
        pr("{}: Fotoname {} was created".format(row[0], fotoName))
        
        # Update the "Tijd" field with the proper date
        row[6]=row[3]        
        pr("{}: 'Tijd' field updated".format(row[0]))
        cursor1.updateRow(row)
del row, cursor1

pr("\nProcess 3: Update the fields 'km','L_R','X','Y', 'Spoor' and 'Bron'")
# Process 3: Update the fields 'km','L_R','X','Y','Spoor' and 'Bron'
routeEventTable=os.path.join(scratchWorkspace,"RouteEvents")
projectedRouteEvents_name="ProjectedRouteEvents"
projectedRouteEvents=os.path.join(scratchWorkspace,projectedRouteEvents_name)
Output_Event_Table_Properties="RID POINT MEAS"

# Locate Features Along Routes
arcpy.LocateFeaturesAlongRoutes_lr(pointFeat, spoorFeat, spoorField, "4 Meters", routeEventTable, Output_Event_Table_Properties, "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
pr("\nFeatures along routes were located")

# Make Route Event Layer
arcpy.MakeRouteEventLayer_lr(spoorFeat, spoorField, routeEventTable, "rid POINT meas", "TempRouteEvents", "", "NO_ERROR_FIELD", "", "NORMAL", "", "LEFT", "POINT")
pr("Route event layer created")

# Export Event Layer
arcpy.FeatureClassToFeatureClass_conversion("TempRouteEvents", scratchWorkspace,projectedRouteEvents_name)
pr("Event layer exported to the featureclass '{}'".format(projectedRouteEvents_name))

# Add XY Coordinates to the projected route event table
arcpy.AddXY_management(projectedRouteEvents)
pr("XY coordinates were added to the '{}' featureclass".format(projectedRouteEvents_name))

# Execute AddField for the L/R position in the table
arcpy.AddField_management(projectedRouteEvents, "L_R_1", "TEXT")
# Set local variables for the Field Calculation
expression="leftRight(!Distance!)"
codeblock = """def leftRight(dist):
    if dist < 0:
        return "R"
    elif dist > 0:
        return "L"
    else:
        return "error" """

# Execute CalculateField 
arcpy.CalculateField_management(projectedRouteEvents, "L_R_1", expression, "PYTHON_9.3",codeblock)
pr("Field 'L_R_1' was added to the '{}' featureclass and then calculated\n".format(projectedRouteEvents_name))

# Process 3.1: Add the spoor number
# Store the needed info from the projected route events table
cursor1=arcpy.da.SearchCursor(projectedRouteEvents,["UniekNummer","MEAS","L_R_1","POINT_X","POINT_Y","RID","Geocode"])
dict_event={}
for row in cursor1:
    dict_event[str(row[6])+"_"+str(row[0])]=[row[0],row[1],row[2],row[3],row[4],row[5]]
    
daily=time.strftime("%Y/%m/%d ") # Create string of the current date to use it in the "Processed" field  
# Open an Updatecursor for the input feature to update the projected on the track points, L/R Km fields
lista_processed=[] #list for all the values in the "Bron" field that contain "Processed on"+daily
cursor2=arcpy.da.SearchCursor(pointFeat,["OID@","Bron"])
for row in cursor2:
    if daily in str(row[1]) and row[1] not in lista_processed:
        lista_processed.append(row[1])
outside_radius=[] # list of objects outside of the 4m radius
cursor=arcpy.da.UpdateCursor(pointFeat,["UniekNummer","km","L_R","X","Y","Spoor","OID@","Bron", "Geocode"])
for row in cursor:
    if row[7]=="to process":
        if row[0] is not None:
            combo=str(row[8])+"_"+str(row[0])
            if combo in dict_event:
                row[0]=dict_event[combo][0]
                row[1]=dict_event[combo][1]
                row[2]=dict_event[combo][2]
                row[3]=dict_event[combo][3]
                row[4]=dict_event[combo][4]
                row[5]=dict_event[combo][5]
            else:
                row[1]=None
                row[2]=None
                row[3]=None
                row[4]=None
                row[5]=None
                outside_radius.append(row[6])
                pr("{}. Object outside of the 4m radius".format(row[6]))                
            # Generate the right format for "Bron" field (ex: "Processed on 2017/04/05 (1)")                         
            row[7]="Processed on "+daily+"("+str(len(lista_processed))+")"
            cursor.updateRow(row)            
            pr("{}: The fields 'km','L_R','X','Y','Spoor' were updated".format(row[6]))
            pr("{}. Object processed. 'Bron' field updated".format(row[6]))
    
pr("\n!!! List of the Unique numbers DUPLICATES from the entire dataset: {}".format(d_duplUnique))
pr("\n!!! List of the Foto DUPLICATES from the entire dataset: {}".format(map(str,d_duplFoto)))
pr("\n!!! List of objects from this processing batch outside of the 4m: {}".format(outside_radius))

# Process 4: Modify the photonames in the attachment table
pr("\nProcess 3: Modify the photonames in the attachment table\n")
d_pointFeat={}
globalid_pointfeat=[]
cursor=arcpy.SearchCursor(pointFeat)
for row in cursor:
    if row.getValue("Geocode") is not None and row.getValue("Geocode")<>"":
        d_pointFeat[row.getValue("GlobalID")]=[row.getValue("Foto"),row.getValue("OBJECTID"),row.getValue("Bron")]
        globalid_pointfeat.append(row.getValue("GlobalID"))
del row,cursor

table_foto_dupl=[]
table_differences=[]
global_mismatch=[]

cursor=arcpy.da.SearchCursor(table,["OID@","REL_GLOBALID","ATT_NAME"])
lista_globalids=[row[1] for row in cursor] #list of all global ids in the attached table
globalids_dupl=[i for i in lista_globalids if lista_globalids.count(i)>1] #list of the DUPLICATE global ids in the attached table
globalid_not_in_table=[d_pointFeat[i][1] for i in globalid_pointfeat if i not in lista_globalids]
point_feat_dupl=[] #List OIDS from the point feature that have more than one picture
modified_fotonames=[] #List of TABLE attachment ids that have been modified
null_fotonames=[] #List of TABLE attachment ids that haven't been modified because the photoname that belongs to them is NULL
        
oids_global_dupl=[]  
with arcpy.da.UpdateCursor(table,["OID@","REL_GLOBALID","ATT_NAME"]) as cursor:
    for row in cursor:
        if row[1] not in d_pointFeat:
            global_mismatch.append(row[0]) #check if there are records in the attached table that belong to no points.
        else:
            if d_pointFeat[row[1]][2]=="Geleverd": # "Geleverd" = "delivered"; they won't be part of the "change photoname" process
                pr("{}. Object already delivered".format(row[0]))
            else:
                if row[1] in globalids_dupl:
                    oids_global_dupl.append(row[0])
                    if d_pointFeat[row[1]][1] not in point_feat_dupl:                   
                        point_feat_dupl.append(d_pointFeat[row[1]][1])
                    else:
                        pass
                elif row[2][:-4]<>d_pointFeat[row[1]][0]:
                    pr(str(row[0])+". "+str(row[2][:-4])+" <> "+str(d_pointFeat[row[1]][0]))
                    table_differences.append(row[0])
                    pr("{}. corresponding photoname: {}".format(row[0],d_pointFeat[row[1]][0]))
                    if len(str(d_pointFeat[row[1]][0]))>2:
                        row[2]=row[2].replace(row[2][:-4],d_pointFeat[row[1]][0])
                        pr("{}. Fotoname modified".format(row[0]))
                        modified_fotonames.append(row[0])
                        cursor.updateRow(row)
                    else:
                        null_fotonames.append(row[0])
                        pr("{}. Fotoname not modified because of NULL or '' value of the point fotoname".format(row[0]))             
                else:
                    pr(str(row[0])+". "+str(row[2][:-4])+"="+str(d_pointFeat[row[1]][0]))
                         
pr("\n!!! List of TABLE attachment ids with different foto names then their correspondings in the point featureclass : {}".format(table_differences))
pr("\n!!! List of TABLE attachment ids that have been modified : {}".format(modified_fotonames))
pr("\n!!! List of TABLE attachment ids that haven't been modified because the photoname that belongs to them is NULL or '' : {}".format(null_fotonames))
pr("\n!!! List OIDs from attached table that have duplicates of global ids: {}".format(oids_global_dupl))
pr("\n!!! List OIDs from the point feature that have attached more than one picture: {}".format(point_feat_dupl))
pr("\n!!! List of records from the attached table that either belong to no object from the point feature class, either the corresponding geocode is NULL or ='' : {}".format(global_mismatch))
pr("\n!!! List of objects that don't have the Geocode value filled: {}\n".format(null_geocodes))
pr("\n!!! List of objects that have more are situated on overlapping geocodes: {}".format(issueGeocode))
pr("\n!!! List of objects that have more are situated on overlapping geoSUBcodes: {}\n".format(issueGeosubcode))

#Write messages to a Text File
output_folder = os.path.join(os.path.dirname(str(scratchWorkspace)), 'logfiles')
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
txtFile = open(output_folder+"\\"+ time.strftime('%Y%m%d%H%M') + ".log","w")
txtFile.write ('\n'.join(log))
txtFile.close()

