#!/bin/bash

sed -i 's/name=escalator_direction type=integer value=1/name=escalator_direction type=integer value=2/g' ./user_vision_processing_server_configuration.xml
echo "escalator_up!"

 