'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-12 15:30:37
LastEditTime : 2022-10-05 17:23:51
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /calibrator/vsm_player_client_calib/GUICalib.py
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
import calib
import request_server
import shutil

class GUICalib(QWidget):
    confirm = pyqtSignal(str, str)
    def __init__(self,path,chessBoardShape,gridSize,vsm_type,sub_vsm_type,ip):
        super().__init__()
        self.path = path
        self.chessBoardShape = chessBoardShape
        self.gridSize = gridSize
        self.vsm_type = vsm_type
        self.sub_vsm_type = sub_vsm_type

        self.ip = ip
        self.init_UI()
        self.init_widget()
        self.init_layout()

        self.ret_calib_L = -1
        self.ret_calib_R = -1
        self.ret_calib_S = -1
        self.left_erms=0
        self.right_erms=0
        self.stereo_erms=0
        self.calibed = False
        self.closeFlag = False
        
    def run_calib(self):
        if self.calibed is False:
            left_intrinsic, left_discoeffs,self.left_erms = calib.mono_calib(self.path,self.chessBoardShape,self.gridSize,self.vsm_type,self.sub_vsm_type, "L", )
            if np.abs(left_intrinsic[0,0]-400)<50 and np.abs(left_intrinsic[0,0]-400)<50:
                if self.left_erms>2:
                    self.ret_calib_L = 1
                else:
                    self.ret_calib_L = 0
                    right_intrinsic, right_discoeffs, self.right_erms = calib.mono_calib(self.path,self.chessBoardShape,self.gridSize,self.vsm_type,self.sub_vsm_type, "R",)
                    if np.abs(right_intrinsic[0,0]-400)<50 and np.abs(right_intrinsic[0,0]-400)<50:
                        if self.right_erms>2:
                            self.ret_calib_R = 1
                        else:
                            self.ret_calib_R = 0
                        
                            rvec_1to2, tvec_1to2, self.stereo_erms = calib.stereo_calib(
                                self.path,self.chessBoardShape,self.gridSize, self.vsm_type, self.sub_vsm_type,left_intrinsic, right_intrinsic, left_discoeffs, right_discoeffs)
                            baseline = calib.get_baseline(tvec_1to2[0])
   
                            self.ret_calib_S = 0
                            calib.saveResult(self.path,left_intrinsic, right_intrinsic, left_discoeffs[0].T, right_discoeffs[0].T, rvec_1to2, tvec_1to2, baseline, self.vsm_type, self.sub_vsm_type)
                            # QMessageBox.information(self, 'Info',f"成功保存标定文件")
                            if request_server.request_server(com="MD",devid="dev001",status=f"scf0") != 0:
                                QMessageBox.warning(self, 'Warning',"没有网络")
                                return
                            self.confirm_btn.setText("confirm")
                            self.calibed = True
                        
                    else:
                        self.ret_calib_R = 2
                        self.confirm_btn.setEnabled(False)
            else:
                self.ret_calib_L = 2
                
            self.calib_status_detect()
        else:
            self.confirm.emit(self.path,self.ip)
            
    def change_calib_color(self,source, name, signal):
        if signal==0:
            source.setStyleSheet("color:green")      
        elif signal==1:
            self.confirm_btn.setEnabled(False)
            source.setStyleSheet("color:yellow") 
            shutil.rmtree(os.path.join(self.path,"calib", name), ignore_errors=True)
            os.makedirs(os.path.join(self.path,"calib", name), exist_ok=True)
            self.close()
        elif signal==2:
            self.confirm_btn.setEnabled(False)
            source.setStyleSheet("color:red")
            shutil.rmtree(os.path.join(self.path,"calib", name), ignore_errors=True)
            os.makedirs(os.path.join(self.path,"calib", name), exist_ok=True)
            self.close()
            


    def calib_status_detect(self):
        
        if self.ret_calib_L == 0:
            # QMessageBox.information(self, 'Info',f"正确标定0摄像头，重投影误差{self.left_erms:.3f}")
            if request_server.request_server(com="MD",devid="dev001",status=f"cl0_{self.left_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        elif self.ret_calib_L == 1:
            QMessageBox.information(self, 'Warning',f"0摄像头重投影误差{self.left_erms:.3f}过大，请重新拍摄")
            if request_server.request_server(com="MD",devid="dev001",status=f"cl1_{self.left_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        elif self.ret_calib_L == 2:
            QMessageBox.information(self, 'Warning',f"0摄像头焦距偏差过大")
            if request_server.request_server(com="MD",devid="dev001",status=f"cl2") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        if self.ret_calib_R == 0:
            # QMessageBox.information(self, 'Info',f"正确标定1摄像头，重投影误差{self.right_erms:.3f}")
            if request_server.request_server(com="MD",devid="dev001",status=f"cr0_{self.right_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        elif self.ret_calib_R == 1:
            QMessageBox.information(self, 'Warning',f"1摄像头重投影误差{self.right_erms:.3f}过大，请重新拍摄")
            if request_server.request_server(com="MD",devid="dev001",status=f"cr1_{self.right_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        elif self.ret_calib_R == 2:
            QMessageBox.information(self, 'Warning',f"1摄像头焦距偏差过大")
            if request_server.request_server(com="MD",devid="dev001",status=f"cr2") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        if self.ret_calib_S == 0:
            # QMessageBox.information(self, 'Info',f"正确标定双目摄像头，重投影误差{self.stereo_erms:.3f}")
            if request_server.request_server(com="MD",devid="dev001",status=f"cs0_{self.stereo_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        elif self.ret_calib_S == 1:
            QMessageBox.information(self, 'Warning',f"双目摄像头重投影误差{self.stereo_erms:.3f}过大，请重新拍摄")
            if request_server.request_server(com="MD",devid="dev001",status=f"cs1_{self.stereo_erms:.3f}") != 0:
                QMessageBox.warning(self, 'Warning',"没有网络")
                return
        self.L_error.setText(f"{self.left_erms:.3f} pixel")
        self.R_error.setText(f"{self.right_erms:.3f} pixel")
        self.S_error.setText(f"{self.stereo_erms:.3f} pixel")
        self.change_calib_color(self.L_calib_status, "L", self.ret_calib_L)
        self.change_calib_color(self.R_calib_status, "R", self.ret_calib_R)
        self.change_calib_color(self.S_calib_status, "S", self.ret_calib_S)


    def init_widget(self):
        self.L_calib_status = QLabel('◉')
        self.L_error_description = QLabel('L_calib_error')
        self.L_error = QLabel('0 pixel')
        
        self.R_calib_status = QLabel('◉')
        self.R_error_description = QLabel('R_calib_error')
        self.R_error = QLabel('0 pixel')
        
        self.S_calib_status = QLabel('◉')
        self.S_error_description = QLabel('S_calib_error')
        self.S_error = QLabel('0 pixel')
        
        
        self.confirm_btn = QPushButton("Start")
        self.confirm_btn.clicked.connect(self._btn_start)

    def init_layout(self):
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.h4_layout = QHBoxLayout()
        self.h1_layout.addWidget(self.L_calib_status)
        self.h1_layout.addWidget(self.L_error_description)
        self.h1_layout.addWidget(self.L_error)
        self.h2_layout.addWidget(self.R_calib_status)
        self.h2_layout.addWidget(self.R_error_description)
        self.h2_layout.addWidget(self.R_error)
        self.h3_layout.addWidget(self.S_calib_status)
        self.h3_layout.addWidget(self.S_error_description)
        self.h3_layout.addWidget(self.S_error)
        self.h4_layout.addWidget(self.confirm_btn)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.addLayout(self.h3_layout)
        self.v_layout.addLayout(self.h4_layout)
        self.setLayout(self.v_layout)

    def init_UI(self):
        self.setWindowTitle('MagicDepth Calibrator')
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def _btn_start(self):
        self.run_calib()

    def closeEvent(self, event):
        if self.closeFlag:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Warning',
                "exit?", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()