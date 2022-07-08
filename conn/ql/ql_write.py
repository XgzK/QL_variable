def yml_file(tx, sun, path='./conn.yml'):
    """

    :param tx: 添加的值
    :param sun: 添加的行
    :param path: 添加的路径
    :return:
    """
    f = open(path, 'r+', encoding='utf-8')
    flist = f.readlines()
    # ql行数从一开始，python读取从零开始
    try:
        flist[sun - 1] = '{}\n'.format(tx)
        f = open(path, 'w+', encoding='utf-8')
        f.writelines(flist)
    except Exception as e:
        print("异常问题，yml_file：" + str(e))
