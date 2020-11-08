#!/bin/bash

##################################################################
##  Constants                                                   ##
##################################################################
ROOT_PATH="/mnt/data/projekti/faks/HMO/tasks/midterm-task"

INSTANCE_1_PATH="data/HMO_2020-21_midterm-task_instance-1-fixed.csv"
INSTANCE_2_PATH="data/HMO_2020-21_midterm-task_instance-2-fixed.csv"

GREEDY_SOLUTION_1="data/greedy-search/solution-1.txt"
GREEDY_SOLUTION_2="data/greedy-search/solution-2.txt"
LOCAL_SOLUTION_1="data/local-search/solution-1.txt"
LOCAL_SOLUTION_2="data/local-search/solution-2.txt"

##################################################################
##  Environment                                                 ##
##################################################################

cd $ROOT_PATH

##################################################################
##  Functionality                                               ##
##################################################################

echo "Greedy search on instance 1"
python3 src/ext/validator.py $INSTANCE_1_PATH $GREEDY_SOLUTION_1
echo ""

echo "Greedy search on instance 2"
python3 src/ext/validator.py $INSTANCE_2_PATH $GREEDY_SOLUTION_2
echo ""

echo "Local search on instance 1"
python3 src/ext/validator.py $INSTANCE_1_PATH $LOCAL_SOLUTION_1
echo ""

echo "Local search on instance 2"
python3 src/ext/validator.py $INSTANCE_2_PATH $LOCAL_SOLUTION_2
echo ""
