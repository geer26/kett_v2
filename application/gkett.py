#from gevent import monkey
#monkey.patch_all()

import eventlet
eventlet.monkey_patch()

from app import app