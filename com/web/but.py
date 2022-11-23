import threading

from flask import render_template, Blueprint, request, flash, redirect, url_for

from com.fo.poadd import upgrade, to_stop
from com.gheaders.log import rz
from com.sql import Sql

apg = Blueprint('but', __name__)
conn = Sql()


@apg.route('/log', methods=['GET'])
def log():
    """
    日志
    :return:
    """
    return render_template('log.html', rz=rz())


@apg.route('/repeat', methods=['GET'])
def repeat():
    """
    重复的数据库值
    :return:
    """
    se_repeat = conn.selectAll(table=conn.surface[1])
    return render_template('aa.html', se_repeat=se_repeat)


@apg.route("/gi", methods=['POST'])
def gi():
    """
    更新软件
    :return:
    """
    if request.method == 'POST':
        git = request.values.get('gi')
        t1 = threading.Thread(target=upgrade, args=(int(git),))
        t1.start()
    # 提示语
    flash('10秒后刷新浏览器')
    # 重定向到首页
    return redirect(url_for('under'))


@apg.route('/under')
def under():
    """
    未分类功能
    :return:
    """
    return render_template('gi.html')


@apg.route("/pare", methods=['GET'])
def pare():
    """
    禁用活动任务
    :return:
    """
    res = to_stop(request.values.get('sun'))
    flash(res)
    return redirect(url_for('under'))
