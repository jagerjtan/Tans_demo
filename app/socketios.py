# coding: utf8
from app import app
from threading import Lock
from flask_socketio import SocketIO, disconnect
import psutil, time

# 监控线程
thread = None
thread_lock = Lock()
freq = 3

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    global freq
    count = 0
    netlist = [psutil.net_io_counters().bytes_recv]
    while True:
        socketio.sleep(freq)
        count += 1
        t = time.strftime('%H:%M:%S', time.localtime())  # 获取系统时间
        cpus = round(sum(psutil.cpu_percent(interval=None, percpu=True)) / 4, 2)  # 获取系统cpu使用率 non-blocking
        mem = psutil.virtual_memory().percent
        netlist.append(psutil.net_io_counters().bytes_recv)
        net = round((netlist[-1] - netlist[-2]) / ((1024 ** 2) * 3) * 100, 2)
        netlist.pop(0)

        data = {"data": [cpus, mem, net, count, t]}
        socketio.emit('server_response', data, namespace='/serverow')  # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！


# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/serverow')
def stat_connect():
    global thread
    print('client-side connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect', namespace='/serverow')
def stat_end():
    disconnect(namespace='/serverow')
    print('client-side disconnect')

@socketio.on('freq', namespace='/serverow')
def change_freq(myfreq):
    global freq
    freq = int(myfreq['data'])
    print("change freq to %d second" % freq)


@socketio.on('connect', namespace='/test')
def chat_connect():
    socketio.emit('server_sent', {'data': 'Connected!'}, namespace='/test')


@socketio.on('client_sent', namespace='/test')
def chat_loop(msg):
    if msg:
        socketio.sleep(5)
        socketio.emit('server_sent', {'data': 'here'}, namespace = '/test')
        print(msg['data'])
