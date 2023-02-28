'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-09 15:48:38
LastEditTime : 2022-09-20 16:09:03
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /calibrator/vsm_player_client_calib/decoder.py
'''
import av
import numpy as np
import os
import sys
import struct
import ctypes


# 导入ctypes库, 判断操作系统
def get_ctypes_lib(lib_file_dir, lib_file_name):
    """
    获取ctypes库.
    :param lib_file_dir: 库文件的目录
    :param lib_file_name: 库文件的名称
    :return: ctypes库
    """
    lib_file_name_no_ext = os.path.splitext(lib_file_name)[0]
    if sys.platform.startswith('win32'):
        lib_file_path = os.path.join(lib_file_dir, 'libs', f'{lib_file_name_no_ext}.dll')
    elif sys.platform.startswith('linux'):
        lib_file_path = os.path.join(lib_file_dir, 'libs', f'{lib_file_name_no_ext}.so')
    else:
        raise NotImplementedError
    return ctypes.CDLL(lib_file_path)


class depth_decoder:
    def __init__(self):
        self.lib_fastlz = get_ctypes_lib(os.path.dirname(os.path.abspath(__file__)), 'libfastlz.so')

    def get_depth_image(self, image_info, image_data):
        image_height = image_info['ImageHeight']
        image_width = image_info['ImageWidth']
        image_size = image_height * image_width
        if len(image_data) != image_size:
            # 使用fastlz解压
            p_raw_depth_img = ctypes.c_char_p(image_data)
            image = np.zeros(image_width * image_height, dtype='uint8', order='C')
            p_depth_img = image.ctypes.data_as(ctypes.c_char_p)
            self.lib_fastlz.fastlz_decompress(p_raw_depth_img, image_size, p_depth_img,
                                              image_size)
        else:
            rawdata = struct.unpack(f'>{len(image_data)}B', image_data)
            image = np.array(rawdata, dtype=np.uint8).reshape(image_height, image_width)

        return image


class h264_decoder:
    def __init__(self):
        self.codec = av.CodecContext.create('h264', 'r')
        self.have_i_frame = False

        self.lib_yuv_lite = get_ctypes_lib(os.path.dirname(os.path.abspath(__file__)), 'libyuv-lite.so')

    def get_image(self, image_info, image_data):
        image_height = image_info['ImageHeight']
        image_width = image_info['ImageWidth']
        # 如果数据为原始yuv，则直接解析
        if len(image_data) == image_width*image_height*1.5:
            return self.raw_yuv_data_to_rgb(image_data, image_width, image_height)
        # 如果数据不是原始yuv，则使用h264解码
        if image_data.hex()[9] == '7':
            self.have_i_frame = True
        if self.have_i_frame is False:
            return None
        packets = self.codec.parse(image_data)
        if len(packets) == 0:
            packets = self.codec.parse(None)
        for packet in packets:
            try:
                frames = self.codec.decode(packet)
            except Exception:
                print('packet is wrong')
                return None
            for frame in frames:
                return self.raw_yuv_data_to_rgb(frame, image_width, image_height)

    def raw_yuv_data_to_rgb(self, frame, image_width, image_height):
        if isinstance(frame, bytes):
            yuv_data = np.frombuffer(frame, dtype=np.uint8)
            raw_yuv_data = self.change_uv(yuv_data, image_width, image_height)
        else:
            yuv_data = frame.to_ndarray(format='yuv420p')
            raw_yuv_data = self.change_uv(yuv_data.reshape(-1), image_width, image_height)
        # 取数据指针
        p_raw_yuv_data = raw_yuv_data.ctypes.data_as(ctypes.c_char_p)

        rgb_data = np.zeros(
            shape=image_height * image_width * 3, dtype='uint8', order='C')
        p_rgb_data = rgb_data.ctypes.data_as(ctypes.c_char_p)

        self.lib_yuv_lite.YuvToRGB(p_raw_yuv_data, image_width, image_height, p_rgb_data)

        return rgb_data.reshape((image_height, image_width, 3)).astype('uint8')

    def change_uv(self, raw_yuv_data, image_width, image_height):
        yuv_data_swap = raw_yuv_data.copy()
        half_width = image_width // 2
        half_height = image_height // 2
        yuv_data_swap[image_width*image_height:(image_width*image_height+half_width*half_height)] = raw_yuv_data[(image_width*image_height+half_width*half_height):]
        yuv_data_swap[(image_width*image_height+half_width*half_height):] = raw_yuv_data[image_width*image_height:(image_width*image_height+half_width*half_height)]
        raw_yuv_data = yuv_data_swap
        return raw_yuv_data
