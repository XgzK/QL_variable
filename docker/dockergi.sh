#!/bin/bash
cd /root/ || exit
# 制作更新指令
cd /root/QL_variable/ || exit
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# 文件移动出去
mv -f /root/QL_variable/repeat.sqlite /home && mv -f /root/QL_variable/conn.yml /home
# 错误编译
pyinstaller --add-binary 'com/Web/templates:com/Web/templates' --add-binary 'com/Web/static:com/Web/static' fsbot.py
# 移动到编译目录
mv -f /home/repeat.sqlite /root/QL_variable/dist/fsbot && mv -f /home/conn.yml /root/QL_variable/dist/fsbot