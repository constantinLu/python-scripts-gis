import os
import arcpy

in_path=r"P:\01_Projects\W_Netherland\022 GIS\1004533 Diepladermeting overwegen\work\Delivery 20.12.2016\Intermediate products"
in_object="Polyline"
cad_layer='spoor1' # Change the layers on line25!!
gdb_path="C:/Arcadis/CROSSINGS_2/pts_files_work/TEST_dgn"
gdb_name="lungu.gdb"
out_merge="output_merge"


arcpy.CreateFileGDB_management("C:/Arcadis/CROSSINGS_2/pts_files_work/TEST_dgn", gdb_name)
print(gdb_name+" created")

#Creating the feature layers for the specified CAD objects from specific CAD layers
list_layers=[]
s=0
for dirpath, dirnames, filenames in os.walk(in_path):
    for filename in filenames:
        if filename.endswith((".DGN",".dgn",".DWG",".dwg")):
            s+=1
            filename_path=os.path.join(dirpath,filename)
            object_path=os.path.join(filename_path,in_object)
            feature_layer="Layer"+str(s)
            #ex below: "D:\\lungu\\cadastru.DWG\\Polyline", "cadastru", "\"Layer\" = 'CORP_PROPR'"
            arcpy.MakeFeatureLayer_management(object_path, feature_layer, "\"Layer\" = 'spoor1'")
            list_layers.append(feature_layer)
print("feature layers created")
           
to_merge=str(' " '+'; '.join(list_layers)+' " ')

arcpy.Merge_management(to_merge, os.path.join(gdb_path,gdb_name,out_merge))
print("merged file created. Done.")                                             
                                              
