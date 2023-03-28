#!/bin/bash

set_direction=$1
esc=`sed -n '/escalator_direction/p' /home/magicdepth/fred/deploy_mtc/vpm48/user_vision_processing_server_configuration.xml`
escr=${esc#*value=}
escr1=${escr%></record>*}
if [ $set_direction = "up" ] || [ $set_direction = "1" ]
then
    echo 1
    if [ $escr1 = "2" ]
    then
        sed -i 's/name=escalator_direction type=integer value=2/name=escalator_direction type=integer value=1/g' /home/magicdepth/fred/deploy_mtc/vpm48/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=2/name=escalator_direction type=integer value=1/g' /home/magicdepth/fred/deploy_mtc/vpm50/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' /home/magicdepth/fred/deploy_mtc/vpm47/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' /home/magicdepth/fred/deploy_mtc/vpm49/user_vision_processing_server_configuration.xml
        ansible-playbook /home/magicdepth/fred/playbook/sh_mtc_upd_vpm_cfg_all.yml --ssh-common-args='-o ProxyCommand="ssh -W %h:%p  -q magicdepth@10.18.0.34"' -v
    fi
elif [ $set_direction = "down" ] || [ $set_direction = "2" ]
then
    echo 2
    if [ $escr1 = "1" ]
    then
        sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' /home/magicdepth/fred/deploy_mtc/vpm48/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' /home/magicdepth/fred/deploy_mtc/vpm50/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=2/name=escalator_direction type=integer value=1/g' /home/magicdepth/fred/deploy_mtc/vpm47/user_vision_processing_server_configuration.xml
        sed -i 's/name=escalator_direction type=integer value=2/name=escalator_direction type=integer value=1/g' /home/magicdepth/fred/deploy_mtc/vpm49/user_vision_processing_server_configuration.xml
        ansible-playbook /home/magicdepth/fred/playbook/sh_mtc_upd_vpm_cfg_all.yml --ssh-common-args='-o ProxyCommand="ssh -W %h:%p  -q magicdepth@10.18.0.34"' -v
    fi
fi