import arcpy

infeat=r"C:\Arcadis\Lungu\Projects\Flooding maps\20170810 (1)\Wessem.shp"
infeat2=r"C:\Arcadis\Lungu\Projects\Flooding maps\20170810 (2)\Wessem2.shp"
outfeat=r"C:\Arcadis\Lungu\Projects\Flooding maps\output_test\output_test.shp"

#add  field of Z values in the output feature
arcpy.AddField_management(outfeat, "Z_value", "FLOAT")
print ("field 'Z_values' added in the output file")

arcpy.Sort_management(infeat, infeat2, [["Z_value", "ASCENDING"]] )

cursor=arcpy.da.SearchCursor(infeat2,["SHAPE@","Z_value"])
list_Z=[]
for row in cursor:
    list_Z.append(row[1])
list_Z=sorted(list_Z)
print list_Z

cursor1=arcpy.da.InsertCursor(outfeat,["SHAPE@","Z_value"])
cursor2=arcpy.da.SearchCursor(infeat2,["SHAPE@","Z_value","OID@"])

   
for row in cursor2:
    print ("{} - FID".format(row[2]))
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


arcpy.AddField_management(outfeat, "Area", "DOUBLE")
arcpy.CalculateField_management(outfeat,"Area","!shape.area@squaremeters!","PYTHON_9.3","#")
