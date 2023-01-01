#!/bin/bash
cd /root/ || exit
# 制作更新指令
cd /root/QL_variable/ || exit
#pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
nuitka3 --follow-import-to=com --output-dir=out fsbot.py
cp out/fsbot.bin /root/QL_variable/fsbot
rm -rf out