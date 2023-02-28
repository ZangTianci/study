'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-08 17:19:28
LastEditTime : 2022-12-17 10:43:03
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /vsm_player_client_calib/mainCalibRectify.py
'''
import sys
import argparse
from PyQt5.QtWidgets import QApplication
from GUIRectify import GUIRectify
from GUICalib import GUICalib


class GUIController:
    def __init__(self, path, chessBoardShape, gridSize, vsm_type, sub_vsm_type):
        
        self.gui_calib = GUICalib(path, chessBoardShape, gridSize, vsm_type, sub_vsm_type, "None")
        self.gui_calib.confirm.connect(self.from_calib_gui_to_rectify_gui)
        self.gui_calib.show()
        
        
    def from_calib_gui_to_rectify_gui(self, path, ip):
        self.gui_calib.closeFlag = True
        self.gui_calib.close()
        
        self.gui_rectify = GUIRectify(path, ip)
        self.gui_rectify.show()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    parser.add_argument('--gridSize', type=int)
    parser.add_argument('--chessBoardShape', nargs="+", type=int)
    parser.add_argument('--vsm_type', type=str)
    parser.add_argument('--sub_vsm_type', type=str)
    args, _ = parser.parse_known_args()
    app = QApplication(sys.argv)
    controller = GUIController(args.path,args.chessBoardShape,args.gridSize,args.vsm_type,args.sub_vsm_type)
    sys.exit(app.exec_())
