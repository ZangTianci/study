import os

path = '/media/ztc/Data/work/calibrate/MD/192.168.1.111_ea7c361a2418/'
calibpath = os.path.join(path, 'calib')
lpicpath = os.path.join(calibpath, 'L')
rpicpath = os.path.join(calibpath, 'R')
spicpath = os.path.join(calibpath, 'S')
lspicpath = os.path.join(spicpath, 'L')
rspicpath = os.path.join(spicpath, 'R')
picpaths = [lpicpath, rpicpath, lspicpath, rspicpath]
for picpath in picpaths:
    piclist = os.listdir(picpath)
    for pic in piclist:
        picre = pic.split('-')
        picre1 = picre[0]+picre[1]+picre[2]+picre[3]+"_"+picre[4]
        os.rename(os.path.join(picpath, pic), os.path.join(picpath, picre1))