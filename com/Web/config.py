import uuid

# 给这个网站设置密钥
SECRET_KEY = ''.join(str(uuid.uuid4()).split('-'))
DEBUG = False
SSL_DISABLE = False