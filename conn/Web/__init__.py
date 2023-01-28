import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from . import config

app = Flask(__name__, static_folder=os.getcwd().replace("\\", "/") + "/Web/static", static_url_path='/static',
            template_folder=os.getcwd().replace("\\", "/") + '/Web/templates')
app.config.from_object(config)
# 防止跨域
CORS(app, resources=r'/*', supports_credentials=True)
# ws 配置
connected_sids = set()
socketio = SocketIO(app, cors_allowed_origins='*')
