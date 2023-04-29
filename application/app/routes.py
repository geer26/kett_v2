from flask import render_template
from app import app, socketio


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/single/')
def single_mode():
    return render_template('single_vue.html')
