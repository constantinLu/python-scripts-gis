import arcpy

infeat=r"C:\Arcadis\Lungu\Projects\Flooding\Projects\Flooding maps\20170810 (1)\Wessem.shp"
outfeat=r"C:\Arcadis\Lungu\Projects\Flooding maps\output.gdb\output"

#add  field of Z values in the output feature
arcpy.AddField_management(outfeat, "Z_value", "FLOAT")
print ("field 'Z_values' added in the output file")

cursor=arcpy.da.SearchCursor(infeat,["SHAPE@","Z_value"])
list_Z=[]
for row in cursor:
    list_Z.append(row[1])
list_Z=sorted(list_Z)

cursor1=arcpy.da.InsertCursor(outfeat,["SHAPE@","Z_value"])
cursor2=arcpy.da.SearchCursor(infeat,["SHAPE@","Z_value"])

for row in cursor2:
    if list_Z.index(row[1])==0:        
        cursor1.insertRow((row[0],row[1]))
        print("First feature added")
    else:
        cursor3=arcpy.da.SearchCursor(outfeat,["SHAPE@","Z_value","OID@"])
        listaoid=[]
        for row3 in cursor3:
            listaoid.append(row3[2])
        cursor4=arcpy.da.SearchCursor(outfeat,["SHAPE@","Z_value","OID@"])
        for row4 in cursor4:
            if row4[2]==max(listaoid):
                print row4[2]
                polygon=row4[0].union(row[0])
                print polygon
                cursor1.insertRow((polygon,row[1]))
                print ("Feature created")
                #arcpy.CopyFeatures_management(polygon,outfeat)
                #row4[2]=row[1]
                #cursor4.updateRow(row)
                #print ("Feature added")
                
