#! /bin/bash

# Validate kp files for given or current month.
# Darek Stefanski
# 10.09.2014

. ~/.bash-paths-work

if [ $# -ne 1 ]
then
  date=`date +"%Y.%m"`
else
  date=$1
fi

#TODO: validate files $KP_PATH/$date.*.kp
