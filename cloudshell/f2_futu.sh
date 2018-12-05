#!/usr/bin/env bash
echo "-----init-----"
cd ~/ckquant/cloudshell/
./init.sh

echo "-----python-----"

cd ~/ckquant/cloudshell/
python3 main.py
python3 main_ck.py