import json
import os
import shutil

path1="/home/ztc/文档/wechat/WeChat Files/wxid_v3i0uu0k22aa22/FileStorage/File/2022-11/label_area/"
path2="/home/ztc/文档/wechat/WeChat Files/wxid_v3i0uu0k22aa22/FileStorage/File/2022-11/label_area2/"

TheLastArea='0'
sqlist=[]
count=0

for path in [path1,path2]:
    lists=os.listdir(path)
    for list in lists:
        with open(os.path.join(path,list)) as f:
            data = json.load(f)
            for dat in data:
                if dat['area']=="101":
                    count=0
                    pass
                else:
                    count=count+1
                    if count==5:
                        sqlist.append(dat['sq'])
sqlist.sort()

pic_path1='/media/ztc/Data/temp/pkl/1/rgb/'
pic_path2='/media/ztc/Data/temp/pkl/2/rgb/'
picsqlist=[]
for pic_path in [pic_path1,pic_path2]:
    pic1=os.listdir(pic_path)

    for pic in pic1:
        picsq=pic.split(".")[0]
        if picsq in sqlist:
            picpath=os.path.join(pic_path,pic)
            # shutil.copy(picpath,'/media/ztc/Data/temp/pkl/pic/')
            picsqlist.append(picsq)

for path in [path1,path2]:
    lists=os.listdir(path)
    lists.sort()
    for list in lists:
        with open(os.path.join(path,list)) as f:
            data = json.load(f)
            for dat in data:                                                                                                         
                if dat['sq'] in picsqlist:       
                    print(dat['area'])

# path_ini='/media/ztc/Data/temp/pkl/result/2022-11-18/'
# list_inis=os.listdir(path_ini)
# list_inis.sort()
# for list_ini in list_inis:
#     with open(os.path.join(path_ini,list_ini)) as fs:
#         data_ini = json.load(fs)
#         for dat_ini in data_ini:
#             if str(dat_ini['sq']) in picsqlist:       
#                 print(dat_ini['area'])
   
