#!/bin/bash
get_arch='arch'
# 容器保活
# 判断文件是否存在不存在则拉取
if [ ! -f "/val/repeat.sqlite" ]; then
  echo "没有检测到文件存在拉取新项目"
  python3 -m pip install --upgrade pip
  sh /root/UpdateAll.sh
fi
while true
do
    # 停止返回0 正常返回1
    # shellcheck disable=SC2009
    # shellcheck disable=SC2126
    stillRunning=$(ps -ef |grep fsbot |grep -v "grep" |wc -l)
    if [ "$stillRunning" ]; then
      echo 程序死亡开始执行
      # 判断文件是否存在不存在则拉取
      if [ ! -f "/val/repeat.sqlite" ]; then
          sh /root/UpdateAll.sh
      fi
      # shellcheck disable=SC2046
      if [[ $get_arch =~ "x86_64" ]];then
        echo 检测到系统是 $get_arch 执行 fsbot
        kill -9 $(netstat -nlp | grep fsbot | awk '{print $7}' | awk -F"/" '{ print $1 }')
        cd /val && ./fsbot
      else
        echo 检测到系统是 $get_arch 执行 fsbot.py
        kill -9 $(netstat -nlp | grep fsbot.py | awk '{print $7}' | awk -F"/" '{ print $1 }')
                cd /val && python fsbot.py
      fi
    fi
done