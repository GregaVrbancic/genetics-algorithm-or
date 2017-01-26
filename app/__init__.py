from flask import Flask
import eventlet
from flask_socketio import SocketIO

app = Flask(__name__)
eventlet.monkey_patch()
async_mode = 'eventlet'
socketio = SocketIO(app, async_mode=async_mode)

from app import views
