import cv2
import os

def show_parallax(root_path="/home/ztc/code/", origin_pic='background_2.bmp'):

    # origin_pic=os.listdir(root_path)[0]

    path1=os.path.join(root_path, origin_pic)
    pic=cv2.imread(path1,cv2.IMREAD_GRAYSCALE)
    picr=cv2.applyColorMap(pic*8, cv2.COLORMAP_JET)
    cv2.imshow("2",pic)
    cv2.imshow("hello",picr)
    cv2.waitKey(0)


if __name__ == '__main__':

    root_path=input("请输入图片所在路径(避免中文路径):")
    origin_pic=input("请输入图片名称(避免中文名称):")
    show_parallax(root_path=root_path,origin_pic=origin_pic)