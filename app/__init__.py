# coding:utf8
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config) #导入参数设置
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:chiaki2008@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "af2fad8cfe1f4c5fac4aa5edf6fcc8f3"
# app.config["UP_DIR"]=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
# app.debug = True
db = SQLAlchemy(app)

from app.main import main as main_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404


if __name__ == "__main__":
    app.run()
