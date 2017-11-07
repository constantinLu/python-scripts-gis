import os
import arcpy

in_path=r"C:\Arcadis\CROSSINGS_2\test2\testeee.gdb"
out_merge="Merged.shp"

list_layers=arcpy.ValueTable()
s=0
for dirpath, dirname, filenames in arcpy.da.Walk(in_path, datatype="FeatureClass", type="Polyline"):
    for filename in filenames:
        s+=1
        filename_path=os.path.join(dirpath,filename)
        
        feature_layer="Layer"+str(s)
        arcpy.MakeFeatureLayer_management(filename_path,feature_layer, "GEOCODE IN ( '042', '054', '090', '475', '478', '518', '519', '522', '552', '553', '614', '618')")
        list_layers.addRow(feature_layer)
print(list_layers)
arcpy.Merge_management(list_layers,os.path.join(in_path,out_merge))

print(out_merge+" created")
        
