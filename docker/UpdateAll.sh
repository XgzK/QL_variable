#!/bin/bash
# 部分更新就是保留配置文件的更新
# 进入/root目录
cd /root/ || exit
# 下载
wget https://xgzq.tk/library/qlva.tgz
# 解压
tar -zxvf qlva.tgz
# 如果是1保留配置文件
if test "$1" = "1"; then
  echo "保留配置文件更新项目"
  # 把配置文件复制出来
  cp -f /val/conn.yml /
  cp -f /val/repeat.sqlite /
  rm -rf /val/*
  source ./dockergi.sh
  # 移动文件
  cp -rf /root/QL_variable/* /val
  # 把配置文件移动到项目目录
  mv -f /conn.yml /val
  mv -f /repeat.sqlite /val
else
  echo "删除配置文件更新项目"
  # 删除ip下所有文件
  rm -rf /val/*
  source ./dockergi.sh
  # 移动文件
  cp -rf /root/QL_variable/* /val
fi
# 判断文件是否存在存在则执行
if [ -f "/val/test.sh" ]; then
  sh /val/test.sh
else
  echo "没有检测到文件不需要额外执行其他任务"
fi
# 删除压缩包, 删除文件夹
rm -rf /root/qlva.tgz
rm -rf /root/QL_variable
# shellcheck disable=SC2046
kill -9 $(netstat -nlp | grep fsbot | awk '{print $7}' | awk -F"/" '{ print $1 }')