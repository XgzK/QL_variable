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
   cp -r /val/conn.yml /
   # 删除ip下所有文件
   rm -rf /val/*
   # 移动文件
   cp -r /root/QL_variable/* /val
   # 删除复制过来的配置文件
   rm -rf /val/conn.yml
   # 把配置文件移动到项目目录
   cp -r /conn.yml /val
   # 删除复制出去的文件
   rm -rf /conn.yml
else
  echo "删除配置文件更新项目"
  # 删除ip下所有文件
  rm -rf /val/*
  # 移动文件
  cp -r /root/QL_variable/* /val
fi
# 判断文件是否存在存在则执行
if [ -f "/root/QL_variable/test.sh" ];then
  sh /root/QL_variable/test.sh
else
  echo "没有检测到文件不需要额外执行其他任务"
fi
# 删除压缩包, 删除文件夹
rm -rf qlva.tgz QL_variable
cd /val || exit
pip3 install -r requirements.txt
# shellcheck disable=SC2046
kill -9 $(netstat -nlp | grep :5008 | awk '{print $7}' | awk -F"/" '{ print $1 }')
echo 杀死了了原本程序自动启动