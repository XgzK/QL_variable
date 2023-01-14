from flask import render_template, request, redirect, url_for, flash, session, Blueprint

from com.gheaders.conn import ConnYml
from com.fo.poadd import ym_change
from com.sql import Sql

conn = Sql()
connyml = ConnYml()
ind = Blueprint('index', __name__)


@ind.route("/", methods=['GET', 'POST'])
def index():
    """
    表单
    :return:
    """
    if request.method == 'POST':
        books = request.values.getlist('books[]')
        # 把表单传递给方法添加到conn.yml
        q = ym_change(books)
        flash(q[1])
        return redirect(url_for('ind.index'))
    else:
        yml = connyml.read_yaml()
        if yml['deduplication'] == 1:
            return render_template('yml.html', chec='')
        else:
            return render_template('yml.html', chec='checked')


@ind.route("/login", methods=["GET", "POST"])
def login():
    """
    登录
    :return:
    """
    # 清空session
    session.pop('username', None)
    if request.method == 'POST':
        username = request.values.get("username")
        password = request.values.get("password")
        # 如果有空
        if not all([username, password]):
            flash("密码或账户为空")
            return redirect(url_for('ind.login'))
        else:
            new_user = conn.selectAll(table=conn.surface[4])
            # 查询是否有密码和账户存在，如果没有让用户注册
            if not new_user:
                # 插入用户名和密码
                conn.insert(table=conn.surface[4], username=f"{username}", password=f"{password}")
                session['username'] = username
                session.permanent = True
                return redirect(url_for('ind.index'))
            # 如果验证成功，将用户名加密并保存在cookie中
            user_ck = conn.selectTopone(table=conn.surface[4], where=f"username='{username}'")
            if not user_ck:
                # 没有查询到用户用户信息
                flash("输入的密码或账户不正确")
                return redirect(url_for('ind.login'))
            # 判断用户是否存在
            elif username == user_ck[0] and password == user_ck[1]:
                session['username'] = username
                session.permanent = True
                return redirect(url_for('ind.index'))
            else:
                flash("输入的密码或账户不正确")
                return redirect(url_for('ind.login'))
    else:
        return render_template('login.html')
