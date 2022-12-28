import re

from flask import request, session, flash, redirect, url_for

from . import app, index, but, connected_sids, socketio
from ..sql import Sql

app.register_blueprint(index.ind, name='ind', url_prefix='/')
app.register_blueprint(but.apg, name='apg', url_prefix='/config')
conn = Sql()


@app.before_request
def befores():
    """
    每次请求都执行
    :return:
    """
    ht_ip = request.environ
    # 检查的IP不是127.0.0.1 和session为空 不等于 登录
    if ht_ip['REMOTE_ADDR'] != '127.0.0.1' and ht_ip['PATH_INFO'] != '/login' and len(
            re.findall('^(/static/[jscimg]+)/', ht_ip['PATH_INFO'])) == 0:
        username = session.get('username')
        user_ck = conn.selectTopone(table=conn.surface[4], where=f"username='{username}'")
        # 检测有没有这个用户存在
        if not user_ck:
            new_user = conn.selectAll(table=conn.surface[4])
            # 如果返回的有用户存在
            if not new_user:
                flash("没有检测到账户存在请设置密码和账户")
            return redirect(url_for('ind.login'))
    else:
        # 发生未知事件
        return redirect(url_for('ind.login'))


@socketio.on('connect')
def on_connect():
    """
    链接来了
    :return:
    """
    connected_sids.add(request.sid)
    # print(f'{request.sid} 已连接')


@socketio.on('disconnect')
def on_disconnect():
    """
    断开连接
    :return:
    """
    connected_sids.remove(request.sid)
    # print(f'{request.sid} 已断开')
