# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config

from threading import Lock
from flask_socketio import SocketIO, emit
import psutil, time

# 监控线程
async_mode = None
thread = None
thread_lock = Lock()


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        t = time.strftime('%H:%M:%S', time.localtime())  # 获取系统时间（只取分:秒）
        cpus = psutil.cpu_percent(interval=None, percpu=True)  # 获取系统cpu使用率 non-blocking
        # getone = {'data': [t, *cpus]}
        # print(getone)
        socketio.emit('server_response',
                      {'data': [t, *cpus], 'count': count},
                      namespace='/test')  # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！


app = Flask(__name__)
app.config.from_object(config)  # 导入参数设置
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:chiaki2008@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "af2fad8cfe1f4c5fac4aa5edf6fcc8f3"
# app.config["UP_DIR"]=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
# app.debug = True
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode=async_mode)

from app.main import main as main_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("ui/404.html"), 404


if __name__ == "__main__":
    # socketio.run(app)
    app.run()
