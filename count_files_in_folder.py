import os
import os.path

main_path="P:/01_Projects/W_Netherland/022 GIS/1004533 Diepladermeting overwegen/work/delivery_20.12.2016/Endproducts"

s=0
for folder in os.listdir(main_path):
    if folder[:3]=="OVW":
        s+=1
        path_folder=os.path.join(main_path,folder)
        list_files=[]
        
        for item in os.listdir(path_folder):
            if str(item) !="Thumbs.db":
                list_files.append(item)
                path_item=os.path.join(path_folder,item)                    
        print(str(s)+". "+folder+": "+str(len(list_files))+": "+str(list_files))
           
        
        
