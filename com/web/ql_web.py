import threading

from flask import Flask, render_template, request, redirect, url_for, flash

from com.gheaders.conn import read_yaml
from com.gheaders.log import rz
from com.fo.poadd import ym_change, upgrade, to_stop
from com.sql import conn

app = Flask(__name__)
app._static_folder = "./templates/"
# 给这个网站设置密钥
app.config['SECRET_KEY'] = 'AHTKFJYTJddyktu56587970'


@app.route("/", methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    else:
        yml = read_yaml()
        if yml['deduplication'] == 1:
            return render_template('yml.html', chec='')
        else:
            return render_template('yml.html', chec='checked')


@app.route('/log', methods=['GET'])
def log():
    """
    日志
    :return:
    """
    return render_template('log.html', rz=rz())


@app.route('/repeat', methods=['GET'])
def repeat():
    """
    重复的数据库值
    :return:
    """
    se_repeat = conn.selectAll(table=conn.surface[1])
    return render_template('aa.html', se_repeat=se_repeat)


@app.route('/under')
def under():
    """
    未分类功能
    :return:
    """
    return render_template('gi.html')


@app.route("/gi", methods=['POST'])
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


@app.route("/pare", methods=['GET'])
def pare():
    """
    禁用活动任务
    :return:
    """
    res = to_stop()
    flash(res)
    return redirect(url_for('under'))


def run_web():
    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
