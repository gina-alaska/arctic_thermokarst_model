#!/bin/bash

# activate atm env and lauch atm program 
# $1 is the control file
# use:
#    ./run_atm.sh <path_to_control_file>
source activate atm-env && python atm/ATM.py $1
