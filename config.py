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
PASSWORD = 'xxxxxxx'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设定上传文件的保存目录
UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
MEM_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app\\static\\uploads\\members\\")


# session加密所需要的随机参数
SECRET_KEY = b'\x01\x9c\xb4\xf3\x90s9\xff\x90\x18\xc9h`\xa5\x83\xfb\xeb\x1af\x07\x0c\xff\x16\x0e'
# SECRET_KEY = os.urandom(24)
# print(SECRET_KEY)

# 设定session的过期时间
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

# 原始绑于app.__init__里面的参数
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:chiaki2008@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "af2fad8cfe1f4c5fac4aa5edf6fcc8f3"
# app.config["UP_DIR"]=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
# app.debug = True
