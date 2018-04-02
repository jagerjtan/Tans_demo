# -*- coding: utf-8 -*

import os
from datetime import timedelta

# 排查模式
DEBUG = True

# 数据库操作相关
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'tan_panel'  # 数据库的名字
USERNAME = 'root'
PASSWORD = 'chiaki2008'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设定上传文件的保存目录
UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")

# session加密所需要的随机参数
SECRET_KEY = os.urandom(24)

# 设定session的过期时间
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
