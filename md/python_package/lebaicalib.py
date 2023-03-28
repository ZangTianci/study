import math
import time
import json
import os

from lebai import LebaiRobot, CartesianPose, JointPose


class lebai_run():

    def __init__(self, robot_ip):
        self.robot_ip = robot_ip

    def ip(self):
        self.rb = LebaiRobot(self.robot_ip) # 使用时修改此处地址

    def start_system(self):
        self.rb.start_sys()
        time.sleep(5)

    def run(self, JP = [49/180*math.pi, 58/180*math.pi, (-152)/180*math.pi, (-83)/180*math.pi, (-89)/180*math.pi, (-2)/180*math.pi]):  
        self.rb.movej(JointPose(JP), 0, 0, 3, 0)
        base = self.rb.get_actual_tcp_pose()
        p2 = CartesianPose(0.1, 0, 0, 0, 0, 0, base=base)
        self.rb.movel(p2, 0, 0, 3, 0)

        self.rb.stop()
        time.sleep(2)

    def setvoice(self):
        self.rb.set_voice(0)

    def stop_system(self):
        self.rb.stop_sys()


class calib(lebai_run):
    def __init__(self, robot_ip):
        super().__init__(robot_ip)

    def read_posefile(self, filepath, filename):
        calib_pose_check = []
        filep = os.path.join(filepath, filename)
        with open(filep,"r") as file:
            dic = json.load(file)
            dic["source"] = json.loads(dic['source'])
            for a in range(0,61):
                a = "%02d" % a
                if "joint" in dic["source"]["timeline"][int(a)]["data"]:
                    # if "check" in dic["source"]["timeline"][int(a)]["name"]:
                    calib_pose_check.append(dic["source"]["timeline"][int(a)]["data"]["joint"])
        return calib_pose_check

    def calib(self, lbdname='vsm_a1_90.lbd'):
        self.ip()
        self.start_system()
        calib_pose = self.read_posefile(filepath='/media/ztc/Data/md_code/tools/operation_toolset/calib_robot/', filename=lbdname)
        # check
        for calibp in calib_pose:
            self.run(JP = calibp)
        self.stop_system()



if __name__ == '__main__':
    lebai_calib1 = calib("192.168.1.97")
    lebai_calib1.calib(lbdname='vsm_b3_150g.lbd')
    # lebai_calib1.read_posefile(filepath='/home/ztc/code/python_package/', filename='vsm_b1.lbd')
    