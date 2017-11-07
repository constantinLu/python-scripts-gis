import datetime, arcpy,os
   
# Input variables    
pointFeat=arcpy.GetParameterAsText(0)
geocodeFeat=arcpy.GetParameterAsText(1)
scratchWorkspace=arcpy.GetParameterAsText(2)

geoSpJoin=os.path.join(scratchWorkspace,"geoSpJoin")
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
arcpy.SpatialJoin_analysis(pointFeat, geocodeFeat, geoSpJoin, "JOIN_ONE_TO_MANY", "KEEP_ALL")

# Determine if there there are more than one geocode/geosubcode per object
issueGeocode=[]
issueGeosubcode=[]
d_countSubgeo={}

cursor=arcpy.da.SearchCursor(geoSpJoin,["TARGET_FID","GEOSUBCODE_1", "GEOCODE_1"])
for row in cursor:
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
cursor=arcpy.da.UpdateCursor(pointFeat,["OID@", "Geosubcode", "Geocode"])
for row in cursor:
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
 
pr("\n!!! List of objects that have more are situated on overlapping geocodes: {}\n".format(issueGeocode))
pr("\n!!! List of objects that have more are situated on overlapping geoSUBcodes: {}\n".format(issueGeosubcode))

#Write messages to a Text File
output_folder = os.path.join(os.path.dirname(str(scratchWorkspace)), 'logfiles')
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
txtFile = open(output_folder+"\\"+ time.strftime('%Y%m%d%H%M') + ".log","w")

#txtFile.write ('\n'.join(log))
txtFile.close()

