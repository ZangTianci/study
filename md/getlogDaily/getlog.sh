#!/bin/bash
rm -f /home/magicdepth/ztc/dpmlog.zip
rm -f /home/magicdepth/ztc/vpmlog.zip
scp root@192.168.1.250:/userdata/log/LOG_ODM_System_1.txt /home/magicdepth/ztc/dpmlog
scp root@192.168.1.250:/userdata/log/LOG_ODM_System_2.txt /home/magicdepth/ztc/dpmlog
zip dpmlog.zip /home/magicdepth/ztc/dpmlog/*
zip vpmlog.zip /opt/log/LOG_ODM_System*
rm /home/magicdepth/ztc/dpmlog/*