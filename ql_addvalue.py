from flask_apscheduler import APScheduler

from conn.get_qlcs import get_main
from conn.gheaders.conn import read_yaml
from conn.gheaders.log import log_ip
from conn.ql.ql_del import descend, ql_write, del_file
from conn.ql.ql_list import vaguefind
from conn.ql.ql_run import ql_run
from conn.ql.ql_token import token_main

scheduler = APScheduler()


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return:
    """
    token_main()


@scheduler.task('interval', id='immortal_main', minutes=15)
def immortal_main():
    """
    主要功能运行,每15分钟运行一次
    :return:
    """
    jstx = read_yaml()
    if jstx['judge'] == 0:
        jsli = get_main()
        # 判断是否有任务
        if len(jsli) > 0:
            print("有任务")
            # 遍历获取所有任务列表
            for i in range(len(jsli[0])):
                print("获取到数据了")
                # 读取文件的行数
                descend()
                # 把内容添加最后一行
                ql_write(jsli[1][i])
                # 传入脚本名称
                id = vaguefind(jsli[0][i])
                print("id:" + str(id))
                # 判断是否有脚本
                if id != -1:
                    # 根据脚本id，执行脚本
                    print("执行脚本")
                    ql_run(id)
                # 删除添加的行
                del_file()
        else:
            log_ip("本次没有任务，15分钟后再次运行")
            print("本次没有任务，15分钟后再次运行")
    else:
        print("异常问题：conn.yml文件中judge设置为false,表示配置异常")


if __name__ == '__main__':
    print("开始运行")
    # 定时任务第一次不会执行，所以手动添加一次
    timing_ck()
    immortal_main()
    # 添加定时任务
    scheduler.start()
    print("手动执行结束")
    # 让程序一直运行
    while True:
        pass
