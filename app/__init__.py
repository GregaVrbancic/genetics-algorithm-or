from flask import Flask
import eventlet
from flask_socketio import SocketIO

app = Flask(__name__)

# setup the socketio
eventlet.monkey_patch()
async_mode = 'eventlet'
socketio = SocketIO(app, async_mode=async_mode)

app.debug = True

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from app import views
from app import genetic
