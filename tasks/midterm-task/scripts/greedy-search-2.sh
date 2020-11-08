#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################
ROOT_PATH="/mnt/data/projekti/faks/HMO/tasks/midterm-task"

INSTANCE_PATH="data/HMO_2020-21_midterm-task_instance-2.tsv"
DUMP_PATH="data/greedy-search/dump-2.tsv"
SOLUTION_DUMP_PATH="data/greedy-search/solution-2.txt"

PRICE_BUDGET=100.0
MAX_PLAYERS_IN_MAIN_TEAM=11
MAX_PLAYERS_PER_CLUB=3

GK_COUNT=2
DEF_COUNT=5
MID_COUNT=5
FW_COUNT=3

GK_RANGE=(1 1)
DEF_RANGE=(3)
MID_RANGE=(0)
FW_RANGE=(1)

VERBOSITY=2


##################################################################
##  Environment                                                 ##
##################################################################

cd $ROOT_PATH


##################################################################
##  Functionality                                               ##
##################################################################

python3 src/greedy_search.py --instance_path $INSTANCE_PATH \
                             --dump_path $DUMP_PATH \
                             --solution_dump_path $SOLUTION_DUMP_PATH \
                             --price_budget $PRICE_BUDGET \
                             --max_players_in_main_team $MAX_PLAYERS_IN_MAIN_TEAM \
                             --max_players_per_club $MAX_PLAYERS_PER_CLUB \
                             --gk_count $GK_COUNT \
                             --def_count $DEF_COUNT \
                             --mid_count $MID_COUNT \
                             --fw_count $FW_COUNT \
                             --gk_range $(echo ${GK_RANGE[@]}) \
                             --def_range $(echo ${DEF_RANGE[@]}) \
                             --mid_range $(echo ${MID_RANGE[@]}) \
                             --fw_range $(echo ${FW_RANGE[@]}) \
                             --verbosity $VERBOSITY
