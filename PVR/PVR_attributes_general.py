import datetime, arcpy,os
   
# Input variables

pointFeat=arcpy.GetParameterAsText(0)
spoorFeat=arcpy.GetParameterAsText(1)
spoorField=arcpy.GetParameter(2)
scratchWorkspace=arcpy.GetParameterAsText(3)

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
listaUnique=[] #list of all "UniekNummer" field values
duplUnique=[]#list of the Unique numbers duplicates

cursor=arcpy.da.SearchCursor(pointFeat,["OID@","UniekNummer"]) # Make lists with all the used values in the "UniekNummer" and "Foto" fields
for row in cursor:
    listaUnique.append(row[1])
    checkDuplicates(row[1],listaUnique,duplUnique)

pr("\nProcess: Update the fields 'km','L_R','X','Y', 'Spoor' and 'Bron'")
# Process 2: Update the fields 'km','L_R','X','Y','Spoor' and 'Bron'
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

# Process 2.1: Add the spoor number
# Store the needed info from the projected route events table
cursor1=arcpy.da.SearchCursor(projectedRouteEvents,["UniekNummer","MEAS","L_R_1","POINT_X","POINT_Y","RID"])
dict_event={}
for row in cursor1:
    dict_event[row[0]]=[row[1],row[2],row[3],row[4],row[5]]
    
daily=time.strftime("%Y/%m/%d ") # Create string of the current date to use it in the "Processed" field  
# Open an Updatecursor for the input feature to update the projected on the track points, L/R Km fields

outside_radius=[] # list of objects outside of the 4m radius
objects_updated=[]
cursor=arcpy.da.UpdateCursor(pointFeat,["UniekNummer","km","L_R","X","Y","Spoor","OID@","Bron"])
for row in cursor:
    if row[0] is not None and row[0] not in duplUnique:
        objects_updated.append(row[6])
        if row[0] in dict_event:
            pr("{}. Object in dict_event".format(row[6]))
            row[1]=dict_event[row[0]][0]
            row[2]=dict_event[row[0]][1]
            row[3]=dict_event[row[0]][2]
            row[4]=dict_event[row[0]][3]
            row[5]=dict_event[row[0]][4]
        else:
            ("{}. Object NOT in dict_event".format(row[6]))
            row[1]=None
            row[2]=None
            row[3]=None
            row[4]=None
            row[5]=None
            outside_radius.append(row[6])        
            pr("{}. Object outside of the 4m radius".format(row[6]))
        cursor.updateRow(row)
    # Generate the right format for "Bron" field (ex: "Processed on 2017/04/05 (1)")                         
    #row[7]="Processed on "+daily+"("+str(len(lista_processed))+")"
    #cursor.updateRow(row)            
    pr("{}: The fields 'km','L_R','X','Y','Spoor' were updated".format(row[6]))
    #pr("{}. Object processed. 'Bron' field updated".format(row[6]))

pr("\n!!! List of the Unique numbers DUPLICATES from the entire dataset: {}".format(duplUnique))    
pr("\n!!! List of objects from this processing batch outside of the 4m: {}".format(outside_radius))
pr("\n!!! List of objects that have been updated:\n {}".format(objects_updated))
#Write messages to a Text File
output_folder = os.path.join(os.path.dirname(str(scratchWorkspace)), 'logfiles')
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
txtFile = open(output_folder+"\\"+"general_"+ time.strftime('%Y%m%d%H%M') + ".log","w")
txtFile.write ('\n'.join(log))
txtFile.close()


