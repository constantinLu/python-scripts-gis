import shutil
import os
'place below the path of the crossings folders'
'important! do not forget to replace the \ from the copy-pasted path with /' 
path_ovw="C:/Arcadis/LunguC/Instruire/PYTHON/teste/foldere"

'place below the path of the screenshots'
'important! do not forget to replace the \ from the copy-pasted path with /'
path_screensh="C:/Arcadis/LunguC/Instruire/PYTHON/teste/capturi"

s=0
for folder in os.listdir(path_ovw):
        for pic_jpg in os.listdir(path_screensh):
                n=len(pic_jpg)-4
                pic=pic_jpg[0:n]
                pic_list=[]
                pic_list.append(pic)
                if pic==folder:
                        s+=1
                        path_new1=os.path.join(path_screensh,pic_jpg)
                        shutil.copy2(os.path.join(path_screensh,pic_jpg),os.path.join(path_ovw,folder))
                        print(str(s)+". Copied "+pic_jpg+" to "+path_ovw+"/"+folder)
                        print(path_new1)      

        
