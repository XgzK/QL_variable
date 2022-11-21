from com.gheaders.conn import read_yaml


def ql_header(Authorization):
    """
    返回ql需要请求头
    :param Authorization: 青龙密钥
    :return:
    """
    authoriza = read_yaml()
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    return headers


def qlck_header():
    """
    返回ql需要请求头
    :return:
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    return headers
