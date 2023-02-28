import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import vsm_player_client
import cv2
import time
import numpy as np
import calib
import getmac
import request_server


class GUISnap(QWidget):
    calib_info = pyqtSignal(str, list, int, str, str, str)

    def __init__(self):
        super().__init__()
        self.cwd = os.getcwd()
        
        empty_pic = np.zeros([480, 640, 3], dtype=np.uint8)
        self.empty_pic = cv2.putText(empty_pic.copy(), "No Signal", (240, 225),
                                     cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 2)
        self.unavailable_pic = cv2.putText(empty_pic.copy(), "Unavailable", (240, 225),
                                           cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 2)
        
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.logic_detect)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.draw_pic)
        self.timer2.start(50)

        self.init_UI()
        self.init_widget()
        self.init_vsmvideo()
        self.init_layout()

        self.auto_detect_flag = False
        # 0:L 1:R 2:S
        self.snap_stereo_flag = 2
        # 0:check 1:calib
        self.layout_flag = 0

        self.enable_calib_btn_flag = False
        self.chessBoardShape = [
            int(x) for x in self.chessBoardShape_line.currentText().split("*")]

        self.chessBoardShape = [8, 11]
        self.gridSize = 45
        self.vsm_type = None
        self.sub_vsm_type = None
        self.closeFlag = False
        self.server_init_Flag = False
        self.depth_data, self.left_rgb_data, self.right_rgb_data = None, None, None
        
    def init_server(self):
        self.server_init_Flag = True
        self.receive_data_client, \
            self.parse_client, \
            self.get_depth_image_client, \
            self.get_left_rgb_image_client, \
            self.get_right_rgb_image_client, \
            self.parse_image = vsm_player_client.init_vsm_player_client()
        self.timer1.start(10)


    def init_UI(self):
        self.setWindowTitle('MagicDepth Calibrator')
        self._center()

    def init_widget(self):
        file_path = os.path.dirname(__file__)

        self.ip_line = QLabel('IP:')
        self.ip = QLineEdit('192.168.1.203')
        self.ip.setFixedWidth(125)

        self.connect_vsm = self._btn("connect", self.start_video, True)
        self.disconnect_vsm = self._btn("disconnect", self.stop_video, True)
        self.connect_status = QLabel('◉')
        self.connect_status.setStyleSheet("color:red")
        self.save_path_discription = QLabel('Save Path:')

        self.save_path = QLineEdit(file_path)
        self.save_path.setReadOnly(True)
        self.save_path.setFixedWidth(600)
        self.pic_save_path = self._btn("...", self.choose_savepic, True)

        self.vsm_type_discription = QLabel('VSM Type:')
        self.vsm_type_line = QLabel('')
        self.vsm_type_line.setFixedWidth(100)
        self.check_vsm_type = self._btn("check", self.check_vsm, False)

        self.chessBoardShape_discription = QLabel('ChessBoard Shape:')
        self.chessBoardShape_line = self._combo_box(
            ["8*11", "6*9"], self.get_chessBoardShape)

        self.gridSize_discription = QLabel('Grid Size:')
        self.gridSize_line = self._combo_box(["45", "75"], self.get_gridSize)

        self.mode_calib_L = self._radio_btn('L', False)
        self.mode_calib_R = self._radio_btn('R', False)
        self.mode_calib_S = self._radio_btn('S', True)
        self.mode_calib_check = self._radio_btn('Check', False)

        self.mode_calib = QButtonGroup(self)
        self.mode_calib.addButton(self.mode_calib_L, 0)
        self.mode_calib.addButton(self.mode_calib_R, 1)
        self.mode_calib.addButton(self.mode_calib_S, 2)
        self.mode_calib.addButton(self.mode_calib_check, 3)
        self.mode_calib.buttonClicked.connect(self.changeMode)
        self.layout_discription = QLabel('Layout:')
        self.layout_normal = self._radio_btn('normal', True)
        self.layout_calib = self._radio_btn('calib', False)

        self.layout_mode = QButtonGroup(self)
        self.layout_mode.addButton(self.layout_normal, 0)
        self.layout_mode.addButton(self.layout_calib, 1)
        self.layout_mode.buttonClicked.connect(self.changeLayout)

        self.snap = self._btn("snap", self.snap_pic, False)

        self.sum_L = QLabel("0/10")
        self.sum_R = QLabel("0/10")
        self.sum_S = QLabel("0/10")
        self.sum_check = QLabel("0/1")

        self.calib = self._btn("calib", self.calib_trigger, False)

    def get_chessBoardShape(self):
        self.vsm_type_line.setText("")
        self.chessBoardShape = [
            int(x) for x in self.chessBoardShape_line.currentText().split("*")]

    def get_gridSize(self):
        self.gridSize = int(self.gridSize_line.currentText())

    def changeMode(self,):
        self.snap_stereo_flag = self.mode_calib.checkedId()

    def changeLayout(self,):
        self.layout_flag = self.layout_mode.checkedId()
        if self.layout_flag == 1:
            self.pic_depth.setVisible(False)
        else:
            self.pic_depth.setVisible(True)
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        self._center()

    def enable_calib_btn(self, enable: bool):
        if self.enable_calib_btn_flag != enable:
            self.enable_calib_btn_flag = enable
            self.chessBoardShape_line.setEnabled(enable)
            self.gridSize_line.setEnabled(enable)
            self.mode_calib_L.setEnabled(enable)
            self.mode_calib_R.setEnabled(enable)
            self.mode_calib_S.setEnabled(enable)
            self.mode_calib_check.setEnabled(enable)
            self.check_vsm_type.setEnabled(enable)

    def init_layout(self):
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h1_layout.addWidget(self.pic_left)
        self.h1_layout.addWidget(self.pic_right)
        self.h1_layout.addWidget(self.pic_depth)
        
        self.h2_layout.addWidget(self.save_path_discription)
        self.h2_layout.addWidget(self.save_path)
        self.h2_layout.addWidget(self.pic_save_path)

        self.h2_layout.addWidget(self.ip_line)
        self.h2_layout.addWidget(self.ip)
        self.h2_layout.addWidget(self.connect_vsm)
        self.h2_layout.addWidget(self.disconnect_vsm)
        self.h2_layout.addWidget(self.connect_status)
        self.h2_layout.addWidget(self.layout_discription)
        self.h2_layout.addWidget(self.layout_normal)
        self.h2_layout.addWidget(self.layout_calib)

        self.h2_layout.addStretch(1)

        self.h3_layout.addWidget(self.chessBoardShape_discription)
        self.h3_layout.addWidget(self.chessBoardShape_line)
        self.h3_layout.addWidget(self.gridSize_discription)
        self.h3_layout.addWidget(self.gridSize_line)
        self.h3_layout.addWidget(self.vsm_type_discription)
        self.h3_layout.addWidget(self.vsm_type_line)
        self.h3_layout.addWidget(self.check_vsm_type)
        self.h3_layout.addWidget(self.mode_calib_L)
        self.h3_layout.addWidget(self.sum_L)
        self.h3_layout.addWidget(self.mode_calib_R)
        self.h3_layout.addWidget(self.sum_R)
        self.h3_layout.addWidget(self.mode_calib_S)
        self.h3_layout.addWidget(self.sum_S)
        self.h3_layout.addWidget(self.mode_calib_check)
        self.h3_layout.addWidget(self.sum_check)

        self.h3_layout.addWidget(self.snap)
        self.h3_layout.addWidget(self.calib)
        self.h3_layout.addStretch(1)

        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.addLayout(self.h3_layout)
        self.setLayout(self.v_layout)

    def _combo_box(self, items, fun):
        combo_box = QComboBox()
        combo_box.setFixedWidth(80)
        combo_box.addItems(items)
        combo_box.setEnabled(False)
        combo_box.currentIndexChanged.connect(fun)
        return combo_box

    def _radio_btn(self, discription, setChecked):
        radio_btn = QRadioButton(discription, self)
        radio_btn.setChecked(setChecked)
        radio_btn.setEnabled(False)
        return radio_btn

    def _btn(self, discription, fun, enable):
        btn = QPushButton(discription)
        btn.clicked.connect(fun)
        btn.setEnabled(enable)
        return btn

    def init_vsmvideo(self):
        self.pic_left = QLabel()
        self.pic_right = QLabel()
        self.pic_depth = QLabel()

        self.pic_left.setFixedSize(640, 480)
        self.pic_left.setScaledContents(True)
        self.pic_left.setStyleSheet("border: 2px solid black")

        self.pic_right.setFixedSize(640, 480)
        self.pic_right.setScaledContents(True)
        self.pic_right.setStyleSheet("border: 2px solid black")

        self.pic_depth.setFixedSize(640, 480)
        self.pic_depth.setScaledContents(True)
        self.pic_depth.setStyleSheet("border: 2px solid black")

    def start_video(self):
        if not self.server_init_Flag:
            self.init_server()
        self.receive_data_client.connect_vsm_failed=False
        self.connectvsm_flag=0
        self.connectvsm_failed=0
        self.dataquene_warning=0
        g = getmac.IP2MAC()
        mac = g.getMac(self.ip.text())
        self.filename = self.ip.text()+'_'+mac
        self.path = os.path.join(self.save_path.text(), self.filename)

        self.receive_data_client.pasue_flag = True
        if self.receive_data_client.connection_status:
            self.receive_data_client.close_connect()
        server_info = (self.ip.text(), 3513)
        self.receive_data_client.set_server_info(server_info)
        self.receive_data_client.pasue_flag = False
        print(self.receive_data_client.connect_vsm)

        
    def stop_video(self):
        if self.server_init_Flag:
            self.receive_data_client.pasue_flag = True
            if self.receive_data_client.connection_status:
                self.receive_data_client.close_connect()
            self.receive_data_client.clear_server_info()

    def choose_savepic(self):
        self.dir_choose = QFileDialog.getExistingDirectory(
            self, "选取文件夹", self.cwd)  # 起始路径
        if self.dir_choose == "":
            return
        else:
            self.save_path.setText(str(self.dir_choose))
            self.cwd = self.dir_choose
            self.vsm_type_line.setText("")

    def snap_pic(self):
        if self.layout_flag==1:
            if self.auto_detect_flag:
                path = os.path.join(self.path, "detect")
            else:
                if self.snap_stereo_flag == 0 or self.snap_stereo_flag == 1:
                    path = os.path.join(self.path, "calib")
                elif self.snap_stereo_flag == 2:
                    path = os.path.join(self.path, "calib", "S")
                else:
                    path = os.path.join(self.path, "check")
        else:
            path = os.path.join(self.path, "snap")

        l_path = os.path.join(path, "L")
        r_path = os.path.join(path, "R")
        d_path = os.path.join(path, "D")
        if self.auto_detect_flag or self.snap_stereo_flag==3:
            shutil.rmtree(l_path, ignore_errors=True)
            shutil.rmtree(r_path, ignore_errors=True)

        os.makedirs(l_path, exist_ok=True)
        os.makedirs(r_path, exist_ok=True)
        if self.layout_flag==0:
            os.makedirs(d_path, exist_ok=True)
        if self.depth_data is not None:
            depth_image = self.depth_data[1]
        else:
            depth_image = self.unavailable_pic
        if self.left_rgb_data is not None:
            left_rgb_image = self.left_rgb_data[1]
        else:
            left_rgb_image = self.unavailable_pic
        if self.right_rgb_data is not None:
            right_rgb_image = self.right_rgb_data[1]
        else:
            right_rgb_image = self.unavailable_pic
        
        save_time_stamp = int(time.time()*1000)
        if self.layout_flag==1:
            if self.snap_stereo_flag == 0:
                ret = calib.check_chessborad_single(
                    left_rgb_image, self.chessBoardShape)
                if ret is True:
                    print(f'检测到标定板, 保存left rgb图像')
                    # QMessageBox.information(self, 'Info',f"检测到标定板, 保存0摄像头图像")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"sl0") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return
                    left_rgb_image_path = os.path.join(
                        l_path, f'{save_time_stamp}_0.bmp')
                    cv2.imwrite(left_rgb_image_path, left_rgb_image)
                else:
                    print("未检测到标定板")
                    QMessageBox.information(self, 'Warning',f"未检测到标定板")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"sl1") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return

            elif self.snap_stereo_flag == 1:
                ret = calib.check_chessborad_single(
                    right_rgb_image, self.chessBoardShape)
                if ret is True:
                    print(f'检测到标定板, 保存right rgb图像')
                    # QMessageBox.information(self, 'Info',f"检测到标定板, 保存1摄像头图像")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"sr0") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return
                    right_rgb_image_path = os.path.join(
                        r_path, f'{save_time_stamp}_1.bmp')
                    cv2.imwrite(right_rgb_image_path, right_rgb_image)
                else:
                    print("未检测到标定板")
                    QMessageBox.information(self, 'Warning',f"未检测到标定板")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"sr1") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return

            elif self.snap_stereo_flag == 2:
                retL = calib.check_chessborad_single(
                    left_rgb_image, self.chessBoardShape)
                retR = calib.check_chessborad_single(
                    right_rgb_image, self.chessBoardShape)

                if retR is True and retL is True:
                    print(f'检测到标定板, 保存双目图像')
                    # QMessageBox.information(self, 'Info',f"检测到标定板, 保存双目摄像头图像")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"ss0") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return
                    left_rgb_image_path = os.path.join(
                        l_path, f'{save_time_stamp}_0.bmp')
                    right_rgb_image_path = os.path.join(
                        r_path, f'{save_time_stamp}_1.bmp')
                    cv2.imwrite(left_rgb_image_path, left_rgb_image)
                    cv2.imwrite(right_rgb_image_path, right_rgb_image)
                else:
                    print("未检测到标定板")
                    QMessageBox.information(self, 'Warning',f"未检测到标定板")
                    if request_server.request_server(com="MD",devid=self.filename,status=f"ss1") != 0:
                        QMessageBox.warning(self, 'Warning',"没有网络")
                        return
            elif self.snap_stereo_flag == 3:
                left_rgb_image_path = os.path.join(
                    l_path, f'{save_time_stamp}_0.bmp')
                right_rgb_image_path = os.path.join(
                    r_path, f'{save_time_stamp}_1.bmp')
                cv2.imwrite(left_rgb_image_path, left_rgb_image)
                cv2.imwrite(right_rgb_image_path, right_rgb_image)
                print(f'保存检测用图像')
                # QMessageBox.information(self, 'Info',f"保存检测用图像")
                if request_server.request_server(com="MD",devid=self.filename,status=f"sa") != 0:
                    QMessageBox.warning(self, 'Warning',"没有网络")
                    return

        else:
            left_rgb_image_path = os.path.join(
                l_path, f'{save_time_stamp}_0.bmp')
            right_rgb_image_path = os.path.join(
                r_path, f'{save_time_stamp}_1.bmp')
            depth_rgb_image_path = os.path.join(
                d_path, f'{save_time_stamp}_2.bmp')
            
            cv2.imwrite(left_rgb_image_path, left_rgb_image)
            cv2.imwrite(right_rgb_image_path, right_rgb_image)
            cv2.imwrite(depth_rgb_image_path, depth_image)


    def check_vsm(self):
        self.auto_detect_flag = True
        self.snap_pic()

        ret, vsm_type, sub_vsm_type = calib.auto_detect(
            self.path, self.chessBoardShape)
        if ret == 0:
            self.vsm_type_line.setText(f"{vsm_type}{sub_vsm_type}")
            # QMessageBox.information(self, 'Info',f"检测到设备型号{self.vsm_type_line.text()}")
            if request_server.request_server(com="MD",devid=self.filename,status=f"ad0_{self.vsm_type_line.text()}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
            self.vsm_type = vsm_type
            self.sub_vsm_type = sub_vsm_type
        else:
            self.vsm_type_line.setText(f"Unknown")
            # QMessageBox.information(self, 'Warning',f"未检测到设备型号")
            if request_server.request_server(com="MD",devid=self.filename,status=f"ad1") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return

        self.auto_detect_flag = False

    def logic_detect(self):
        if self.receive_data_client.connect_vsm:
            if self.connectvsm_flag==0:
                self.connectvsm_flag=self.connectvsm_flag+1
                self.disconnectvsm_flag=0
                # QMessageBox.information(self, 'Info',f"vsm连接成功")
                if request_server.request_server(com="MD",devid=self.filename,status=f"cv0") != 0:
                    QMessageBox.warning(self, 'Warning',"没有网络")
                    return
        if self.receive_data_client.disconnect_vsm:
            if self.disconnectvsm_flag==0:
                self.disconnectvsm_flag=self.disconnectvsm_flag+1
                # QMessageBox.information(self, 'Info',f"vsm连接关闭")
                if request_server.request_server(com="MD",devid=self.filename,status=f"dv0") != 0:
                    QMessageBox.warning(self, 'Warning',"没有网络")
                    return
        if self.receive_data_client.connect_vsm_failed:
            if self.connectvsm_failed==0:
                self.connectvsm_failed=self.connectvsm_failed+1
                QMessageBox.information(self, 'Info',f"vsm连接失败，请检查VSM连接与程序运行状态")
                if request_server.request_server(com="MD",devid=self.filename,status=f"cv1") != 0:
                    QMessageBox.warning(self, 'Warning',"没有网络")
                    return
        if self.receive_data_client.dataqueue_warning:
            if self.dataquene_warning==0:
                self.dataquene_warning=self.dataquene_warning+1
                # QMessageBox.information(self, 'Info',f"数据队列达到警戒线，请检查网络质量")
                if request_server.request_server(com="MD",devid=self.filename,status=f"cv2") != 0:
                    QMessageBox.warning(self, 'Warning',"没有网络")
                    return
        if self.receive_data_client.connection_status:
            self.connect_status.setStyleSheet("color:green")
            self.layout_normal.setEnabled(True)
            self.layout_calib.setEnabled(True)
            self.pic_save_path.setEnabled(False)
            self.ip.setEnabled(False)
            self.snap.setEnabled(True)
            if self.layout_flag == 1:
                self.enable_calib_btn(True)
                if self.snap_stereo_flag == 2:
                    self.check_vsm_type.setEnabled(True)
                else:
                    self.check_vsm_type.setEnabled(False)
            else:
                self.enable_calib_btn(False)
            self.depth_data, self.left_rgb_data, self.right_rgb_data = self.parse_image.get_snap_image()
            lsum, rsum, slsum, srsum, clsum, crsum = self.check_sum()
            self.sum_L.setText(f"{lsum}/10")
            if lsum < 10:
                self.sum_L.setStyleSheet("color:red")
            else:
                self.sum_L.setStyleSheet("color:green")

            self.sum_R.setText(f"{rsum}/10")
            if rsum < 10:
                self.sum_R.setStyleSheet("color:red")
            else:
                self.sum_R.setStyleSheet("color:green")

            self.sum_S.setText(f"{slsum}/10")
            if slsum < 10:
                self.sum_S.setStyleSheet("color:red")
            else:
                self.sum_S.setStyleSheet("color:green")
            self.sum_check.setText(f"{clsum}/1")
            if clsum < 1:
                self.sum_check.setStyleSheet("color:red")
            else:
                self.sum_check.setStyleSheet("color:green")

            self.parse_image.accept_data = True
            self.get_depth_image_client.accept_data = True
            self.get_left_rgb_image_client.accept_data = True
            self.get_right_rgb_image_client.accept_data = True
            self.parse_client.accept_data = True
            if lsum >= 10 and rsum >= 10 and slsum >= 10 and slsum == srsum and clsum==1 and clsum==crsum and self.vsm_type is not None and self.sub_vsm_type is not None:
                self.calib.setEnabled(True)
            else:
                self.calib.setEnabled(False)
        else:
            if self.receive_data_client.pasue_flag is True:
                self.connect_status.setStyleSheet("color:red")
            else:
                self.connect_status.setStyleSheet("color:yellow")
            if self.layout_normal.isEnabled():
                self.pic_save_path.setEnabled(True)
                self.ip.setEnabled(True)
                self.enable_calib_btn(False)
                self.layout_normal.setEnabled(False)
                self.layout_calib.setEnabled(False)
                self.parse_image.accept_data = False
                self.get_depth_image_client.accept_data = False
                self.get_left_rgb_image_client.accept_data = False
                self.get_right_rgb_image_client.accept_data = False
                self.parse_client.accept_data = False
            self.depth_data, self.left_rgb_data, self.right_rgb_data = None, None, None

    def draw_pic(self):
        if self.depth_data is not None:
            info_disp, show_disp = self.depth_data
            if show_disp is not None:
                show_disp = cv2.applyColorMap(show_disp*8, cv2.COLORMAP_JET)
                show_disp = cv2.cvtColor(show_disp, cv2.COLOR_BGR2RGB)
                if info_disp['ImageWidth'] / info_disp['ImageHeight'] < 1:
                    show_disp = cv2.rotate(
                        show_disp, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            show_disp = self.empty_pic

        temp_depthSrc = QImage(show_disp, show_disp.shape[1], show_disp.shape[0],
                               show_disp.shape[1] * 3, QImage.Format_RGB888)
        self.pic_depth.setPixmap(QPixmap.fromImage(temp_depthSrc))

        if self.snap_stereo_flag != 1:
            if self.left_rgb_data is not None:
                left_rgb_image = self.left_rgb_data[1]
                if left_rgb_image is not None:
                    show_left = left_rgb_image
                else:
                    show_left = self.empty_pic
            else:
                show_left = self.empty_pic
        else:
            show_left = self.unavailable_pic

        show_left = cv2.cvtColor(show_left, cv2.COLOR_BGR2RGB)
        temp_leftSrc = QImage(show_left[:], show_left.shape[1], show_left.shape[0], show_left.shape[1] * 3,
                              QImage.Format_RGB888)
        self.pic_left.setPixmap(QPixmap.fromImage(temp_leftSrc))

        if self.snap_stereo_flag != 0:
            if self.right_rgb_data is not None:
                right_rgb_image = self.right_rgb_data[1]
                if right_rgb_image is not None:
                    show_right = right_rgb_image
                else:
                    show_right = self.empty_pic
            else:
                show_right = self.empty_pic
        else:
            show_right = self.unavailable_pic

        show_right = cv2.cvtColor(show_right, cv2.COLOR_BGR2RGB)
        temp_rightSrc = QImage(show_right[:], show_right.shape[1], show_right.shape[0],
                               show_right.shape[1] * 3, QImage.Format_RGB888)
        self.pic_right.setPixmap(QPixmap.fromImage(temp_rightSrc))

    def check_sum(self):
        lsum, rsum, slsum, srsum, clsum, crsum = 0, 0, 0, 0, 0, 0
        if os.path.exists(os.path.join(self.path, "calib", "L")):
            lsum = len(os.listdir(os.path.join(self.path, "calib", "L")))
        if os.path.exists(os.path.join(self.path, "calib", "R")):
            rsum = len(os.listdir(os.path.join(self.path, "calib", "R")))
        if os.path.exists(os.path.join(self.path, "calib", "S", "L")):
            slsum = len(os.listdir(os.path.join(self.path, "calib", "S", "L")))
        if os.path.exists(os.path.join(self.path, "calib", "S", "R")):
            srsum = len(os.listdir(os.path.join(self.path, "calib", "S", "R")))
        if os.path.exists(os.path.join(self.path, "check", "L")):
            clsum = len(os.listdir(os.path.join(self.path, "check", "L")))
        if os.path.exists(os.path.join(self.path, "check", "R")):
            crsum = len(os.listdir(os.path.join(self.path, "check", "R")))
        return lsum, rsum, slsum, srsum, clsum, crsum

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def calib_trigger(self):
        self.receive_data_client.pasue_flag = True
        if self.receive_data_client.connection_status:
            self.receive_data_client.close_connect()
        self.receive_data_client.stop_flag = True
        self.parse_image.stop_flag=True
        self.get_depth_image_client.terminate()
        self.get_left_rgb_image_client.terminate()
        self.get_right_rgb_image_client.terminate()
        self.parse_client.stop_flag=True
        self.calib_info.emit(
            self.path,
            self.chessBoardShape,
            self.gridSize,
            self.vsm_type,
            self.sub_vsm_type,
            self.ip.text())

    def closeEvent(self, event):
        if self.closeFlag:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Warning',
                "exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()