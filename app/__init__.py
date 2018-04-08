# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)  # 导入参数设置
db = SQLAlchemy(app)

from app.main import main as main_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

from app.socketios import *


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("ui/404.html"), 404


if __name__ == "__main__":
    app.run()
