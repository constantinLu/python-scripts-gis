import arcpy,operator

infeat=r"C:\Arcadis\Lungu\Projects\Flooding maps\20170810\Wessem.shp"
outfeat=r"C:\Arcadis\Lungu\Projects\Flooding maps\output_test\output_test.shp"

#add  field of Z values in the output feature
arcpy.AddField_management(outfeat, "Z_value", "FLOAT")
print ("field 'Z_values' added in the output file")

cursor1=arcpy.da.SearchCursor(infeat,["SHAPE@","Z_value"])
list_Z=[]
for row in cursor1:
    list_Z.append(row[1])
list_Z=sorted(list_Z)

cursor2=arcpy.da.InsertCursor(outfeat,["SHAPE@","Z_value"])

cursor=arcpy.da.SearchCursor(infeat,["SHAPE@","Z_value"])

for row in cursor:
    if list_Z.index(row[1])==0:
        cursor2.insertRow((row[0],row[1]))   
    else:
        polygon=row[0]
        cursor3=arcpy.da.SearchCursor(outfeat,["SHAPE@","Z_value","OID@"])
        listaoid=[]
        for row1 in cursor3:
            listaoid.append(row1[2])
        cursor4=arcpy.da.SearchCursor(outfeat,["SHAPE@","Z_value","OID@"])
        for row2 in cursor4:
            if row2[2]==max(listaoid):
                cursor2.insertRow((row2[0],row2[1]))
                row2[0].union(polygon)

    
    
    
    
