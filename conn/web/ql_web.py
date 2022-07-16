from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "你好本程序运行正常运行"


def run_web():
    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
