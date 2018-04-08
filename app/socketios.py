# coding: utf8
from app import app
from threading import Lock
from flask_socketio import SocketIO
import psutil, time

# 监控线程
thread = None
thread_lock = Lock()

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    netlist = [psutil.net_io_counters().bytes_recv]
    while True:
        socketio.sleep(2)
        count += 1
        t = time.strftime('%H:%M:%S', time.localtime())  # 获取系统时间
        cpus = round(sum(psutil.cpu_percent(interval=None, percpu=True)) / 4, 2)  # 获取系统cpu使用率 non-blocking
        mem = psutil.virtual_memory().percent
        netlist.append(psutil.net_io_counters().bytes_recv)
        net = round((netlist[-1] - netlist[-2]) / ((1024 ** 2) * 3) * 100, 2)
        netlist.pop(0)
        socketio.emit('server_response',
                      {'data': [t, cpus, mem, net], 'count': count},
                      namespace='/serverow')  # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！


# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/serverow')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
