echo "start installing..."

# vsm
echo "installing vsm program..."
cp ./vsm/default_video_stereo_daemon_configuration.xml /system/etc/
cp ./vsm/user_video_stereo_daemon_configuration.xml /system/etc/
cp ./vsm/video_stereo_daemon /system/bin/
chmod 777 /system/bin/video_stereo_daemon
cp ./vsm/cpufreq.sh /system/bin/
chmod 777 /system/bin/cpufreq.sh
mkdir /data/vsm
mkdir /data/vsm/vpm
mkdir /data/vsm/vpm/base
cp ./vsm/lib* /data/vsm/vpm/base
cp ./vsm/video_stereo_server_V2 /data/vsm/vpm/base
cp ./vsm/default_video_stereo_server_configuration.xml /data/vsm/vpm/base
cp ./vsm/user_video_stereo_server_configuration.xml /data/vsm/vpm/base
chmod 777 /data/vsm/vpm/base/video_stereo_server_V2
echo "finish vsm program installation"

# vsm_calibrate
echo "installing vsm_calibrate program..."
cp ./vsm_calibrate/axis_640x480_240x320.yml /system/etc
mkdir /data/vsm
mkdir /data/vsm/cali
cp ./vsm_calibrate/default_video_stereo_server_configuration.xml /data/vsm/cali
cp ./vsm_calibrate/libcatch_crash.so /data/vsm/cali
cp ./vsm_calibrate/libimage_capture.so /data/vsm/cali
cp ./vsm_calibrate/libnetworkserviceV2.so /data/vsm/cali
cp ./vsm_calibrate/libRGBLed.so /data/vsm/cali
cp ./vsm_calibrate/libsgm.so /data/vsm/cali
cp ./vsm_calibrate/libsvpc_log.so /data/vsm/cali
cp ./vsm_calibrate/libvsm_V2.so /data/vsm/cali
cp ./vsm_calibrate/user_video_stereo_server_configuration.xml /data/vsm/cali
cp ./vsm_calibrate/video_stereo_server_V2 /data/vsm/cali
chmod 777 /data/vsm/cali/video_stereo_server_V2
echo "finish vsm_calibrate program installation"

echo "finish all installation"
