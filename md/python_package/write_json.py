import json


def write_json():

    vpm_config = {
        'vendor_name': 'Magicdepth',
        'server_addr': '192.168.1.19',
        'do_connect_em_server': '0',
        'em_server_addr': '192.168.1.86',
        'nfs_server_ip_address': '192.168.1.89',
        'socket_addr1': '192.168.1.102',
        'socket_addr2': '192.168.1.100',
        # data_collecter_type
        # exit_when_load_failed
        # start_time
        # end_time

    }
    
    # mode='a'是追加
    with open('vpm_config.json', mode='w', encoding='utf-8') as js:
        # indent参数指定json字典换行缩进
        json.dump(vpm_config, js, indent=1)
        js.write('\n')
            
    
if __name__ == '__main__':
    write_json()