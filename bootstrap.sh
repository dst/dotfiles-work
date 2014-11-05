#!/usr/bin/env bash

# Dariusz Stefanski
# 05.11.2014
#
# Boostraps work dotfiles project

REPO_PATH=~/myprojects/dotfiles-work

mkdir -p $REPO_PATH
sudo apt-get install git
git clone git@github.com:dst/dotfiles-work.git $REPO_PATH
cd $REPO_PATH
./install.sh
