infeature='Objecten_P_merged_1'
infield='uniqueid'

lista=[]
cursor=arcpy.da.SearchCursor(infeature,[infield])
for row in cursor:
    if row[0] not in lista:
        lista.append(row[0])

def seq(field):
    return (lista.index(field)+1)

