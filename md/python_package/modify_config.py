import json
import os

# 通过读取json修改xml配置
class modify_config:

    def __init__(self, json_path, json_file, xml_path, xml_file):
        self.json_path = json_path
        self.json_file = json_file
        self.xml_path = xml_path
        self.xml_file = xml_file

    # 读json文件
    def readjson(json_path='', json_file=''):

        # mode='a'是追加
        with open(os.path.join(json_path, json_file), mode='r', encoding='utf-8') as js:
            # indent参数指定json字典换行缩进
            config = json.load(js)
            return config

    # 推送配置文件到vsm上
    def adb_push_config(xml_path='', xml_file='', ip=''):
        # os.system(f'adb disconnect')
        # os.system(f'adb connect {ip}')
        vsmconfig = os.path.join(xml_path, xml_file)
        os.system(f'adb push {vsmconfig} /data/vsm/vpm/base')
        # os.system(f'adb reboot')

# 修改vpm配置文件
class modify_vpm_config(modify_config):

    def __init__(self, json_path, json_file, xml_path, xml_file):

        super().__init__(json_path, json_file, xml_path, xml_file)
        self.vpmconfig = {
            'name=vendor_name': '      <record name=vendor_name type=string value=Magicdepth></record>\n',
            'name=server_addr': '        <record name=server_addr type=string value=192.168.1.16></record>\n',
            'name=em_server_addr': '        <record name=em_server_addr type=string value=192.168.1.80></record>\n',
            'name=nfs_server_ip_address': '        <record name=nfs_server_ip_address type=string value=192.168.1.80></record>\n',
            'name=socket_addr1': '        <record name=socket_addr type=string value=192.168.1.10></record>\n',
            'name=socket_addr2': '        <record name=socket_addr type=string value=192.168.1.10></record>\n'
        }


    def ch_vpm_dict(self):

        vpmjs = modify_config.readjson(self.json_path, self.json_file)
        # vpm ip
        vpmconfig = self.vpmconfig
        server_addr = vpmconfig['name=server_addr']
        server_addr = server_addr.split('.')[0] + '.' + vpmjs['name=server_addr'].split('.')[1] + '.' + vpmjs['name=server_addr'].split('.')[2] + '.' + vpmjs['name=server_addr'].split('.')[3] + server_addr[-11:]
        vpmconfig['name=server_addr'] = server_addr

        em_server_addr = vpmconfig['name=em_server_addr']
        em_server_addr = em_server_addr.split('.')[0] + '.' + vpmjs['name=em_server_addr'].split('.')[1] + '.' + vpmjs['name=em_server_addr'].split('.')[2] + '.' + vpmjs['name=em_server_addr'].split('.')[3] + em_server_addr[-11:]
        vpmconfig['name=em_server_addr'] = em_server_addr

        nfs_server_ip_address = vpmconfig['name=nfs_server_ip_address']
        nfs_server_ip_address = nfs_server_ip_address[:-13] + (vpmjs['name=nfs_server_ip_address'].split('.'))[3] + nfs_server_ip_address[-11:]
        vpmconfig['name=nfs_server_ip_address'] = nfs_server_ip_address

        socket_addr1 = vpmconfig['name=socket_addr1']
        socket_addr1 = socket_addr1.split('.')[0] + '.' + vpmjs['name=socket_addr1'].split('.')[1] + '.' + vpmjs['name=socket_addr1'].split('.')[2] + '.' + vpmjs['name=socket_addr1'].split('.')[3] + socket_addr1[-11:]
        vpmconfig['name=socket_addr1'] = socket_addr1

        socket_addr2 = vpmconfig['name=socket_addr2']
        socket_addr2 = socket_addr2.split('.')[0] + '.' + vpmjs['name=socket_addr2'].split('.')[1] + '.' + vpmjs['name=socket_addr2'].split('.')[2] + '.' + vpmjs['name=socket_addr2'].split('.')[3] + socket_addr2[-11:]
        vpmconfig['name=socket_addr2'] = socket_addr2

        return vpmconfig

    def rw_vpm_file(self):

        vpmconfig = self.ch_vpm_dict()
        with open(os.path.join(self.xml_path, self.xml_file), 'r') as xr:
            line = xr.readlines()

        with open(os.path.join(self.xml_path, self.xml_file), 'w') as xw:
            vsm = 0
            for l in line:
                for key in vpmconfig:
                    if 'name=socket_addr' in l:
                        if vsm == 0:
                            l = vpmconfig['name=socket_addr1']
                            vsm += 1
                            break
                        elif vsm == 1:
                            l = vpmconfig['name=socket_addr2']
                            vsm += 1
                    elif key in l:
                        l = vpmconfig[key]     
                xw.write(l)

# 修改vsm配置文件
class modify_vsm_config(modify_config):

    def __init__(self, json_path, json_file, xml_path, xml_file):

        super().__init__(json_path, json_file, xml_path, xml_file)
        self.vsmconfig = {
            'name=server_addr': '        <record name=server_addr type=string value=192.168.1.204></record>\n',
            'name=work_mode': '      <record name=work_mode type=integer value=0></record>\n',
            'name=image_set_point': '        <record name=image_set_point type=double value=120.0></record>\n'
        }

    def ch_vsm_dict(self):

        self.vsmcfg = modify_config.readjson(self.json_path, self.json_file)
        vsmjs = self.vsmcfg
        vsmconfig = self.vsmconfig
        # vpm ip
        server_addr = vsmconfig['name=server_addr']
        server_addr = server_addr.split('.')[0] + '.' + vsmjs['name=server_addr'].split('.')[1] + '.' + vsmjs['name=server_addr'].split('.')[2] + '.' + vsmjs['name=server_addr'].split('.')[3] + server_addr[-11:]
        vsmconfig['name=server_addr'] = server_addr

        work_mode = vsmconfig['name=work_mode']
        work_mode = work_mode[:-12] + vsmjs['name=work_mode'] + work_mode[-11:]
        vsmconfig['name=work_mode'] = work_mode

        image_set_point = vsmconfig['name=image_set_point']
        image_set_point = image_set_point[:-16] + vsmjs['name=image_set_point'] + image_set_point[-11:]
        vsmconfig['name=image_set_point'] = image_set_point

        return vsmconfig

    def rw_vsm_file(self, push=0):

        vsmconfig = self.ch_vsm_dict()
        with open(os.path.join(self.xml_path, self.xml_file), 'r') as xr:
            line = xr.readlines()

        with open(os.path.join(self.xml_path, self.xml_file), 'w') as xw:
            for l in line:
                for key in vsmconfig:
                    if key in l:
                        l = vsmconfig[key]     
                xw.write(l)
        
        if push == 1:
            modify_config.adb_push_config(xml_path=self.xml_path, xml_file=self.xml_file, ip=self.vsmcfg['name=server_addr'])

              
if __name__ == '__main__':

    # 实例化修改vpm配置
    modify_vpm_config1 = modify_vpm_config(
        json_path = '/home/ztc/code/python_package/',
        json_file = 'vpm_config.json',
        xml_path = '/home/ztc/code/python_package/',
        xml_file = 'user_vision_processing_server_configuration.xml'
        )
    modify_vpm_config1.rw_vpm_file()
    
    # 实例化修改vsm配置
    # modify_vsm_config1 = modify_vsm_config(
    #     json_path = '/home/ztc/code/python_package/',
    #     json_file = 'vsm_config.json',
    #     xml_path = '/home/ztc/code/python_package/',
    #     xml_file = 'user_video_stereo_server_configuration.xml'
    #     )
    # modify_vsm_config1.rw_vsm_file(push = 1)

