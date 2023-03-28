import os
import shutil
import cv2
from PIL import Image
import platform
import re
import json


def rotate_pic(path1='/media/ztc/Data/work/calibrate/MD/111/R/'):

    imglist=os.listdir(path1)
    for bmp in imglist:
        img = Image.open(os.path.join(path1,bmp))
        # img = img.transpose(Image.ROTATE_90)  # 将图片旋转90度
        img = img.transpose(Image.ROTATE_180)  # 将图片旋转180度
        # img = img.transpose(Image.ROTATE_270)  # 将图片旋转270度
        # img.show("img/rotateImg.png")
        img.save(os.path.join(path1,bmp))

def show_parallax(root_path="/home/ztc/code/",origin_pic="1673576587399_2.bmp"):

    # origin_pic_list=os.listdir(root_path)
    # for origin_pic in origin_pic_list:
    path1=os.path.join(root_path, origin_pic)
    pic=cv2.imread(path1,cv2.IMREAD_GRAYSCALE)
    picr=cv2.applyColorMap(pic*8, cv2.COLORMAP_JET)
    
    origin_pic1 = origin_pic.split('.')[0]
    origin_pic2 = origin_pic.split('.')[1]
    parallax_plot = f'{origin_pic1}_color.{origin_pic2}'
    cv2.imwrite(os.path.join(root_path, parallax_plot),picr)

    cv2.imshow("2",pic)
    cv2.imshow("hello",picr)
    cv2.waitKey(0)

def move_except07_18(path=''):

    LA_path = os.path.join(path, 'LA')
    LB_path = os.path.join(path, 'LB')
    UA_path = os.path.join(path, 'UA')
    UB_path = os.path.join(path, 'UB')
    hour_in_use = range(7,19)

    for loca_path in [LA_path, LB_path, UA_path, UB_path]:
        if os.path.exists(loca_path) == True:
            filelist = os.listdir(loca_path)
            for video in filelist:
                hour = video.split('_')[1]
                if hour == '06' or hour == '19':
                    os.makedirs(f"{loca_path}_1",exist_ok=True)
                    shutil.move(os.path.join(loca_path, video), f"{loca_path}_1")

def md5_axis(path1='/media/ztc/Data/work/calibrate/MD/'):

    listvsm = os.listdir(path1)
    for vsm in listvsm:
        vsmfile = os.path.join(path1, vsm)
        if 'axis.yml' in os.listdir(vsmfile):
            os.system(f'md5sum {vsmfile}/axis.yml')

class IP2MAC:
    """
    Python3根据IP地址获取MAC地址（不能获取本机IP，可以获取与本机同局域网设备IP的MAC）
    """
    def __init__(self):
        self.patt_mac = re.compile('([a-f0-9]{2}[-:]){5}[a-f0-9]{2}', re.I)

    def getMac(self, ip):
        sysstr = platform.system()

        if sysstr == 'Windows':
            macaddr = self.__forWin(ip)
        elif sysstr == 'Linux':
            macaddr = self.__forLinux(ip)
        else:
            macaddr = None

        macaddr = macaddr.replace(":","")


        return macaddr or '00-00-00-00-00-00'

    def __forWin(self, ip):
        os.popen('ping -n 1 -w 500 {} > nul'.format(ip))
        macaddr = os.popen('arp -a {}'.format(ip))
        macaddr = self.patt_mac.search(macaddr.read())

        if macaddr:
            macaddr = macaddr.group()
        else:
            macaddr = None

        return macaddr

    def __forLinux(self, ip):
        os.popen('ping -nq -c 1 -W 500 {} > /dev/null'.format(ip))

        result = os.popen('arp -an {}'.format(ip))

        result = self.patt_mac.search(result.read())

        return result.group() if result else None

def read_json(filepath='', file=''):
    filejson = os.path.join(filepath, file)
    with open(filejson, mode='r', encoding='utf8') as js:
        json_data = json.load(js)
    return json_data



if __name__ == '__main__':

    # move_except07_18(path='/media/ztc/TOSHIBAEXT#11/')
    # md5_axis()
    # g = IP2MAC()
    # print(g.getMac('192.168.1.244'))
    show_parallax(root_path='/media/ztc/Data/md_code/calibrator/vsm_player_client_calib/192.168.1.150_6236991a6c90/snap/D/',origin_pic="1679976874631_2.bmp")
    # show_parallax(root_path='/media/ztc/Data/work/initialize/MD/lab6/batch9_vsm150/config/vsm_1/',origin_pic='1664369720681_2.bmp')
