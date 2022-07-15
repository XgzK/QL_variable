from conn.gheaders.log import log_ip
from conn.sql.pysql import select_data


def vaguefind(str12):
    """
    对比脚本和获取的值找到运行青龙需要的数字
    :param str12: 传入脚本名称
    :return: 如果成功返回脚本的专属id,如果脚本不存在返回-1
    """
    try:
        l = select_data()
        # 循环读取青龙脚本
        for i in range(len(l)):
            # 把多余的部分去掉
            cs = l[i][2].split("/")
            # print(cs[-1])
            # 对比脚本名称
            if cs[-1] == str12:
                print("脚本名称：" + str12 + "脚本id：" + str(l[i][0]))
                # 因为必须数组所以这里创建一个数组,返回数组id
                dd = [l[i][0]]
                # 如果对比成功立刻结束此方法
                log_ip("脚本: " + str12 + "名称: " + l[i][1] + "id: " + str(l[i][0]))
                return dd
        # 如果运行到这里表示这个脚本你没有
        log_ip(str(str12) + "脚本不存在")
        return -1
    except Exception as e:
        log_ip("vaguefind,异常信息：" + str(e))
