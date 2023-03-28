import json
import re
import os

# duqu
def readjson_vpm():

    # mode='a'是追加
    with open('vsm_config.json', mode='r', encoding='utf-8') as js:
        # indent参数指定json字典换行缩进
        vpmjs = json.load(js)
        return vpmjs

def ch_dict():

    vpmjs = readjson_vpm()
    vpmconfig = {
        'name=server_addr': '        <record name=server_addr type=string value=192.168.1.204></record>\n',
        'name=work_mode': '      <record name=work_mode type=integer value=0></record>\n',
        'name=image_set_point': '        <record name=image_set_point type=double value=120.0></record>\n'

    }

    # vsm ip
    server_addr = vpmconfig['name=server_addr']
    server_addr = server_addr[:-13] + (vpmjs['name=server_addr'].split('.'))[3] + server_addr[-11:]
    vpmconfig['name=server_addr'] = server_addr

    em_server_addr = vpmconfig['name=em_server_addr']
    em_server_addr = em_server_addr[:-13] + (vpmjs['name=em_server_addr'].split('.'))[3] + em_server_addr[-11:]
    vpmconfig['name=em_server_addr'] = em_server_addr

    nfs_server_ip_address = vpmconfig['name=nfs_server_ip_address']
    nfs_server_ip_address = nfs_server_ip_address[:-13] + (vpmjs['name=nfs_server_ip_address'].split('.'))[3] + nfs_server_ip_address[-11:]
    vpmconfig['name=nfs_server_ip_address'] = nfs_server_ip_address

    socket_addr1 = vpmconfig['name=socket_addr1']
    socket_addr1 = socket_addr1[:-13] + (vpmjs['name=socket_addr1'].split('.'))[3] + socket_addr1[-11:]
    vpmconfig['name=socket_addr1'] = socket_addr1

    socket_addr2 = vpmconfig['name=socket_addr2']
    socket_addr2 = socket_addr2[:-13] + (vpmjs['name=socket_addr2'].split('.'))[3] + socket_addr2[-11:]
    vpmconfig['name=socket_addr2'] = socket_addr2

    return vpmconfig

def rw_file(path='/home/ztc/code/python_package/', file='user_vision_processing_server.xml'):

    vpmconfig = ch_dict()

    with open(os.path.join(path, 'user_vision_processing_server_configuration.xml'), 'r') as xr:
        line = xr.readlines()

    with open(os.path.join(path, file), 'w') as xw:
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

      
if __name__ == '__main__':

    rw_file()
