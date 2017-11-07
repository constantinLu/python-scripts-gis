import os
import arcpy
import time

arcpy.env.workspace = 'Database Connections/RAIL op NLAR1APP08.sde/Rail.DBO.OVW'
inFeatures='Rail.DBO.Overwegen'
#change the path below
backups_path="C:/Arcadis/Lungu_catalin/Joost"

daily=time.strftime("%Y%m%d")

gdb_daily="backup_"+daily+"_1"+".gdb"
gdb_daily_partial="backup_"+daily
gdb_daily_path=os. path.join(backups_path,gdb_daily)
out_daily_path=os. path.join(gdb_daily_path,inFeatures)

def create_bkp(inFeatures,out_path):
    out_path=os. path.join(gdb_daily_path,inFeatures)
    arcpy.CreateFileGDB_management(backups_path, gdb_daily)
    print (str(gdb_daily)+" was created")
    arcpy.Copy_management(inFeatures, out_path,"FeatureClass")
    print("backup features were created")
    
lista=[]    
for obj in os.listdir(backups_path):
    if gdb_daily_partial in obj:
        lista.append(obj)

if len(lista)==0:        
        create_bkp(inFeatures,out_daily_path)        
else:
    gdb_daily="backup_"+daily+"_"+str(len(lista)+1)+".gdb"
    gdb_daily_path=os. path.join(backups_path,gdb_daily)
    create_bkp(inFeatures,out_daily_path)
    
print arcpy.GetMessages(4)   
    
