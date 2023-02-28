import socket
import threading
import multiprocessing
import time
from collections import deque
from decoder import *

import storage_structure
from storage_structure import SVPCM_IMAGE_TYPE

class Receive_data_client(threading.Thread):
    def __init__(self, channel_id=0):
        threading.Thread.__init__(self,daemon=True)
        self.server_info = None
        self.channel_id = channel_id
        self.sock = None
        self.data = b''
        self.data_queue = deque(maxlen=50)
        self.run_time = 0
        self.pasue_flag = True
        self.stop_flag = False
        self.connection_status = False
        self.connect_vsm=False
        self.disconnect_vsm=False
        self.connect_vsm_failed=False
        self.dataqueue_warning=False

    def set_server_info(self, server_info):
        self.server_info = server_info
    
    def clear_server_info(self):
        self.server_info = None

    def connect_to_server(self):

        try:
            socket.setdefaulttimeout(3)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'连接到 {self.server_info}')
            
            if self.server_info is not None:
                self.sock.connect(self.server_info)
                self.connect_vsm=True
                self.disconnect_vsm=False
                self.connection_status = True
            time.sleep(0.1)
        except socket.error as msg:
            self.sock = None
            self.connect_vsm=False
            print(msg)
            self.connect_vsm_failed=True
            print("Socket连接失败: 请检查程序运行状态、IP地址、端口号、网络连接")

    def close_connect(self):
        if self.sock is not None:
            self.sock.close()
            print('连接关闭成功')
            self.connect_vsm_failed=False
            self.connect_vsm=False
            self.disconnect_vsm=True
            self.dataqueue_warning=False
        else:
            print('已经关闭')
            self.connect_vsm_failed=False
            self.connect_vsm=False
            self.dataqueue_warning=False
        self.sock = None
        self.run_time = 0
        self.connection_status = False
        self.data = b''

    def run(self):
        err_data_time=0
        err_connection_time=0
        while True:
            if self.stop_flag:
                break
            if self.pasue_flag==True:
                time.sleep(0.1)
                continue
            try:
                recv_data = self.sock.recv(4000000)
                self.data += recv_data
                if len(self.data) < 32:
                    err_data_time += 1
                else:
                    err_data_time = 0
                    err_connection_time = 0
                if err_data_time > 20:
                    print("无法收到有效数据，重新连接")
                    self.close_connect()
                    # time.sleep(0.1)
                    raise Exception
                elif err_data_time != 0:
                    continue

                block_info = storage_structure.tag_image_frame(self.data)
                packet_length = block_info['PacketLength']
                
                # 保证顺利读取数据
                if len(self.data) < packet_length:
                    continue
                block_data = self.data[:packet_length]
                check_sum = block_info['CheckSum']
                cal_check_sum = storage_structure.check_sum_32(block_data, len(block_data))
                image_type = SVPCM_IMAGE_TYPE(block_info['ImageType']).value
                image_sequence = block_info['ImageSequence']
                image_width = block_info['ImageWidth']
                image_height = block_info['ImageHeight']
                image_time_stamp = block_info['TimeStamp']
                image_quality = block_info['ImageQuality']
                image_data = block_data[32:]

                self.data = self.data[packet_length:]

                block_status = 4294967295 - check_sum == cal_check_sum
                if not block_status:
                    print('数据校验失败')
                    print(block_data[:100])
                    continue
                self.image_info = {'ImageType': image_type, 'ImageSequence': image_sequence, 'ImageWidth': image_width,
                            'ImageHeight': image_height, 'TimeStamp': image_time_stamp,
                            'ImageChannel': self.channel_id, 'ImageQuality': image_quality,
                            'ImageDataStatus': block_status}
                if len(self.data_queue) > 35:
                    print(f"警告：通道 {self.channel_id} 的数据队列达到警戒线 {len(self.data_queue)}，请检查程序是否正常")
                    self.dataqueue_warning=True
                self.data_queue.append((self.image_info, image_data))

            except Exception as e:
                if self.sock is None:
                    self.connect_vsm=False
                    if self.server_info is None:
                        continue
                    else:
                        print(f'尝试连接{self.server_info}第{self.run_time}次')
                        time.sleep(0.5)
                        self.connect_to_server()
                else:
                    err_connection_time+=1
                    if err_connection_time>5:
                        print("连接超时")
                        print(f'尝试连接{self.server_info}第{self.run_time}次')
                        time.sleep(0.5)
                        self.connect_to_server()
                self.run_time += 1
                self.data = b''

            time.sleep(0.01)

    def get_data(self):
        return self.data_queue.popleft() if len(self.data_queue) else None


class ParseImageData(threading.Thread):
    def __init__(self, channel_id, receive_client, input_depth_queue:multiprocessing.Queue, input_left_rgb_queue:multiprocessing.Queue, input_right_rgb_queue:multiprocessing.Queue):
        threading.Thread.__init__(self,daemon=True)
        self.channel_id = channel_id
        self.receive_client = receive_client
        self.input_depth_queue = input_depth_queue
        self.input_left_rgb_queue = input_left_rgb_queue
        self.input_right_rgb_queue = input_right_rgb_queue
        self.accept_data = True
        self.stop_flag = False

    def run(self):
        while True:
            if self.stop_flag:
                break
            if self.accept_data:
                image_data = self.receive_client.get_data()
                if image_data is None:
                    time.sleep(0.001)
                    continue
                    
                if image_data[0]['ImageType'] == SVPCM_IMAGE_TYPE.IMAGE_TYPE_DEPTH.value:
                    self.input_depth_queue.put(image_data)
                    if self.input_depth_queue.qsize() >= 15:
                        print(f"警告： depth_data_deque的数据队列达到警戒线 {self.input_depth_queue.qsize()}，请检查程序是否正常")
                        self.dataqueue_warning=True
                elif image_data[0]['ImageType'] == SVPCM_IMAGE_TYPE.IMAGE_TYPE_LEFT_COLOR.value:
                    self.input_left_rgb_queue.put(image_data)
                    if self.input_left_rgb_queue.qsize() >= 15:
                        print(f"警告： l_yuv_data_deque的数据队列达到警戒线 {self.input_left_rgb_queue.qsize()}，请检查程序是否正常")
                        self.dataqueue_warning=True
                elif image_data[0]['ImageType'] == SVPCM_IMAGE_TYPE.IMAGE_TYPE_RIGHT_COLOR.value:
                    self.input_right_rgb_queue.put(image_data)
                    if self.input_right_rgb_queue.qsize() >= 15:
                        print(f"警告： l_yuv_data_deque的数据队列达到警戒线 {self.input_right_rgb_queue.qsize()}，请检查程序是否正常")
                        self.dataqueue_warning=True
            else:
                if not self.input_depth_queue.empty():
                    self.input_depth_queue.get()                
                if not self.input_left_rgb_queue.empty():
                    self.input_left_rgb_queue.get()                
                if not self.input_right_rgb_queue.empty():
                    self.input_right_rgb_queue.get()
            time.sleep(0.02)


class ParseImageData2Image_Process(multiprocessing.Process):
    def __init__(self, input_queue:multiprocessing.Queue, output_queue:multiprocessing.Queue, image_type, rgb_shape=(640, 480)):
        multiprocessing.Process.__init__(self,daemon=True)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.image_type = image_type
        self.accept_data = True
        self.stop_flag = False
        self.rgb_shape = rgb_shape
    def run(self):
        if self.image_type == 'depth':
            self.decoder = depth_decoder()
        elif self.image_type in ['l_yuv', 'r_yuv']:
            self.decoder = h264_decoder()
        while True:
            if self.stop_flag:
                break
            if self.accept_data:
                if not self.input_queue.empty():
                    data = self.input_queue.get(block=True, timeout=0.1)
                    if data is not None:
                        image_info = data[0]
                        image_data = data[1]
                        if self.image_type == 'depth':
                            image = self.decoder.get_depth_image(image_info, image_data)
                        elif self.image_type in ['l_yuv', 'r_yuv']:
                            image = self.decoder.get_image(image_info, image_data)
                        self.output_queue.put((image_info, image))
                time.sleep(0.02)
            else:
                if not self.input_queue.empty():
                    self.input_queue.get()
                    
class ParseImage(threading.Thread):
    def __init__(self, output_queue_list):
        threading.Thread.__init__(self,daemon=True)
        self.output_depth_queue = output_queue_list[0]
        self.output_left_rgb_queue = output_queue_list[1]
        self.output_right_rgb_queue = output_queue_list[2]

        self.depth_sequence_deque = deque(maxlen=5)
        self.left_rgb_sequence_deque = deque(maxlen=5)
        self.right_rgb_sequence_deque = deque(maxlen=5)

        self.depth_info_deque = deque(maxlen=5)
        self.left_rgb_info_deque = deque(maxlen=5)
        self.right_rgb_info_deque = deque(maxlen=5)

        self.depth_image_deque = deque(maxlen=5)
        self.left_rgb_image_deque = deque(maxlen=5)
        self.right_rgb_image_deque = deque(maxlen=5)

        self.last_sequence = [None, None, None]
        
        self.accept_data = True
        self.stop_flag = False

    def run(self):
        while True:
            if self.stop_flag:
                break
            if self.accept_data:
                if not self.output_depth_queue.empty():
                    depth_data = self.output_depth_queue.get(block=True, timeout=0.1)
                    depth_info = depth_data[0]
                    depth_image = depth_data[1]
                    self.depth_sequence_deque.append(depth_info['ImageSequence'])
                    self.depth_info_deque.append(depth_info)
                    self.depth_image_deque.append(depth_image)
                if not self.output_left_rgb_queue.empty():
                    left_rgb_data = self.output_left_rgb_queue.get(block=True, timeout=0.1)
                    left_rgb_info = left_rgb_data[0]
                    left_rgb_image = left_rgb_data[1]
                    self.left_rgb_sequence_deque.append(left_rgb_info['ImageSequence'])
                    self.left_rgb_info_deque.append(left_rgb_info)
                    self.left_rgb_image_deque.append(left_rgb_image)
                if not self.output_right_rgb_queue.empty():
                    right_rgb_data = self.output_right_rgb_queue.get(block=True, timeout=0.1)
                    right_rgb_info = right_rgb_data[0]
                    right_rgb_image = right_rgb_data[1]
                    self.right_rgb_sequence_deque.append(right_rgb_info['ImageSequence'])
                    self.right_rgb_info_deque.append(right_rgb_info)
                    self.right_rgb_image_deque.append(right_rgb_image)
            else:
                self.depth_sequence_deque.clear()
                self.depth_info_deque.clear()
                self.depth_image_deque.clear()
                self.left_rgb_sequence_deque.clear()
                self.left_rgb_info_deque.clear()
                self.left_rgb_image_deque.clear()
                self.right_rgb_sequence_deque.clear()
                self.right_rgb_info_deque.clear()
                self.right_rgb_image_deque.clear()
            time.sleep(0.02)

    def get_snap_image(self):
        sequence_deque_list = [self.depth_sequence_deque, self.left_rgb_sequence_deque,
                               self.right_rgb_sequence_deque]
        len_sequence_deque_list = [len(self.depth_sequence_deque), len(self.left_rgb_sequence_deque),
                                   len(self.right_rgb_sequence_deque)]
        snap_data = [None, None, None]
        inter_sequence_list = None
        for index, len_deque in enumerate(len_sequence_deque_list):
            if len_deque != 0:
                if inter_sequence_list is None:
                    inter_sequence_list = set(sequence_deque_list[index])
                else:
                    inter_sequence_list = inter_sequence_list.intersection(set(sequence_deque_list[index]))
        if inter_sequence_list is not None and len(inter_sequence_list):
            snap_sequence = max(list(inter_sequence_list))
        else:
            return None, None, None
        for index, len_deque in enumerate(len_sequence_deque_list):
            if len_deque == 0:
                snap_data[index] = None
            else:
                snap_index = sequence_deque_list[index].index(snap_sequence)
                if index == 0:
                    snap_data[index] = [self.depth_info_deque[snap_index], self.depth_image_deque[snap_index]]
                elif index == 1:
                    snap_data[index] = [self.left_rgb_info_deque[snap_index], self.left_rgb_image_deque[snap_index]]
                elif index == 2:
                    snap_data[index] = [self.right_rgb_info_deque[snap_index], self.right_rgb_image_deque[snap_index]]
        return snap_data[0], snap_data[1], snap_data[2]
    
    def pause_frame(self):
        self.accept_data = not self.accept_data


def init_vsm_player_client():
    input_depth_queue = multiprocessing.Queue(maxsize=100)
    input_left_rgb_queue = multiprocessing.Queue(maxsize=100)
    input_right_rgb_queue = multiprocessing.Queue(maxsize=100)

    output_depth_queue = multiprocessing.Queue(maxsize=100)
    output_left_rgb_queue = multiprocessing.Queue(maxsize=100)
    output_right_rgb_queue = multiprocessing.Queue(maxsize=100)

    output_queue_list = [output_depth_queue, output_left_rgb_queue, output_right_rgb_queue]

    receive_data_client = Receive_data_client(1)
    parse_client = ParseImageData(1, receive_data_client, input_depth_queue, input_left_rgb_queue, input_right_rgb_queue)
    get_depth_image_client = ParseImageData2Image_Process(input_depth_queue, output_depth_queue, 'depth')
    get_left_rgb_image_client = ParseImageData2Image_Process(input_left_rgb_queue, output_left_rgb_queue, 'l_yuv')
    get_right_rgb_image_client = ParseImageData2Image_Process(input_right_rgb_queue, output_right_rgb_queue, 'r_yuv')
    parse_image = ParseImage(output_queue_list)

    receive_data_client.start()
    parse_client.start()
    get_depth_image_client.start()
    get_left_rgb_image_client.start()
    get_right_rgb_image_client.start()
    parse_image.start()


    return receive_data_client, parse_client, get_depth_image_client, get_left_rgb_image_client, get_right_rgb_image_client, parse_image
