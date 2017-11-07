import os
import arcpy

#inputs
in_path=r"P:\01_Projects\W_Netherland\022 GIS\1004533 Diepladermeting overwegen\work\Delivery 20.12.2016\Intermediate products"
out_path = "C:\\Arcadis\\CROSSINGS_2\\pts_files_work\\TEST_dgn"
gdb_name="lungu.gdb"
gdb_path=os.path.join(out_path,gdb_name)

#create new geodatabase
arcpy.CreateFileGDB_management(out_path, gdb_name)
print(str(gdb_name)+" created")



#create features for each .dgn file for a specific layer
#the search is made only in the folders from the main directory
list_features=[]
s=1
for folder in os.listdir(in_path):
    if folder.startswith("OVW"):
        folder_path=os.path.join(in_path,folder)
        for obj in os.listdir(folder_path):
            
            if obj.endswith((".dgn",".DGN")):        
                path_poly=os.path.join(folder_path,obj,"Polyline")
                name_feature="feature"+str(s)
                s+=1                
                arcpy.FeatureClassToFeatureClass_conversion(path_poly, gdb_path, name_feature, "\"Layer\" = 'spoor1'")
                print(str(name_feature)+" created")
                feature_path=os.path.join(gdb_path,name_feature)
                list_features.append(feature_path)

#all the features in a string
features_all='"'+str('; '.join(list_features))+'"'

#merge the features
test_merge = "C:\\Arcadis\\CROSSINGS_2\\pts_files_work\\TEST_dgn\\lungu.gdb\\test_merge"
arcpy.Merge_management(features_all,test_merge)
print("Done")
                


