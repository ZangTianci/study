'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-12 17:08:09
LastEditTime : 2022-11-09 14:18:50
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /calibrator/vsm_player_client_calib/GUIRectify.py
'''
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import rectify
import os
import request_server

class GUIRectify(QWidget):
    def __init__(self,path,ip):
        super().__init__()
        self.path = path
        self.ip = ip
        self.rectify_instance = rectify.Rectiy(self.path, 150, 150, 160, 120, 0)
        
        img_L_name = os.listdir(os.path.join(self.path, "check", "L"))[0]
        img_R_name = os.listdir(os.path.join(self.path, "check", "R"))[0]
        self.img_L = cv2.imread(os.path.join(self.path, "check", "L", img_L_name))
        self.img_R = cv2.imread(os.path.join(self.path, "check", "R", img_R_name))
        if self.rectify_instance.vsm_type == "a":
            self.img_shape = [480,640]
            self.x_focal = 150
            self.y_focal = 150
            self.x_shift = 160
            self.y_shift = 120
            self.disparity_shift=0
        else:
            self.img_shape = [640,480]
            self.x_focal = 150
            self.y_focal = 150
            self.x_shift = 120
            self.y_shift = 160
            self.disparity_shift=0
        self.rectify_instance.update_map(self.x_focal,self.y_focal,self.x_shift,self.y_shift,self.disparity_shift)

        self.init_UI()
        self.init_widget()
        self.init_vsmvideo()
        self.init_layout()

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.draw_pic)
        self.timer2.start(1000)
        
    def init_vsmvideo(self):
        self.pic = QLabel()
        self.pic.setFixedSize(self.img_shape[1]*2, self.img_shape[0])
        self.pic.setScaledContents(True)
        self.pic.setStyleSheet("border: 2px solid black")

    def init_widget(self):

        self.ip_discription = QLabel('IP:')
        self.ip_line = QLabel(self.ip)
        self.ip_line.setFixedWidth(125)
        self.path_discription = QLabel('Path:')
        self.path_line = QLabel(self.path)

        self.x_focal_discription,self.x_focal_line = self._line('x_focal:',self.x_focal)
        self.y_focal_discription,self.y_focal_line = self._line('y_focal:',self.y_focal)
        self.x_shift_discription,self.x_shift_line = self._line('x_shift:',self.x_shift)
        self.y_shift_discription,self.y_shift_line = self._line('y_shift:',self.y_shift)
        self.disparity_shift_discription,self.disparity_shift_line = self._line('disparity_shift:',self.disparity_shift)
        self.save_btn = self._btn("Save",self.save,True)

    def save(self):
        
        self.save_btn.setEnabled(False)
        self.rectify_instance.save()
        # QMessageBox.information(self, 'Info',f"成功保存矫正文件")
        if request_server.request_server(com="MD",devid="dev001",status=f"srf0") != 0:
            QMessageBox.warning(self, 'Warning',"没有网络")
            return
        self.close()

    def _line(self,description,initial_val):
        line_discription = QLabel(description)
        line = QLineEdit(f"{initial_val}")
        line.setFixedWidth(40)
        line.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))
        return line_discription, line

    def _combo_box(self, items, fun):
        combo_box = QComboBox()
        combo_box.setFixedWidth(80)
        combo_box.addItems(items)
        combo_box.setEnabled(False)
        combo_box.currentIndexChanged.connect(fun)
        return combo_box

    def draw_pic(self):
        self.rectify_instance.update_map(
            int(self.x_focal_line.text()) if self.x_focal_line.text() != "" else 1,
            int(self.y_focal_line.text()) if self.y_focal_line.text() != "" else 1,
            int(self.x_shift_line.text()) if self.x_shift_line.text() != "" else 1,
            int(self.y_shift_line.text()) if self.y_shift_line.text() != "" else 1,
            int(self.disparity_shift_line.text()) if self.disparity_shift_line.text() != "" else 0
            )
        show_left, show_right = self.rectify_instance.remap(self.img_L, self.img_R)
        rst=cv2.hconcat([show_left, show_right])
        for m in range(0, rst.shape[0], 20):
            rst = cv2.line(rst, (0, m), (rst.shape[1], m), (0, 0, 255), 1)

        show_src = cv2.cvtColor(rst, cv2.COLOR_BGR2RGB)
        temp_Src = QImage(show_src[:], show_src.shape[1], show_src.shape[0], show_src.shape[1] * 3,
                              QImage.Format_RGB888)
        self.pic.setPixmap(QPixmap.fromImage(temp_Src))

    def init_layout(self):
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h1_layout.addWidget(self.pic)

        self.h2_layout.addWidget(self.ip_discription)
        self.h2_layout.addWidget(self.ip_line)
        self.h2_layout.addWidget(self.path_discription)
        self.h2_layout.addWidget(self.path_line)
        
        self.h2_layout.addStretch(1)

        self.h3_layout.addWidget(self.x_focal_discription)
        self.h3_layout.addWidget(self.x_focal_line)
        self.h3_layout.addWidget(self.y_focal_discription)
        self.h3_layout.addWidget(self.y_focal_line)
        self.h3_layout.addWidget(self.x_shift_discription)
        self.h3_layout.addWidget(self.x_shift_line)
        self.h3_layout.addWidget(self.y_shift_discription)
        self.h3_layout.addWidget(self.y_shift_line)
        self.h3_layout.addWidget(self.disparity_shift_discription)
        self.h3_layout.addWidget(self.disparity_shift_line)
        self.h3_layout.addWidget(self.save_btn)
        self.h3_layout.addStretch(1)

        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.addLayout(self.h3_layout)
        
        self.setLayout(self.v_layout)


    def init_UI(self):
        self.setWindowTitle('MagicDepth Calibrator')
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _btn(self, discription, fun, enable):
        btn = QPushButton(discription)
        btn.clicked.connect(fun)
        btn.setEnabled(enable)
        return btn
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning',
            "exit?", QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()