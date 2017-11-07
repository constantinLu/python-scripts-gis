infeature=''
infield=''

lista=[row[0] for row in arcpy.da.SearchCursor(infeature,[infield])]

def duplicate(field):
    occ=lista.count(field)
    if field in lista:
        return occ

        
        
    
