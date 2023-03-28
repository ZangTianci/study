cp ./axis_640x480_240x320.yml /system/etc
cp ./cpufreq.sh /system/bin
chmod +x /system/bin/cpufreq.sh

mkdir /data/vsm
mkdir /data/vsm/cali
cp ./default_video_stereo_server_configuration.xml /data/vsm/cali
cp ./libcatch_crash.so /data/vsm/cali
cp ./libimage_capture.so /data/vsm/cali
cp ./libnetworkserviceV2.so /data/vsm/cali
cp ./libRGBLed.so /data/vsm/cali
cp ./libsgm.so /data/vsm/cali
cp ./libsvpc_log.so /data/vsm/cali
cp ./libvsm_V2.so /data/vsm/cali
cp ./user_video_stereo_server_configuration.xml /data/vsm/cali
cp ./video_stereo_server_V2 /data/vsm/cali
chmod +x /data/vsm/cali/video_stereo_server_V2
