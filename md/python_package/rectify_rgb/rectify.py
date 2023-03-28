'''
Author       : JiaYu.Wu
Email        : a472796892@gmail.com
Company      : Magic Depth
Date         : 2021-11-20 15:51:51
LastEditTime : 2022-10-09 18:29:32
LastEditors  : JiaYu.Wu
Description  : #* *#
FilePath     : /test/rectify.py
'''
import cv2
import os
import numpy as np


class Rectify:
    def __init__(self, path):
        infile = cv2.FileStorage(os.path.join(
            path, "axis.yml"), cv2.FileStorage_READ)
        self.baseline = infile.getNode(
            "baseline").real()
        self.fx = infile.getNode(
            "Pl_640").mat()[0,0].astype(np.float32)

        self.mapLx = infile.getNode(
            "left_x_640").mat().astype(np.float32)
        self.mapLy = infile.getNode(
            "left_y_640").mat().astype(np.float32)
        self.mapRx = infile.getNode(
            "right_x_640").mat().astype(np.float32)
        self.mapRy = infile.getNode(
            "right_y_640").mat().astype(np.float32)
        # if os.path.exists(os.path.join(
        #     path, "axis_forward.yml")):
        #     infile = cv2.FileStorage(os.path.join(
        #         path, "axis_forward.yml"), cv2.FileStorage_READ)
        #     self.mapLx_forward = infile.getNode(
        #         "left_x_320").mat().astype(np.float32)
        #     self.mapLy_forward = infile.getNode(
        #         "left_y_320").mat().astype(np.float32)
        #     self.mapRx_forward = infile.getNode(
        #         "right_x_320").mat().astype(np.float32)
        #     self.mapRy_forward = infile.getNode(
        #         "right_y_320").mat().astype(np.float32)

    def remap_pic(self, imageL, imageR,shift = 0):
        map_imageL = cv2.remap(
            imageL, self.mapLx, self.mapLy-shift, cv2.INTER_LINEAR)
        map_imageR = cv2.remap(
            imageR, self.mapRx, self.mapRy, cv2.INTER_LINEAR)
        return map_imageL, map_imageR
    
    def get_undistortPos(self, point:np.ndarray, mode = "L")->np.ndarray:
        if mode == "L":
            undistortPoint = np.array([self.mapLx_forward[point[1],point[0]],self.mapLy_forward[point[1],point[0]]],dtype=np.int32)
        elif mode == "R":
            undistortPoint = np.array([self.mapRx_forward[point[1],point[0]],self.mapRy_forward[point[1],point[0]]],dtype=np.int32)
    
        return undistortPoint
    def get_undistortRec(self, box:np.ndarray)->np.ndarray:
        # 左上角开始顺时针
        points = np.array([[box[0], box[1]], [box[2], box[1]], [
            box[2], box[3]], [box[0], box[3]]], dtype=np.int32)
        undistortPoints = np.zeros_like(points)
        for index in range(4):
            undistortPoints[index,0]=self.mapLx_forward[points[index,1],points[index,0],]
            undistortPoints[index,1]=self.mapLy_forward[points[index,1],points[index,0],]
        return undistortPoints.astype(np.int32)
        
class AxisTransform:
    def __init__(self, input_path:os.PathLike, height_threshold:int = 60) -> None:
        self.height_threshold = height_threshold
        # 视差图内参
        axis_params_path = os.path.join(input_path, "axis.yml")
        axis_params = cv2.FileStorage(axis_params_path, cv2.FileStorage_READ)
        self.baseline = axis_params.getNode('baseline').real()
        self.disparity_shift = axis_params.getNode(
            'disparity_shift').real()

        parameters_params_path1 = os.path.join(input_path, "axis.yml")
        parameters_params1 = cv2.FileStorage(
            parameters_params_path1, cv2.FileStorage_READ)
        projection_l = parameters_params1.getNode('Pl_320').mat()
        self.f320y = projection_l[0, 0]/2
        self.f320x = projection_l[1, 1]/2
        self.c320y = projection_l[0, 2]/2
        self.c320x = 240-projection_l[1, 2]/2

        track_params_path = os.path.join(input_path, "initialize_params.yml")
        track_param = cv2.FileStorage(track_params_path, cv2.FileStorage_READ)
        self.transform_inited = track_param.getNode(
            "transform_inited").real()

        self.rgb_shift_x = int(track_param.getNode("rgb_shift_x").real())
        self.rgb_shift_y = int(track_param.getNode("rgb_shift_y").real())

        escalator_map_x = track_param.getNode(
            "height_curve_location_map").mat()
        escalator_map_k = track_param.getNode("height_curve_slope_map").mat()
        escalator_map_b = track_param.getNode("height_curve_bias_map").mat()
        self.HeightMap = np.stack(
            [escalator_map_x, escalator_map_k, escalator_map_b])

        if self.transform_inited == 1:
            rotation = track_param.getNode("rotation").mat()
            translation = track_param.getNode("translation").mat()
            self.translation = np.mat(translation)
            self.rotationmatrix = np.mat(cv2.Rodrigues(rotation)[0])
            self.camera_pos = -self.rotationmatrix.I*self.translation
            self.camera_pos[2] = -self.camera_pos[2]
        else:
            self.origin_x = track_param.getNode("origin_x").real()
            self.origin_y = track_param.getNode("origin_y").real()
            self.camera_ground_height = track_param.getNode(
                "camera_ground_height").real()
            self.camera_pos = np.array(
                [self.origin_x, self.origin_y, self.camera_ground_height])

    '''
    description : #* 根据配置移动图像 *#
    param        {*} self
    param        {np.ndarray} img 图像
    return       {np.ndarray}
    '''
    def img_shift(self, img:np.ndarray)->np.ndarray:
        if self.rgb_shift_y > 0:
            img = cv2.hconcat([np.zeros(
                [img.shape[0], self.rgb_shift_y], dtype=np.uint8), img[:, :-self.rgb_shift_y]])
        else:
            img = cv2.hconcat(
                [img[:, -self.rgb_shift_y:], np.zeros([img.shape[0], -self.rgb_shift_y], dtype=np.uint8)])
        if self.rgb_shift_x > 0:
            img = cv2.vconcat([np.zeros(
                [self.rgb_shift_x, img.shape[1], ], dtype=np.uint8), img[:-self.rgb_shift_x, :]])
        else:
            img = cv2.vconcat(
                [img[-self.rgb_shift_x:, :], np.zeros([-self.rgb_shift_x, img.shape[1], ], dtype=np.uint8)])
        return img

    '''
    description : #*  *#
    param        {*} self
    param        {np.ndarray} image_location 640图像点位置【u,v,d】
    return       {np.ndarray} 世界坐标系位置【X, Y, Z】
    '''
    def calc_world_point(self, image_location:np.ndarray) -> np.ndarray:
        # 图像像素坐标系
        image_location = np.array(image_location).reshape(-1, 3)
        imagePixelX, imagePixelY, imagePixelZ = image_location[:,
                                                               0], image_location[:, 1], image_location[:, 2]
        # 图像物理坐标系
        imagePhysicsX = 240-imagePixelY/2
        imagePhysicsY = imagePixelX/2
        imagePhysicsZ = imagePixelZ + self.disparity_shift
        # 相机坐标系320
        camera320Z = np.where(imagePhysicsZ == 0, 0,
                              self.f320x*self.baseline/imagePhysicsZ)
        camera320X = (imagePhysicsX-self.c320x)*camera320Z/self.f320x
        camera320Y = (imagePhysicsY-self.c320y)*camera320Z/self.f320y
        # 相机坐标系640
        camera640X = camera320Y
        camera640Y = -camera320X
        camera640Z = camera320Z
        # 世界坐标系
        if self.transform_inited == 1:
            [WorldX, WorldY, WorldZ] = self.rotationmatrix.I*(
                np.array([camera640X, camera640Y, camera640Z])-self.translation)
            WorldZ = -np.array(WorldZ)
        else:
            WorldX, WorldY, WorldZ = -self.origin_x-camera640X, - \
                self.origin_y-camera640Y, self.camera_ground_height-camera640Z
            WorldX = np.expand_dims(WorldX, 0)
            WorldY = np.expand_dims(WorldY, 0)
            WorldZ = np.expand_dims(WorldZ, 0)
        World = np.array(
            [WorldX.tolist()[0], WorldY.tolist()[0], WorldZ.tolist()[0]])
        return np.round(World, 2)

    '''
    description : #*  *#
    param        {*} self
    param        {np.ndarray} world_location 世界坐标系位置【X, Y, Z】
    return       {np.ndarray} 640图像点位置【u,v,d】
    '''
    def calc_camera_point(self, world_location:np.ndarray) -> np.ndarray:
        world_location = np.array(world_location).reshape(-1, 3)
        # 相机坐标系640
        WorldX, WorldY, WorldZ = world_location[:,
                                                0], world_location[:, 1], world_location[:, 2]
        if self.transform_inited == 1:
            [camera640X, camera640Y, camera640Z] = self.rotationmatrix * \
                np.array([WorldX, WorldY, -WorldZ])+self.translation
        else:
            [camera640X, camera640Y, camera640Z] = np.mat(
                [-self.origin_x-WorldX, -self.origin_y-WorldY, self.camera_ground_height-WorldZ])

        # 相机坐标系320
        camera320X = -camera640Y
        camera320Y = camera640X
        camera320Z = camera640Z

        # 图像物理坐标系
        imagePhysicsX = np.where(
            camera320Z == 0, self.c320x, camera320X * self.f320x / camera320Z + self.c320x)
        imagePhysicsY = np.where(
            camera320Z == 0, self.c320y, camera320Y * self.f320y / camera320Z + self.c320y)
        imagePhysicsZ = np.where(
            camera320Z == 0, 0, self.f320x*self.baseline/camera320Z)

        # 图像像素坐标系
        imagePixelX = np.round(2*imagePhysicsY, 2)
        imagePixelY = np.round(480-2*imagePhysicsX, 2)
        imagePixelZ = np.round(imagePhysicsZ-self.disparity_shift, 2)

        return np.array([imagePixelX.tolist()[0], imagePixelY.tolist()[0], imagePixelZ.tolist()[0]]).T

    '''
    description : #* 相对坐标与绝对坐标的互相转换 *#
    param        {*} self
    param        {np.ndarray} world_location 转换前坐标
    param        {str} mode 【relative】: 绝对坐标转相对坐标; 【absolute】: 相对坐标转绝对坐标
    return       {np.ndarray}
    '''
    def get_height(self, world_location:np.ndarray, mode:str="relative") -> np.ndarray:
        # 0.5舍0.501入, 且避免曲线太远导致的index超范围
        location = world_location.copy()
        ground_index = np.where(np.abs(
            self.HeightMap[0]-location[0]) == np.abs(self.HeightMap[0]-location[0]).min())[0][0]
        if mode == "relative":
            location[-1] = location[-1] * self.HeightMap[1,
                                                         ground_index] + self.HeightMap[2, ground_index]
        elif mode == "absolute":
            location[-1] = (location[-1] - self.HeightMap[2,
                                                          ground_index]) / self.HeightMap[1, ground_index]
        return np.round(location, 2)
