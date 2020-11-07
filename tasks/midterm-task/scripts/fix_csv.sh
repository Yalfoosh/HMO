#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################
ROOT_PATH="/mnt/data/projekti/faks/HMO/tasks/midterm-task"

CSV_PATHS=(\
    "data/HMO_2020-21_midterm-task_instance-1.csv" \
    "data/HMO_2020-21_midterm-task_instance-2.csv"\
)
DESTINATION_FOLDER="data"


##################################################################
##  Environment                                                 ##
##################################################################

cd $ROOT_PATH


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/fixes/fix_csv.py --csv_paths $(echo ${CSV_PATHS[@]}) \
                             --destination_folder $DESTINATION_FOLDER \
                             --tsv
