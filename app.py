from time import sleep
from requests import request
from threading import Thread, Event
from flask import Flask, render_template, request
from BaseDatos import Conexion

class LoopThread(Thread):
    def __init__(self, stop_event):
        self.stop_event = stop_event

        Thread.__init__(self)

    def run(self):
        while not self.stop_event.is_set():
            self.loop_process()

    def restart(self):
        self.stop_event.clear()
        self.run()

    def loop_process(self):
        db.insertar()
        sleep(1)


db = Conexion()
STOP_EVENT = Event()
STOP_EVENT.set()
thread = LoopThread(STOP_EVENT)
thread.start()

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    mensaje=''
    STOP_EVENT.set()
    thread.join()
    if request.method =='POST':
        user = request.form['user']
        password = request.form['password']
        host = request.form['host']
        mensaje = db.conectar(user, password, host)

        return render_template('index.html', mensaje=mensaje)
    return render_template('index.html', mensaje=mensaje)

@app.route('/insertar')
def insertar():
    thread.restart()
    return 'Información insertada'

@app.route('/leer')
def leer():
    STOP_EVENT.set()
    thread.join()
    bancos = db.leer()
    return render_template('leer_info.html', bancos=bancos)
