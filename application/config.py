import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or '01!ChAnGeThIs!89'
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME') or '<Cookie_name>'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False