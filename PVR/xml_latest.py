import arcpy, os, datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom as minidom

jpegPath=arcpy.GetParameterAsText(0)
pointFeat=arcpy.GetParameterAsText(1)

def pr(x):
    arcpy.AddMessage(x)
    
dictGIS={}
cursor=arcpy.da.SearchCursor(pointFeat,["Foto","Sein","Object", "Geosubcode","km","L_R","Spoor","Boog","Bocht","X","Y","Opmerking","DatumTijd"])
for row in cursor:    
    if row[0] not in dictGIS:
        dataa=str(row[12].year)+"-"+str(row[12].month).rjust(2,"0")+"-"+str(row[12].day).rjust(2,"0")
        dictGIS[row[0]]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],dataa]
del row, cursor
pr(dictGIS)
et.write(open(r"C:\Users\iistrate-ciobanu\Desktop\lala.xml", 'w'), encoding='utf-8')
for item in os.listdir(jpegPath):
    filename=os.path.splitext(item)[0]
    if filename in dictGIS:
        filenamePath=os.path.join(jpegPath,item)        
        
        root = ET.Element("obstakels")
        doc = ET.SubElement(root, "obstakel")
        et= ET.ElementTree(root)

        ET.SubElement(doc, "naam").text = filename
        ET.SubElement(doc, "detail").text = "Sein "+dictGIS[filename][0]
        ET.SubElement(doc, "categorie").text = dictGIS[filename][1]
        ET.SubElement(doc, "geosubcode").text = dictGIS[filename][2]
        ET.SubElement(doc, "kmvan").text = str(int(round(dictGIS[filename][3]*1000,0)))
        if dictGIS[filename][4]=="L":
            ET.SubElement(doc, "islinksvanspoor").text = "true"
        else:            
            ET.SubElement(doc, "islinksvanspoor").text = "false"
        ET.SubElement(doc, "spoor").text = dictGIS[filename][5]
        if dictGIS[filename][6]==">5000":
            ET.SubElement(doc, "isrechtstand").text = "true"
            ET.SubElement(doc, "boogstraal").text = "9000"
        else:
            ET.SubElement(doc, "isrechtstand").text = "false"
            ET.SubElement(doc, "boogstraal").text =dictGIS[filename][6]
        if dictGIS[filename][7]=="binnen":
            ET.SubElement(doc, "isbinnenzijdeboog").text ="true"
        else:
            ET.SubElement(doc, "isbinnenzijdeboog").text ="false"    
        ET.SubElement(doc, "x").text = str(int(round(dictGIS[filename][8]*1000,0)))
        ET.SubElement(doc, "y").text = str(int(round(dictGIS[filename][9]*1000,0)))
        ET.SubElement(doc, "z").text = "0"
        ET.SubElement(doc, "argument").text = "0"
        ET.SubElement(doc, "mal").text = "ProRail"
        if dictGIS[filename][10] ==None:            
            ET.SubElement(doc, "opmerking").text = "No opmerking"
        else:    
            ET.SubElement(doc, "opmerking").text = dictGIS[filename][10]
        ET.SubElement(doc, "datumopname").text = dataa
        ET.SubElement(doc, "refpuntlinksx").text = "405"
        ET.SubElement(doc, "refpuntlinksy").text = "1391"
        ET.SubElement(doc, "refpuntrechtsx").text = "810"
        ET.SubElement(doc, "refpuntrechtsy").text = "1391"      

        with open(filenamePath, "rb") as f:
            data = f.read()
            pictureCode=data.encode("base64")
        ET.SubElement(doc, "pixels").text = pictureCode
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(str(filename)+".xml", "w") as f:
            f.write(xmlstr+"\n")
        


'''        et.write(f, encoding='utf-8', xml_declaration=True) 
        print(f.getvalue())  # your XML file, encoded as UTF-8
'''
