from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Workout


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('supervisor_mode'))
    if not current_user.is_authenticated and request.method == 'POST':

        if request.form['uname'] and request.form['passw']:
            user = User.query.filter_by(username=request.form['uname']).first()

            if not user or not user.check_password(request.form['passw']):
                print('LOGIN FAILED!')
                return redirect(url_for('index'))

            else:
                login_user(user)
                return redirect(url_for('supervisor_mode'))

        else:
            print('MISSING LOGIN DATA!')
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/single/')
def single_mode():
    return render_template('single_vue.html')


@app.route('/supervisor/')
@login_required
def supervisor_mode():
    return render_template('supervisor_vue.html')


@app.route('/supervised/')
def supervised_mode():
    return render_template('supervised_vue.html')


@app.route('/adduser/<username>/<password>')
def addsu(username, password):
    #eg. https://example.com/examplesuname/example1Password!2
    user = User()
    user.username = username
    user.set_password(password)
    user.is_superuser = True
    db.session.add(user)
    db.session.commit()
    return redirect('/')
