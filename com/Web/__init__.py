from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from . import config

app = Flask(__name__, static_folder="static", static_url_path='/static', template_folder='templates')
app.config.from_object(config)
# 防止跨域
CORS(app, resources=r'/*')
# ws 配置
connected_sids = set()
socketio = SocketIO(app, cors_allowed_origins='*')

