#!/usr/bin/env bash

# Dariusz Stefanski
# 10.09.2014

. ~/.bash-functions

REPO_ROOT=`pwd`

createBackupDir
installHomeDotfiles $REPO_ROOT
installBin $REPO_ROOT/bin work
