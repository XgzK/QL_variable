import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.log import log_ip
from conn.ql.ql_write import yml_file


def ql_tk():
    """
    用于获取登录用的ck,ck有效期一个月
    :return: 返回登录用的Bearer XXXXXXXXXXX，如果没有获取到，返回0
    """
    try:
        yam = read_yaml()
        url = yam['ip'] + "/open/auth/token"
        params = {
            'client_id': yam['Client ID'],
            'client_secret': yam['Client Secret']
        }
        cs = requests.get(url=url, params=params, timeout=5)
        print(cs.url)
        jstx = cs.json()
        log_ip("获取登录Bearer成功")
        return jstx['data']['token_type'] + " " + jstx['data']['token']
    except Exception as e:
        print("ql_tk异常信息，请检查conn.yml文件第2行和第3行，异常信息：" + str(e))
        log_ip("ql_tk异常信息，请检查conn.yml文件第2行和第3行，异常信息：" + str(e))
        return 0


def token_main():
    """
    主要用于调用ck
    :return:
    """
    try:
        ck = ql_tk()
        if ck != 0:
            str1 = 'Authorization:' + f" '{ck}'"
            yml_file(str1, 5)
            log_ip("新的Bearer添加成功token_main")
            yml_file("judge: 0", 19)
        else:
            log_ip("新的Bearer添加失败,token_main")
            # 如果异常就向conn.yml添加一个值 false
            yml_file("judge: 1", 19)
    except Exception as e:
        print("token_main败，请检查conn.yml文件第2行和第3行，异常信息：" + str(e))
        log_ip("token_main败，请检查conn.yml文件第2行和第3行，异常信息：" + str(e))
