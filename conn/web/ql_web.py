from flask import Flask

from conn.gheaders.log import rz

app = Flask(__name__)


@app.route("/")
def index():
    return "你好本程序运行正常运行"


@app.route('/log')
def log():
    lo = rz()
    if lo == -1:
        return "日志为空"
    return lo


def run_web():
    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
