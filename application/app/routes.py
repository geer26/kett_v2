from flask import render_template
from app import app, socket


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/single/')
def single_mode():
    return render_template('single_vue.html')


@socket.on('message')
def ping():
    socket.emit('pong!')
