import arcpy  
  
# point layers loaded in your dataframe  
pnts1 = arcpy.mapping.Layer("line1_pnts")  
pnts2 = arcpy.mapping.Layer("line2_pnts")  
  
# create search cursor to iterate through first layer  
scur = arcpy.SearchCursor(pnts1)  
row = scur.next()  
  
closestPnt = 0  
closestPntID = 0  
cenPnts = []  
ctr=0  
  
while row:     
   shp = row.shape  
   geom = shp.getPart()  
   print "Geom1 - " + str(row.FID) + ": " + str(geom.X) + ":" + str(geom.Y)  
   mindist = 9999  
   tmpdist = 9999  
    # search cursor for feature in second line point layer  
   scur2 = arcpy.SearchCursor(pnts2)  
   row2 = scur2.next()  
   geom2X = 0  
   geom2Y = 0  
   while row2:  
      shp2 = row2.shape  
      geom2 = shp2.getPart()  
      # check distance between points first and second layer and find closest point  
      tmpdist = shp.distanceTo(shp2)  
      if tmpdist < mindist:  
         mindist = tmpdist  
         closestPnt = shp2  
         closesPntID = row2.FID  
         geom2X = geom2.X  
         geom2Y = geom2.Y  
      row2 = scur2.next()  
   del scur2  
   print "Geom2 - " + str(closesPntID) + ": " + str(closestPnt.getPart().X) + ":" + str(closestPnt.getPart().Y)     
   print "Dist: " + str(mindist)  
   if shp != closestPnt:  
      # calculate geometric centre of two points closest to each other  
      cenX = (geom.X + geom2X) / 2  
      cenY = (geom.Y + geom2Y) / 2  
      midpnt = arcpy.Point(cenX, cenY)  
      # create mid line point  
      ptGeometry = arcpy.PointGeometry(point)  
      print "Mid1 >> " + str(cenX) + ":" + str(cenY)             
      # add point to array  
      cenPnts.append(midpnt)    
   row = scur.next()  
   ctr += 1  
del scur  
  
# write list of points to new point feature class ("cenlinepnts" - create point feature class and load into dataframe) for centre line  
inscur = arcpy.InsertCursor("cenlinepnts")  
insrow = inscur.newRow()  
for p in cenPnts:  
   insrow.shape = p  
   inscur.insertRow(insrow)  
del inscur  