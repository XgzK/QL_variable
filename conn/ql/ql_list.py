from conn.gheaders.conn import read_yaml
from conn.gheaders.log import log_ip
from conn.ql.ql_Version import ql10_db, ql13_sql


def vaguefind(str12):
    """
    对比脚本和获取的值找到运行青龙需要的数字，现在是适配器，根据青龙版本执行不同的方法
    :param str12: 传入脚本名称
    :return: 如果成功返回脚本的专属id,如果脚本不存在返回[-1]
    """
    try:
        versi = read_yaml()
        # 判断青龙版本
        if versi['qlVersion'] <= 10:
            return ql10_db(str12)
        elif versi['qlVersion'] >= 11:
            return ql13_sql(str12)
        else:
            print("青龙版本未知")
            log_ip("青龙版本未知,请阅读conn.yml配置文件说明")
            return [-1]
    except Exception as e:
        log_ip("vaguefind,异常信息：" + str(e))
