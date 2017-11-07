import os
import shutil

#in "in_path" should be all the input files, in folders or not
in_path=r"C:\Arcadis\LunguC\test_input"

outpath=r"C:\Arcadis\LunguC\test_output"

#"lista" is a list with all records from the progress sheet
lista =["10126","10793","11560","12341","12351","12353","12354","12355","12356","12853","13100","13106","13281","14347","14435","14436","14437","14443","14448","14451","14454","14455","14782","15221","15236","15298","15651","15652","17014","17015","17016","17019","17908","17909","63598","72312","72313","72314","72315","72316","72317","72318","72319","72320","72321","72322","72323","72540","00207","00748","00749","00874","01788","02769","03437","03609","03907","04160","04192","04939","04940","04960","04961","04963","05550","05553","06373","06727","06728","07454","07794","08796","08835","08852","08954","10410","12346","14347","14440","14441","14442","14452","15650","15653","17017","17018","17459","17997"]
def createdirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

for dirpath,dirnames,filenames in os.walk(in_path):
    for filename in filenames:
        file_path=os.path.join(dirpath,filename)
        for i in lista:            
            if i in filename:
                inter_path=os.path.join(outpath,i)
                createdirectory(inter_path)
                shutil.copy2(file_path,inter_path)
                print(str(filename)+" copied")

for folder in os.listdir(outpath):
    folder_path=os.path.join(outpath,folder)
    check_path=os.listdir(folder_path)
    if  os.path.isdir(folder_path) and len(check_path)==0:
        os.rmdir(folder_path)
        print("Folder "+str(folder)+" was empty, so it has been removed")















        










        

print ("\n Done. Your smile would work better :).")
 
