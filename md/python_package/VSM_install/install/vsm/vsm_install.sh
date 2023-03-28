echo start installing...

a=ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|busybox awk '{print $2}'|tr -d "addr:"

sed -i 's/192.168.1.12/a/' /vsm/user_video_stereo_server_configuration.xml

# cp ./axis.yml /system/etc/
cp ./default_video_stereo_daemon_configuration.xml /system/etc/
cp ./user_video_stereo_daemon_configuration.xml /system/etc/
cp ./video_stereo_daemon /system/bin/
chmod 777 /system/bin/video_stereo_daemon
cp ./cpufreq.sh /system/bin/
chmod 777 /system/bin/cpufreq.sh

mkdir /data/vsm
mkdir /data/vsm/vpm
mkdir /data/vsm/vpm/base
cp ./lib* /data/vsm/vpm/base
cp ./video_stereo_server_V2 /data/vsm/vpm/base
cp ./default_video_stereo_server_configuration.xml /data/vsm/vpm/base
cp ./user_video_stereo_server_configuration.xml /data/vsm/vpm/base
chmod 777 /data/vsm/vpm/base/video_stereo_server_V2

echo finish all installation
