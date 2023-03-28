'''
Author       : JiaYu.Wu
Email        : a472796892@gmail.com
Company      : Magic Depth
Date         : 2022-01-26 15:24:14
LastEditTime : 2022-10-10 18:32:55
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /test/test_rectify2.py
'''
import os
import cv2
import argparse 
from rectify import *


if __name__ == "__main__":

    config_path=input("请输入配置路径(避免中文路径):")
    cv2.namedWindow('rst',0)

    rectify_instance_generate = Rectify(config_path)
    
    imgL = cv2.imread(os.path.join(config_path,"rgb.bmp"))
    img_generateL, img_generateR = rectify_instance_generate.remap_pic(imgL,imgL)
    rst = cv2.hconcat([img_generateL,img_generateR])
    for i in range(0,rst.shape[0],rst.shape[0]//20):
        cv2.line(rst,[0,i],[rst.shape[1],i],(255,0,0),1)
    while True:
        cv2.imshow('rst',img_generateL)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break