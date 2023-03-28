#!/bin/bash
status=$1
dir=0
if [ $status = "up" ]
then
    dir='1'
elif [ $status = "down" ]
then 
    dir='2'
fi
esc=`sed -n '/escalator_direction/p' user_vision_processing_server_configuration.xml`
escr=${esc#*value=}
escr1=${escr%></record>*}
if [ $escr1 = $dir ]
then
    echo 1
else
    echo 2 
fi


