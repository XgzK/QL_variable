from conn.gheaders.conn import read_yaml


def ql_header():
    """
    返回ql需要请求头
    :return:
    """
    authoriza = read_yaml()
    headers = {
        'Accept': 'application/json',
        'Authorization': authoriza['Authorization'],
        'Content-Type': 'application/json;charset=UTF-8'
    }
    return headers
