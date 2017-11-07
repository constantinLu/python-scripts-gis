import os.path
import os
import shutil

#Change the path below
path_ovws="C:/Arcadis/CROSSINGS_2/finals 01.11.2016"

def createdirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return;
s=0 #s=sequence of ovw in main folder
for folder in os.listdir(path_ovws):
    if str(folder)=="Thumbs.db":
        os.remove(folder)
    path_ovw=os.path.join(path_ovws,folder)
    endprod=os.path.join(path_ovw,'Endproducts')
    int_prod=os.path.join(path_ovw,'Intermediate products')
    createdirectory(endprod)
    createdirectory(int_prod)    
    endings=[".pdf",".xls",".txt","-i.pdf","-i.xls","-i.txt"]#possible endings for endproducts
    pos_endprod=[]#possible endproducts
    s+=1

    for i in endings:
        pos_endprod.append(str(folder)+i)
    ss=0 #ss=sequence of file in each ovw folder
    list_end=[] #list of endproducts
    list_int=[] #list on intermediate products  
    for fisier in os.listdir(path_ovw):
        ss+=1        
        if fisier=='Endproducts' or fisier=='Intermediate products' or fisier=='Thumbs.db':
            pass
        elif fisier in pos_endprod:            
            shutil.move(os.path.join(path_ovw,fisier),endprod)
            list_end.append(fisier)
            print(str(s)+"-"+str(ss)+". "+folder+": "+fisier+" moved")
        else:
            shutil.move(os.path.join(path_ovw,fisier),int_prod)
            list_int.append(fisier)
            print(str(s)+"-"+str(ss)+". "+folder+": "+fisier+" moved")
    print("     "+str(len(list_end))+" Endproducts moved")
    print("     "+str(len(list_int))+" Intermediate products moved")
    if len(list_end)<>3:
        print ("            !!!check the endproducts!!!")
print("Done.") 
