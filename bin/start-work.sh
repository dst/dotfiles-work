#!/bin/bash

# Starts programs useful at work
# Dariusz Stefanski
# 10.09.2014

. ~/.bash-functions
. ~/.bash-paths-work

echo "Starting work"

kp-validate.sh
kp-open.sh

pullGitRepo $WORK_REPO_PATH

# Force start, because we use also zim for it-zim-notes
startProgramForce zim $ZIM_NOTES_WORK_PATH

# start project specific if exists
start-project.sh