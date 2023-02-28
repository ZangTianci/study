'''
Author       : JiaYu.Wu
PersonalEmail: a472796892@gmail.com
OfficeEmail  : jiayu.wu@magicdepth.com
Company      : Magic Depth
Date         : 2022-07-08 17:19:28
LastEditTime : 2022-12-17 11:09:49
LastEditors  : JiaYu.Wu
Description  : #*  *#
FilePath     : /vsm_player_client_calib/mainRectify.py
'''
import sys
import argparse
from PyQt5.QtWidgets import QApplication
from GUIRectify import GUIRectify


class GUIController:
    def __init__(self, path):
        self.gui_rectify = GUIRectify(path, "None")
        self.gui_rectify.show()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    args, _ = parser.parse_known_args()
    app = QApplication(sys.argv)
    controller = GUIController(args.path)
    sys.exit(app.exec_())
