'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-08 17:19:28
LastEditTime : 2022-07-13 11:29:39
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /vsm_player_client_calib/main.py
'''
import sys
import multiprocessing
from PyQt5.QtWidgets import QApplication
from GUIRectify import GUIRectify
from GUISnap import GUISnap
from GUICalib import GUICalib


class GUIController:
    def __init__(self):
        self.gui_snap = GUISnap()
        self.gui_snap.show()
        self.gui_snap.calib_info.connect(self.from_snap_gui_to_calib_gui)

    def from_snap_gui_to_calib_gui(self, path, chessBoardShape, gridSize, vsm_type, sub_vsm_type, ip):
        self.gui_calib = GUICalib(path, chessBoardShape, gridSize, vsm_type, sub_vsm_type, ip)
        self.gui_calib.confirm.connect(self.from_calib_gui_to_rectify_gui)
        self.gui_calib.show()
        self.gui_snap.hide()
        
        
    def from_calib_gui_to_rectify_gui(self, path, ip):
        self.gui_snap.closeFlag = True
        self.gui_calib.closeFlag = True
        self.gui_snap.close()
        self.gui_calib.close()
        
        self.gui_rectify = GUIRectify(path, ip)
        self.gui_rectify.show()


    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    controller = GUIController()
    sys.exit(app.exec_())
