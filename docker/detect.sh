#!/bin/sh
# 容器保活
# 判断文件是否存在不存在则拉取
if [ ! -f "/val/addvalue.py" ];then
  echo "没有检测到文件存在拉取新项目"
  sh /root/UpdateAll.sh
else
  echo "检测到文件存在不再拉取新项目"
fi
while true
do
    # 停止返回0 正常返回1
    # shellcheck disable=SC2009
    # shellcheck disable=SC2126
    stillRunning=$(ps -ef |grep addvalue.py |grep -v "grep" |wc -l)
    if [ "$stillRunning" ]; then
      echo 程序死亡开始执行
      cd /val && python3 addvalue.py
    else
      echo 请等待3000秒后执行;
      sleep 3000
    fi
done