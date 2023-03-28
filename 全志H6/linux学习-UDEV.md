`UDEV`通过侦听内核发出来的信息（时间）管理/dev目录下的设备文件\
运行在应用空间\
根据系统硬件设备状态，创建文件等



配置文件,以支持USB设备的热拔插,支持UDEV的机制\
在/etc/udev/rules.d 文件夹下创建规则文件\

cd /etc/udev/rules.d/
sudo vim 51-android.rules

在文件中添加内容 SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666"




linux一切设备皆文件

dmesg打印内核信息


## daemon
守护进程，周期性地执行某种任务或等待处理某些发生的事件。在后台运行。守护进程的父进程是init进程
```shell
ps -elf
ps -ef|grep hello |grep -v grep
# 忽略grep
```
cmd列名带[]的是内核守护进程\
d结尾的是应用程序的守护进程\

sudo vi /etc/rc.local 开机自启动,绝对路径加程序名字
