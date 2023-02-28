'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-05-31 12:14:30
LastEditTime : 2022-12-17 10:55:38
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /vsm_player_client_calib/rectify.py
'''
import cv2
import numpy as np
import os
import argparse
from numba import jit

class Rectiy:
    def __init__(self, path, x_focal, y_focal, x_shift, y_shift, disparity_shift) -> None:
        self.x_focal = x_focal
        self.y_focal = y_focal
        self.x_shift = x_shift
        self.y_shift = y_shift

        self.disparity_shift = disparity_shift

        self.padding_x = 0
        self.padding_y = 0
        self.axis_forward_scale = 8

        infile = cv2.FileStorage(os.path.join(
            path, "parameters.xml"), cv2.FileStorage_READ)

        self.left_intrinsic = infile.getNode("left_intrinsic").mat()
        self.left_discoeffs = infile.getNode("left_discoeffs").mat()
        self.right_intrinsic = infile.getNode("right_intrinsic").mat()
        self.right_discoeffs = infile.getNode("right_discoeffs").mat()
        self.rotation1_2, _ = cv2.Rodrigues(infile.getNode("rotation1_2").mat())
        self.translastion1_2 = infile.getNode("translastion1_2").mat()
        self.vsm_type = infile.getNode("vsm_type").string()
        self.sub_vsm_type = infile.getNode("sub_vsm_type").string()
        self.baseline = infile.getNode("baseline").real()
        self.newInnerMatrix = np.array([
            [self.x_focal, 0, self.x_shift],
            [0, self.y_focal, self.y_shift],
            [0, 0, 1]
        ], dtype=np.float32)

        self.axis_fp_path = os.path.join(path, "axis.yml")
        self.axis_forward_fp_path = os.path.join(path, "axis_forward.yml")
        self.disp_mask_path = os.path.join(path,"mask.bmp")

    def update_map(self, x_focal, y_focal, x_shift, y_shift, disparity_shift):
        self.x_focal = np.clip(x_focal,1,np.inf)
        self.y_focal = np.clip(y_focal,1,np.inf)
        self.x_shift = np.clip(x_shift,1,np.inf)
        self.y_shift = np.clip(y_shift,1,np.inf)
        self.disparity_shift = disparity_shift

        self.generate_map(scale_x=2,scale_y=2)
    '''
    description : #*  *#
    param        {*} scale 基于QVGA的放大比例因子
    param        {*} padding 基于QVGA的扩展像素
    return       {*}
    '''
    def generate_map(self, scale_x = 1, scale_y = 1, padding_x = 0, padding_y = 0):
        self.newInnerMatrix = np.array([
            [self.x_focal*scale_x, 0, (self.x_shift)*scale_x],
            [0, self.y_focal*scale_y, (self.y_shift)*scale_y],
            [0, 0, 1]
        ], dtype=np.float32)
        
        e1 = np.array([[self.translastion1_2[0][0],self.translastion1_2[1][0],self.translastion1_2[2][0]]]).T/np.sqrt(self.translastion1_2[0][0]**2+self.translastion1_2[1][0]**2+self.translastion1_2[2][0]**2)
        e2 = np.array([[-self.translastion1_2[1][0],self.translastion1_2[0][0],0]]).T/np.sqrt(self.translastion1_2[0][0]**2+self.translastion1_2[1][0]**2)
        e3 = np.cross(e1.T,e2.T).T
        e = np.concatenate([e1,e2,e3],1).T
        e = np.mat(e)

        left_rotate = np.mat(self.newInnerMatrix) * e.I * (np.mat(self.newInnerMatrix).I)
        right_rotate = np.mat(self.newInnerMatrix) * (np.mat(self.rotation1_2) *  e).I * (np.mat(self.newInnerMatrix).I)

        if self.vsm_type == "b":
            h, w = 320, 240
        else:
            h, w = 240, 320
        shift_w = w+self.disparity_shift

        mapx, mapy = np.meshgrid(
            np.linspace(-padding_x*scale_x, (padding_x + shift_w)*scale_x-1, (shift_w + padding_x * 2)*scale_x),
            np.linspace(-padding_y*scale_y, (padding_y + h)*scale_y-1, (h + padding_y * 2)*scale_y),
        )
        mapL = np.stack([mapx, mapy, np.ones_like(mapx)], -1)
        mapR = np.stack([mapx, mapy, np.ones_like(mapx)], -1)

        r2L = np.zeros_like(mapL[..., 0])
        coefL = np.zeros_like(mapL[..., 0])

        r2R = np.zeros_like(mapR[..., 0])
        coefR = np.zeros_like(mapR[..., 0])

        for i in range(mapL.shape[0]):
            mapL[i] = (left_rotate*np.mat(mapL[i]).T).T
            mapL[i] = (mapL[i]/mapL[i, :, 2:]).astype(np.float32)
            mapL[i] = (np.mat(self.newInnerMatrix).I*np.mat(mapL[i].T)).T
            x = mapL[i, :, 0]
            y = mapL[i, :, 1]
            r2L[i] = x*x+y*y
            coefL[i] = self.left_discoeffs[0]*r2L[i]+self.left_discoeffs[1] * \
                r2L[i]**2+self.left_discoeffs[4]*r2L[i]**3+1
            mapL[i, :, 0] = x*coefL[i]+2*self.left_discoeffs[2] * \
                x*y+self.left_discoeffs[3]*(r2L[i]+2*x**2)
            mapL[i, :, 1] = y*coefL[i]+self.left_discoeffs[2] * \
                (r2L[i]+2*y**2)+2*self.left_discoeffs[3]*x*y
            mapL[i] = (np.mat(self.left_intrinsic)*np.mat(mapL[i].T)).T

        for i in range(mapR.shape[0]):
            mapR[i] = (right_rotate*np.mat(mapR[i]).T).T
            mapR[i] = (mapR[i]/mapR[i, :, 2:]).astype(np.float32)
            mapR[i] = (np.mat(self.newInnerMatrix).I*np.mat(mapR[i].T)).T
            x = mapR[i, :, 0]
            y = mapR[i, :, 1]
            r2R[i] = x*x+y*y
            coefR[i] = self.right_discoeffs[0]*r2R[i]+self.right_discoeffs[1] * \
                r2R[i]**2+self.right_discoeffs[4]*r2R[i]**3+1
            mapR[i, :, 0] = x*coefR[i]+2*self.right_discoeffs[2] * \
                x*y+self.right_discoeffs[3]*(r2R[i]+2*x*x)
            mapR[i, :, 1] = y*coefR[i]+self.right_discoeffs[2] * \
                (r2R[i]+2*y*y)+2*self.right_discoeffs[3]*x*y
            mapR[i] = (np.mat(self.right_intrinsic)*np.mat(mapR[i].T)).T


        if self.vsm_type == "b":
            mapL[..., [0, 1, 2]] = mapL[..., [1, 0, 2]]
            mapR[..., [0, 1, 2]] = mapR[..., [1, 0, 2]]
            if self.sub_vsm_type == "2" or self.sub_vsm_type == "3":
                mapL[..., 1] = w*2-1-mapL[..., 1]
            else:
                mapL[..., 0] = h*2-1-mapL[..., 0]
            if self.sub_vsm_type == "2" or self.sub_vsm_type == "4":
                mapR[..., 1] = w*2-1-mapR[..., 1]
            else:
                mapR[..., 0] = h*2-1-mapR[..., 0]
        elif self.vsm_type == "a":
            if self.sub_vsm_type == "1" or self.sub_vsm_type == "4":
                mapL[..., 0] = w*2-1-mapL[..., 0]
                mapL[..., 1] = h*2-1-mapL[..., 1]
                
            if self.sub_vsm_type == "1" or self.sub_vsm_type == "3":
                mapR[..., 0] = w*2-1-mapR[..., 0]
                mapR[..., 1] = h*2-1-mapR[..., 1]
                

        self.mapLx = mapL[..., 0]
        self.mapLy = mapL[..., 1]
        self.mapRx = mapR[..., 0]
        self.mapRy = mapR[..., 1]

        if self.disparity_shift != 0:
            self.mapLx = self.mapLx[:, self.disparity_shift*scale_x:]
            self.mapLy = self.mapLy[:, self.disparity_shift*scale_x:]
            self.mapRx = self.mapRx[:, :-self.disparity_shift*scale_x]
            self.mapRy = self.mapRy[:, :-self.disparity_shift*scale_x]
        self.mapLx = np.where((self.mapLx >= 0) & (
            self.mapLx <= 639), self.mapLx, -1).astype(np.float32)
        self.mapLy = np.where((self.mapLy >= 0) & (
            self.mapLy <= 479), self.mapLy, -1).astype(np.float32)
        self.mapRx = np.where((self.mapRx >= 0) & (
            self.mapRx <= 639), self.mapRx, -1).astype(np.float32)
        self.mapRy = np.where((self.mapRy >= 0) & (
            self.mapRy <= 479), self.mapRy, -1).astype(np.float32)


    def generate_forward_map(self): 
        self.generate_map(self.axis_forward_scale, self.axis_forward_scale, self.padding_x, self.padding_y)
        self.H, self.W = self.mapLx.shape
        self.mapLx_forward = np.ones([480, 640])*(-999)
        self.mapLy_forward = np.ones([480, 640])*(-999)
        self.mapRx_forward = np.ones([480, 640])*(-999)
        self.mapRy_forward = np.ones([480, 640])*(-999)
        
        mapLx = self.mapLx.astype(np.int32)
        mapLy = self.mapLy.astype(np.int32)
        mapRx = self.mapRx.astype(np.int32)
        mapRy = self.mapRy.astype(np.int32)
        x_shift = self.padding_x * self.axis_forward_scale
        y_shift = self.padding_y * self.axis_forward_scale
        
        # for h in range(self.H):
        #     if h > 0 and h % (self.H/4) == 0:
        #         print(h)
        #     for w in range(self.W):
        #         if mapLx[h, w] != -1 and mapLy[h, w] != -1:
        #             self.mapLx_forward[mapLy[h, w], mapLx[h, w]] = w #- x_shift
        #             self.mapLy_forward[mapLy[h, w], mapLx[h, w]] = h #- y_shift
        #             self.mapRx_forward[mapRy[h, w], mapRx[h, w]] = w #- x_shift
        #             self.mapRy_forward[mapRy[h, w], mapRx[h, w]] = h #- y_shift

        generatre_forward(
            self.H,self.W,mapLx,mapLy,mapRx,mapRy,self.mapLx_forward,self.mapLy_forward,self.mapRx_forward,self.mapRy_forward)


        self.mapLx_forward = np.where(self.mapLx_forward!=-999,self.mapLx_forward-x_shift,-999)
        self.mapLy_forward = np.where(self.mapLy_forward!=-999,self.mapLy_forward-y_shift,-999)
        self.mapRx_forward = np.where(self.mapRx_forward!=-999,self.mapRx_forward-x_shift,-999)
        self.mapRy_forward = np.where(self.mapRy_forward!=-999,self.mapRy_forward-y_shift,-999)
        
    def remap(self, img_L, img_R):
        remap_img_L = cv2.remap(img_L, self.mapLx, self.mapLy, cv2.INTER_LINEAR)
        remap_img_R = cv2.remap(img_R, self.mapRx, self.mapRy, cv2.INTER_LINEAR)
        return remap_img_L, remap_img_R

    def save(self):
        self.axis_fp = cv2.FileStorage(
            self.axis_fp_path, cv2.FileStorage_WRITE)
        self.axis_forward_fp = cv2.FileStorage(
            self.axis_forward_fp_path, cv2.FileStorage_WRITE)
        print(f"------start axis.yml saving---------")
        self.info_save()
        self.axis_save()
        print(f"------start axis_forward.yml saving---------")
        self.generate_forward_map()
        self.axis_forward_save()
        self.axis_fp.release()
        self.axis_forward_fp.release()
        print(f"------finish axis_forward.yml saving---------")

    def info_save(self):
        self.axis_fp.write("version", "2.5")
        self.axis_fp.write("vsm_type", self.vsm_type)
        self.axis_fp.write("sub_vsm_type", self.sub_vsm_type)
        self.axis_fp.write("yuv_image_width", 640)
        self.axis_fp.write("yuv_image_height", 480)
        self.axis_fp.write("baseline", self.baseline)
        self.axis_fp.write("disparity_shift", self.disparity_shift)
        self.axis_fp.write("disparity_range", 32)

    def axis_save(self):
        self.generate_map(scale_x=2,scale_y=2)
        self.axis_fp.write(f"Pl_640", self.newInnerMatrix)
        self.axis_fp.write(f"Pr_640", self.newInnerMatrix)
        self.axis_fp.write(f"left_x_640", self.mapLx.astype(np.int32))
        self.axis_fp.write(f"left_y_640", self.mapLy.astype(np.int32))
        self.axis_fp.write(f"right_x_640", self.mapRx.astype(np.int32))
        self.axis_fp.write(f"right_y_640", self.mapRy.astype(np.int32))

        self.generate_map(scale_x=1,scale_y=1)
        self.axis_fp.write(f"Pl_320", self.newInnerMatrix)
        self.axis_fp.write(f"Pr_320", self.newInnerMatrix)
        self.axis_fp.write(f"left_x_320", self.mapLx.astype(np.int32))
        self.axis_fp.write(f"left_y_320", self.mapLy)
        self.axis_fp.write(f"right_x_320", self.mapRx.astype(np.int32))
        self.axis_fp.write(f"right_y_320", self.mapRy.astype(np.int32))
        mapS = np.where((self.mapLx==-1)|(self.mapLy==-1),0,1).astype(np.uint8)
        mapS = cv2.erode(mapS,np.ones([21,21]),iterations = 1)
        cv2.imwrite(self.disp_mask_path,mapS)

    def axis_forward_save(self, ):
        self.axis_forward_fp.write("left_x_640", np.where(self.mapLx_forward == -999, -999, self.mapLx_forward//(self.axis_forward_scale//2)))
        self.axis_forward_fp.write("left_y_640", np.where(self.mapLy_forward == -999, -999, self.mapLy_forward//(self.axis_forward_scale//2)))
        self.axis_forward_fp.write("right_x_640", np.where(self.mapRx_forward == -999, -999, self.mapRx_forward//(self.axis_forward_scale//2)))
        self.axis_forward_fp.write("right_y_640", np.where(self.mapRy_forward == -999, -999, self.mapRy_forward//(self.axis_forward_scale//2)))

        self.axis_forward_fp.write("left_x_320", np.where(self.mapLx_forward == -999, -999, self.mapLx_forward//self.axis_forward_scale))
        self.axis_forward_fp.write("left_y_320", np.where(self.mapLy_forward == -999, -999, self.mapLy_forward//self.axis_forward_scale))
        self.axis_forward_fp.write("right_x_320", np.where(self.mapRx_forward == -999, -999, self.mapRx_forward//self.axis_forward_scale))
        self.axis_forward_fp.write("right_y_320", np.where(self.mapRy_forward == -999, -999, self.mapRy_forward//self.axis_forward_scale))

@jit(nopython=True)
def generatre_forward(H,W,mapLx,mapLy,mapRx,mapRy,mapLx_forward,mapLy_forward,mapRx_forward,mapRy_forward):
    for h in range(H):
        for w in range(W):
            if mapLx[h, w] != -1 and mapLy[h, w] != -1:
                mapLx_forward[mapLy[h, w], mapLx[h, w]] = w
                mapLy_forward[mapLy[h, w], mapLx[h, w]] = h
                mapRx_forward[mapRy[h, w], mapRx[h, w]] = w
                mapRy_forward[mapRy[h, w], mapRx[h, w]] = h
    # return mapLx_forward, mapLy_forward, mapRx_forward, mapRy_forward