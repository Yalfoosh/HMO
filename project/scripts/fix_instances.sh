#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################

SOURCE_FOLDER_PATH="data/original"
DESTINATION_FOLDER_PATH="data/json"


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/fix_instances.py --source_folder_path $SOURCE_FOLDER_PATH \
                             --destination_folder_path $DESTINATION_FOLDER_PATH
