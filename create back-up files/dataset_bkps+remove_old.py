import os, arcpy, datetime, shutil
startTime = datetime.datetime.now()

#Input variables
arcpy.env.workspace = r'Database Connections/RAIL op NLAR1APP08.sde'
inFeatures='PVR'
backups_path=r"C:\Arcadis\Test"

cur_date=datetime.datetime.now().strftime("%Y%m%d") #current date
#Determine the current situation in the back-up folder
list_unique_date=[]
list_date_all=[]
for bkp in os.listdir(backups_path):
    data=str(bkp)[7:15]
    list_date_all.append(data)
    if data not in list_unique_date:
        list_unique_date.append(data)

# Create the back-up for the current date
s=list_date_all.count(cur_date)
gdb_daily="backup_"+cur_date+"_"+str(s+1)+".gdb"
gdb_daily_path=os. path.join(backups_path,gdb_daily)
out_daily_path=os. path.join(gdb_daily_path,inFeatures)
out_path=os. path.join(gdb_daily_path,inFeatures)
arcpy.CreateFileGDB_management(backups_path, gdb_daily)
print(str(gdb_daily)+" was created")
arcpy.Copy_management(inFeatures, out_path,"FeatureDataset")
print("Back-up features were created") 

# Remove the back-ups older than the last 5 days in which the script was ran
if cur_date not in list_unique_date:
    list_unique_date.append(cur_date)
list_unique_date.sort(reverse=True)
if len(list_unique_date)>4:
    for bkp in os.listdir(backups_path):
        if str(bkp)[7:15]<>cur_date and str(bkp)[7:15] not in list_unique_date[:5]:        
            shutil.rmtree(os.path.join(backups_path,bkp))
print ("Old back-ups were deleted")
print("Elapsed time: {}".format(datetime.datetime.now()-startTime))

