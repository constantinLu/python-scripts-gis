#Scriptul cauta toate fisierele (de orice tip) dintr-un director, inclusiv din subdirectoarele sale
#Iti afiseaza intr-un .txt file numele fisierului, extensia si directorul

import os

mypath=r"C:\Arcadis\LunguC\Projects\DUBAI\Data\To process" #Insereaza intre ghilimele path-ul tau pentru folderul pe care vrei sa-l inspectezi
txtpath=r"C:\Arcadis\QATAR.txt" #Insereaza intre ghilimele path-ul pentru fisierul .txt pentru output (ti-l creeaza automat)

#Daca rulezi scriptul de mai multe ori, in fisierul .txt iti va adauga la vechile rezultate, pe cele noi
#Deci, ca sa nu ai duplicate, ori stergi vechiul output din .txt, ori creezi fisier nou (schimbi denumirea .txt-ului in txtpath)

f=open(txtpath,'w')
s=1
for dirpath, dirname, filenames in os.walk(mypath):
    for filename in filenames:
        if os.path.splitext(filename)[1] in (".xlsx",".xls", ".XLS",".XLSX"):
            path_filename=os.path.join(dirpath,filename)
            ext=os.path.splitext(filename)[1]
            f.write(str(s)+". "+str(filename)+"@"+str(ext)+","+path_filename+"\n")
            print(str(s)+". "+str(filename)+"@"+str(ext)+"@"+path_filename)
            s=s+1
f.close()
print ("Done. Check your .txt file.")

    
