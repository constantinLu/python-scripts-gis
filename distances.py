import arcpy
lista=[1,93,352,524,800,848,913,938,1006,1099,1357,1368,1788,2218,2337,2381,2653,2923,2973,3023,3073,3508,3586,3875,4175,4287,4442,4454,4710,4870,4950,4990,5310,5520,5570,5655,5985,6200,6210,6460,6530,6830,7160,7410,7690,7860,8070,8080]

feat_in=arcpy.GetParameterAsText(0)
def pr(x):
    arcpy.AddMessage(x)
    
with arcpy.da.SearchCursor(feat_in,["OID@","SHAPE@LENGTH","SHAPE@"]) as cursor:
    for row in cursor:
        for i in lista:
            if i<row[1]:
                coord_X=row[2].positionAlongLine(i,False).centroid.X
                coord_Y=row[2].positionAlongLine(i,False).centroid.Y
                pr("{}. distance:{},{},{}".format(row[0],i,coord_X,coord_Y))
            else:
                pr("Distance too big: {}".format(i))
