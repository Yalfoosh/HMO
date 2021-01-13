#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################

INSTANCE_PATH_1="data/original/HMO_2020-21_project_instance-1.txt"
INSTANCE_PATH_2="data/original/HMO_2020-21_project_instance-2.txt"
INSTANCE_PATH_3="data/original/HMO_2020-21_project_instance-3.txt"
INSTANCE_PATH_4="data/original/HMO_2020-21_project_instance-4.txt"
INSTANCE_PATH_5="data/original/HMO_2020-21_project_instance-5.txt"
INSTANCE_PATH_6="data/original/HMO_2020-21_project_instance-6.txt"

DUMP_PATH_1="data/dumps/HMO_2020-21_project_dump_instance-1.json"
DUMP_PATH_2="data/dumps/HMO_2020-21_project_dump_instance-2.json"
DUMP_PATH_3="data/dumps/HMO_2020-21_project_dump_instance-3.json"
DUMP_PATH_4="data/dumps/HMO_2020-21_project_dump_instance-4.json"
DUMP_PATH_5="data/dumps/HMO_2020-21_project_dump_instance-5.json"
DUMP_PATH_6="data/dumps/HMO_2020-21_project_dump_instance-6.json"

MAX_RUNTIME=(1 5 60)


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/main.py --instance_path $INSTANCE_PATH_1 \
                    --dump_path $DUMP_PATH_1 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})

python3 src/main.py --instance_path $INSTANCE_PATH_2 \
                    --dump_path $DUMP_PATH_2 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})

python3 src/main.py --instance_path $INSTANCE_PATH_3 \
                    --dump_path $DUMP_PATH_3 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})

python3 src/main.py --instance_path $INSTANCE_PATH_4 \
                    --dump_path $DUMP_PATH_4 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})

python3 src/main.py --instance_path $INSTANCE_PATH_5 \
                    --dump_path $DUMP_PATH_5 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})

python3 src/main.py --instance_path $INSTANCE_PATH_6 \
                    --dump_path $DUMP_PATH_6 \
                    --max_runtime $(echo ${MAX_RUNTIME[@]})
