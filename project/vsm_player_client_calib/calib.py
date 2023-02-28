'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-03-18 00:21:39
LastEditTime : 2022-10-05 17:20:47
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /calibrator/vsm_player_client_calib/calib.py
'''
import numpy as np
import cv2
import argparse
import os


def mono_calib(path, chessBoardShape, gridSize, vsm_type, sub_vsm_type, mode):
    print(f"------start {mode} mono calib---------")
    img_size = [640, 480] if vsm_type == "a" else [480, 640]
    cornersW = []
    for i in range(chessBoardShape[1]):
        for j in range(chessBoardShape[0]):
            cornersW.append([j*gridSize, i*gridSize, 0])
    cornersW = np.array(cornersW, dtype=np.float32)
    img_list = os.listdir(os.path.join(path, "calib", mode))
    img_list = [os.path.join(path, "calib", mode, x) for x in img_list]

    CornersW = []
    CornersI = []

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for img_name in img_list:
        img = cv2.imread(img_name)
        if vsm_type == "b":
            #! 为了消除CCI影响，采用对偶的装配调整
            if mode == "L":
                if sub_vsm_type == "2" or sub_vsm_type == "3":
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                else:
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif mode == "R":
                if sub_vsm_type == "2" or sub_vsm_type == "4":
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                else:
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif vsm_type == "a":
            #! 为了消除CCI影响，采用对偶的装配调整
            if mode == "L":
                if sub_vsm_type == "1" or sub_vsm_type == "4":
                    img = cv2.rotate(img, cv2.ROTATE_180)
            elif mode == "R":
                if sub_vsm_type == "1" or sub_vsm_type == "3":
                    img = cv2.rotate(img, cv2.ROTATE_180)

        ret, corner = cv2.findChessboardCorners(
            img, chessBoardShape, flags=cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret:
            cornersI = cv2.cornerSubPix(cv2.cvtColor(
                img, cv2.COLOR_BGR2GRAY), corner, (11, 11), (-1, -1), criteria)[:, 0, :]
            CornersI.append(cornersI)
            CornersW.append(cornersW)
        else:
            print(f"{img_name} not used")
    erms, intrinsicMatrix, distortion = cv2.calibrateCamera(
        CornersW, CornersI, img_size, None, None)[:3]

    print(
        f"------finish {mode} mono calib, error root mean square: {erms:.3f} pixel---------")
    return intrinsicMatrix, distortion, erms


def stereo_calib(path,chessBoardShape,gridSize,vsm_type,sub_vsm_type,left_intrinsic, right_intrinsic, left_discoeffs, right_discoeffs):
    print(f"------start stereo calib---------")

    cornersW = []
    for i in range(chessBoardShape[1]):
        for j in range(chessBoardShape[0]):
            cornersW.append([j, i, 0])
    objectPoints = np.array(cornersW, dtype=np.float32)*gridSize
    img_L_list = os.listdir(os.path.join(path, "calib", "S", "L"))
    img_R_list = os.listdir(os.path.join(path, "calib", "S", "R"))
    img_L_list = sorted(img_L_list, key=lambda x: int(x.split("_")[0]))
    img_R_list = sorted(img_R_list, key=lambda x: int(x.split("_")[0]))
    img_L_list = [os.path.join(path, "calib", "S", "L", x)
                  for x in img_L_list]
    img_R_list = [os.path.join(path, "calib", "S", "R", x)
                  for x in img_R_list]

    Rvec_1to2 = []
    Tvec_1to2 = []
    proj_err = []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for (img_L_name, img_R_name) in zip(img_L_list, img_R_list):

        img_L = cv2.imread(img_L_name)
        img_R = cv2.imread(img_R_name)
        if vsm_type == "b":
            #! 为了消除CCI影响，采用对偶的装配调整
            if sub_vsm_type == "2" or sub_vsm_type == "3":
                img_L = cv2.rotate(img_L, cv2.ROTATE_90_CLOCKWISE)
            else:
                img_L = cv2.rotate(img_L, cv2.ROTATE_90_COUNTERCLOCKWISE)

            if sub_vsm_type == "2" or sub_vsm_type == "4":
                img_R = cv2.rotate(img_R, cv2.ROTATE_90_CLOCKWISE)
            else:
                img_R = cv2.rotate(img_R, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif vsm_type == "a":
            #! 为了消除CCI影响，采用对偶的装配调整
            if sub_vsm_type == "1" or sub_vsm_type == "4":
                img_L = cv2.rotate(img_L, cv2.ROTATE_180)

            if sub_vsm_type == "1" or sub_vsm_type == "3":
                img_R = cv2.rotate(img_R, cv2.ROTATE_180)

        ret_l, cornersi_L = cv2.findChessboardCorners(
            img_L, chessBoardShape)
        ret_r, cornersi_R = cv2.findChessboardCorners(
            img_R, chessBoardShape)
        if ret_l and ret_r:
            cornersi_L = cv2.cornerSubPix(cv2.cvtColor(
                img_L, cv2.COLOR_BGR2GRAY), cornersi_L, (11, 11), (-1, -1), criteria)[:, 0, :]
            cornersi_R = cv2.cornerSubPix(cv2.cvtColor(
                img_R, cv2.COLOR_BGR2GRAY), cornersi_R, (11, 11), (-1, -1), criteria)[:, 0, :]
            ret, rvec1, tvec1 = cv2.solvePnP(
                objectPoints, cornersi_L, left_intrinsic, left_discoeffs)
            ret, rvec2, tvec2 = cv2.solvePnP(
                objectPoints, cornersi_R, right_intrinsic, right_discoeffs)
            R1, _ = cv2.Rodrigues(rvec1)
            R2, _ = cv2.Rodrigues(rvec2)
            R1 = np.mat(R1)
            R2 = np.mat(R2)

            rmtx_1to2 = R1 * R2.T
            rvec_1to2, _ = cv2.Rodrigues(rmtx_1to2)
            tvec_1to2 = tvec1 - rmtx_1to2 * tvec2

            Rvec_1to2.append(rvec_1to2)
            Tvec_1to2.append(tvec_1to2)
            
            imagePoints1 = cv2.projectPoints(
                objectPoints, rvec1, tvec1, left_intrinsic, left_discoeffs)[0].squeeze()
            imagePoints2 = cv2.projectPoints(
                objectPoints, rvec2, tvec2, right_intrinsic, right_discoeffs)[0].squeeze()
            proj_err.append(cv2.norm(imagePoints1, cornersi_L, cv2.NORM_L2) +
                            cv2.norm(imagePoints2, cornersi_R, cv2.NORM_L2))
        else:
            print(f"{img_L_name} not used")

    proj_err = np.array(proj_err)
    softmax_proj_err = np.exp(-proj_err)/np.sum(np.exp(-proj_err))
    erms = np.sqrt(np.sum(softmax_proj_err*np.square(proj_err))/proj_err.shape[0])

    tvec_1to2 = np.sum(np.array(Tvec_1to2)*softmax_proj_err.reshape(-1, 1, 1), axis=0)
    rvec_1to2 = np.sum(np.array(Rvec_1to2)*softmax_proj_err.reshape(-1, 1, 1), axis=0)
        
    print(
        f"------finish stereo calib, error root mean square: {erms:.3f} pixel---------")

    return rvec_1to2, tvec_1to2, erms


def auto_detect(path, chessBoardShape):
    auto_detect_ret = -1
    vsm_type = None 
    sub_vsm_type = None
    img_L_list = os.listdir(os.path.join(path, "detect", "L"))
    img_R_list = os.listdir(os.path.join(path, "detect", "R"))
    if len(img_L_list)>0 and len(img_R_list)>0:
        img_L_list = [os.path.join(path, "detect", "L", x)
                    for x in img_L_list][0]
        img_R_list = [os.path.join(path, "detect", "R", x)
                    for x in img_R_list][0]
        
        img_L = cv2.imread(img_L_list)
        img_R = cv2.imread(img_R_list)

        result_L = auto_detect_mono(img_L, chessBoardShape)
        result_R = auto_detect_mono(img_R, chessBoardShape)

        if result_L['ret'] and result_R['ret']:
            auto_detect_ret, vsm_type, sub_vsm_type = check_vsm_type(result_L,result_R)
        else:
            print("未检测到有效标定板区域")
    else:
        print("没有检测图片")
    return auto_detect_ret, vsm_type, sub_vsm_type
'''
description : #* 检测时vsm必须正放 *#
param        {*} img
param        {*} chessBoardShape
return       {*}
'''

def check_chessborad_single(img,chessBoardShape):
    cornersW = []
    for i in range(chessBoardShape[1]):
        for j in range(chessBoardShape[0]):
            cornersW.append([j, i, 0])
    ret, corners = cv2.findChessboardCorners(img, chessBoardShape)
    return ret
    
def auto_detect_mono(img, chessBoardShape):
    cornersW = []
    for i in range(chessBoardShape[1]):
        for j in range(chessBoardShape[0]):
            cornersW.append([j, i, 0])
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, cornersi = cv2.findChessboardCorners(img, chessBoardShape)
    cornersi_tl0 = np.array([0,0],dtype = np.int32)
    direction_tl = np.array([0,0],dtype = np.int32)
    if ret:
        cornersi = cv2.cornerSubPix(cv2.cvtColor(
            img, cv2.COLOR_BGR2GRAY), cornersi, (11, 11), (-1, -1), criteria)[:, 0, :]

        cornersi_tl0 = cornersi[chessBoardShape[0]
                                * (chessBoardShape[1]-1)]
        cornersi_tl1 = cornersi[chessBoardShape[0]
                                * (chessBoardShape[1]-2)+1]
        vector_tl = cornersi_tl1-cornersi_tl0
        vector_tl = vector_tl / \
            cv2.norm(vector_tl, np.array(
                [0, 0], dtype=np.float32), cv2.NORM_L2)
        direction_tl = np.sign(vector_tl)

    return {"ret": ret, "corner": cornersi_tl0.astype(np.int32), "direction": direction_tl.astype(np.int32)}

def check_vsm_type(result_L, result_R):
    ret = 0
    vsm_type = None
    sub_vsm_type = None

    if result_L['direction'][0] == 1:
        # A型0图xu同向，yv同向
        if result_L['direction'][1] == 1:
            vsm_type="a"
            if result_R['direction'][0] == 1 and result_R['direction'][1] == 1:
                if result_L['corner'][0]>result_R['corner'][0]:
                    #! 为了消除CCI影响，采用对偶的装配调整
                    sub_vsm_type = "2"
                else:
                    sub_vsm_type = "1"
            elif result_R['direction'][0] == -1 and result_R['direction'][1] == -1:
                if result_L['corner'][0]<640-result_R['corner'][0]:
                        #! 为了消除CCI影响，采用对偶的装配调整
                    sub_vsm_type = "4"
                else:
                    sub_vsm_type = "3"
        # B型0图xv逆向，yu同向
        else:
            vsm_type="b"
            if result_R['direction'][0] == 1 and result_R['direction'][1] == -1:
                if result_L['corner'][1]<result_R['corner'][1]:
                        #! 为了消除CCI影响，采用对偶的装配调整
                    sub_vsm_type = "2"
                else:
                    sub_vsm_type = "1"
            elif result_R['direction'][0] == -1 and result_R['direction'][1] == 1:
                if result_L['corner'][1]>480-result_R['corner'][1]:
                        #! 为了消除CCI影响，采用对偶的装配调整
                    sub_vsm_type = "4"
                else:
                    sub_vsm_type = "3"
    else:
        print("不符合A型或B型的检测摆放姿态")
        ret = -1

    return ret, vsm_type, sub_vsm_type

def get_baseline(translastion_x):
    return np.abs(np.round(translastion_x.item()/10)*10).astype(np.uint8)
   
def saveResult(path, left_intrinsic, right_intrinsic, left_discoeffs, right_discoeffs, rotation1_2, translastion1_2, baseline, vsm_type, sub_vsm_type):
    parameter_fp = cv2.FileStorage(os.path.join(path, "parameters.xml"), cv2.FileStorage_WRITE)
    parameter_fp.write("vsm_type", vsm_type)
    parameter_fp.write("sub_vsm_type", sub_vsm_type)
    parameter_fp.write("baseline", baseline//10)
    parameter_fp.write("left_intrinsic", left_intrinsic)
    parameter_fp.write("right_intrinsic", right_intrinsic)
    parameter_fp.write("left_discoeffs", left_discoeffs)
    parameter_fp.write("right_discoeffs", right_discoeffs)
    parameter_fp.write("rotation1_2", rotation1_2)
    parameter_fp.write("translastion1_2", translastion1_2)
    parameter_fp.release()

