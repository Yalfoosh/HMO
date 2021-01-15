#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################

INSTANCE_PATH="data/original/HMO_2020-21_project_instance-4.txt"
DUMP_PATH="data/dumps/HMO_2020-21_project_dump_instance-4.json"
MAX_RUNTIME=(1 5 25)


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/main.py --instance_path $INSTANCE_PATH \
                    --dump_path $DUMP_PATH \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})
