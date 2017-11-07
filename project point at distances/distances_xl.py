import arcpy,os

feat_in=arcpy.GetParameterAsText(0) # Input of line feature
location=arcpy.GetParameterAsText(1) # Location of the point feature
point_feat=arcpy.GetParameterAsText(2) # Name of the point feature
xl_dist=arcpy.GetParameterAsText(3) # Input excel file
field_dist=arcpy.GetParameter(4) # Name of the field 

lista=[]
xlcursor=arcpy.da.SearchCursor(xl_dist,[str(field_dist)])
for row in xlcursor:
    lista.append(row[0])
                        
arcpy.env.overwriteOutput = True

def pr(x):
    arcpy.AddMessage(x)

arcpy.CreateFeatureclass_management(location, point_feat, "Point",spatial_reference=feat_in)
point_feat_location=os.path.join(location,point_feat+".shp")
arcpy.AddField_management(point_feat_location,"Distance","DOUBLE")
arcpy.AddField_management(point_feat_location,"Orig_FID","SHORT")
cursor_insert=arcpy.da.InsertCursor(point_feat_location,["Distance","Orig_FID","SHAPE@X","SHAPE@Y"])
s=0
with arcpy.da.SearchCursor(feat_in,["OID@","SHAPE@LENGTH","SHAPE@"]) as cursor:
    for row in cursor:
        for i in lista:
            if i<row[1]:
                s+=1
                coord_X=row[2].positionAlongLine(i,False).centroid.X
                coord_Y=row[2].positionAlongLine(i,False).centroid.Y
                cursor_insert.insertRow((i,row[0],coord_X,coord_Y))                                
                pr("{}. D={}. point created: X={},Y={}".format(s,i,coord_X,coord_Y))
            else:
                pr("Distance too big: {}".format(i))
