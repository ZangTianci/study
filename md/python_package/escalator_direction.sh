#!/bin/bash
Direction=$1
touch /opt/vpm/base/stop_vision_processing_server
sleep 3
if [ -f "/opt/vpm/base/stop_vision_processing_server" ]
then
    echo touch stop_vision_processing_server succeed! 
    if [ $Direction = "1" ]
    then
        sed -i 's/name=escalator_direction type=integer value=2/name=escalator_direction type=integer value=1/g' ./user_vision_processing_server_configuration.xml
        echo "escalator_up!"
        wget http://www.goquant666.cn/news/news_md_ci/sh_mtc_vpm50_chang_direction_goingup  -O/dev/null
    elif [ $Direction = "2" ]
    then
        sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' ./user_vision_processing_server_configuration.xml
        echo "escalator_down!"
        wget http://www.goquant666.cn/news/news_md_ci/sh_mtc_vpm50_chang_direction_goingdown -O/dev/null
    else
        echo invalid input!
    fi
else
    echo touch stop_vision_processing_server failed!
fi
rm /opt/vpm/base/stop_vision_processing_server
if [ -f "/opt/vpm/base/stop_vision_processing_server" ]
then
    echo rm stop_vision_processing_server failed!
else
    echo rm stop_vision_processing_server successfully!
fi

