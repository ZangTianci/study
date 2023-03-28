import modify_config
import os

class initialize_vsm:

    def __init__(self, initialize_path):
        
        self.initialize_path = initialize_path
        self.app_path = os.path.join(initialize_path, 'app')
        self.exposure_path = os.path.join(initialize_path, 'exposure')
        self.deamon_path = os.path.join(initialize_path, 'deamon')
        self.calib_path = os.path.join(initialize_path, 'calib_temp')
        self.slowdown_freq = os.path.join(initialize_path, 'slowdown_freq')

    def connect_vsm(self):

        vsmconfig = modify_config.modify_config.readjson(json_path=self.initialize_path, json_file='vsm_config.json')
        vsmip = vsmconfig['name=server_addr']
        os.system(f'adb disconnect')
        os.system(f'adb connect {vsmip}')

    def install(self):

        os.system(f'adb push {self.initialize_path}/VSM_install/* /data/')
        os.system(f'adb shell "chmod 777 /data/install/vsm_install.sh"')
        os.system(f'adb shell "cd /data/install && sh vsm_install.sh"')

    def update_app(self, baseline=150):
        
        apppath = os.path.join(self.app_path, str(baseline))
        modify_vsm_config1 = modify_config.modify_vsm_config(
        json_path = self.initialize_path,
        json_file = 'vsm_config.json',
        xml_path = apppath,
        xml_file = 'user_video_stereo_server_configuration.xml'
        )
        modify_vsm_config1.rw_vsm_file(push = 1)

        os.system(f'adb push {self.app_path}/{baseline}/* /data/vsm/vpm/base/')

    def update_axis(self):
        os.system(f'adb push {self.calib_path}/axis.yml /system/etc/')

    def update_deamon(self):

        os.system(f'adb push {self.deamon_path}/video_stereo_daemon /system/bin/')
        os.system(f'adb push {self.deamon_path}/user_video_stereo_daemon_configuration.xml /system/etc/')

    def update_exposure(self):

        os.system(f'adb push {self.exposure_path}/IMX214_lens_50013A7_OTP.xml /vendor/etc/')
        os.system(f'adb push {self.exposure_path}/libisp_isi_drv_IMX214.so /vendor/lib64/hw/')

        os.system(f"adb shell 'md5sum /vendor/etc/IMX214_lens_50013A7_OTP.xml'")
        os.system(f"adb shell 'md5sum /vendor/lib64/hw/libisp_isi_drv_IMX214.so'")

    def update_slowdown_freq(self):
        os.system(f'adb push {self.slowdown_freq}/* /system/bin/')
        os.system(f"adb shell 'chmod 777 /system/bin/cpufreq.sh'")
        os.system(f"adb shell 'chmod 777 /system/bin/setCPUFreq.sh'")
        os.system(f"adb shell 'chmod 777 /system/bin/watchsys.sh'")

    def reboot_vsm(self):
        os.system(f"adb shell 'sync'")
        os.system(f'adb reboot')


if __name__ == ('__main__'):

    # initialize vsm
    initialize_vsm1 = initialize_vsm('/media/ztc/Data/initialize_device/vsm')
    initialize_vsm1.connect_vsm()
    initialize_vsm1.install()
    initialize_vsm1.update_axis()
    initialize_vsm1.update_app(baseline='vsm_v2.0.2022092715')
    initialize_vsm1.update_deamon()
    initialize_vsm1.update_exposure()
    # initialize_vsm1.update_slowdown_freq()
    initialize_vsm1.reboot_vsm()
    