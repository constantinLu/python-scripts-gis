import os
import os.path
import arcpy
from arcpy import env
import time

arcpy.env.workspace = 'Database Connections/RAIL op NLAR1APP08.sde/Rail.DBO.OVW'
inFeatures='Rail.DBO.Overwegen'
#change the path below
backups_path="C:/Arcadis/Lungu_catatalin/Joost"

daily=time.strftime("%Y%m%d")

gdb_daily="backup_"+daily+".gdb"
gdb_daily_partial="backup_"+daily
gdb_daily_path=os. path.join(backups_path,gdb_daily)
out_daily_path=os. path.join(gdb_daily_path,inFeatures)

arcpy.CreateFileGDB_management(backups_path, gdb_daily)
print (str(gdb_daily)+" was created")

arcpy.Copy_management(inFeatures, out_daily_path,"FeatureClass")
print("backup features were created")
    
    
    
