#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################

DUMP_PATH_1="data/dumps/HMO_2020-21_project_dump_instance-1.json"
DUMP_PATH_2="data/dumps/HMO_2020-21_project_dump_instance-2.json"
DUMP_PATH_3="data/dumps/HMO_2020-21_project_dump_instance-3.json"
DUMP_PATH_4="data/dumps/HMO_2020-21_project_dump_instance-4.json"
DUMP_PATH_5="data/dumps/HMO_2020-21_project_dump_instance-5.json"
DUMP_PATH_6="data/dumps/HMO_2020-21_project_dump_instance-6.json"

DESTINATION_PATH="data/dumps/adjusted"


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/convert_dumps.py --dump_path $DUMP_PATH_1 \
                             --destination_path $DESTINATION_PATH

python3 src/convert_dumps.py --dump_path $DUMP_PATH_2 \
                             --destination_path $DESTINATION_PATH

python3 src/convert_dumps.py --dump_path $DUMP_PATH_3 \
                             --destination_path $DESTINATION_PATH

python3 src/convert_dumps.py --dump_path $DUMP_PATH_4 \
                             --destination_path $DESTINATION_PATH

python3 src/convert_dumps.py --dump_path $DUMP_PATH_5 \
                             --destination_path $DESTINATION_PATH

python3 src/convert_dumps.py --dump_path $DUMP_PATH_6 \
                             --destination_path $DESTINATION_PATH
