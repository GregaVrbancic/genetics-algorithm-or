#!flask/bin/python3.5
from app import app, socketio
if __name__ == '__main__':
    socketio.run(app, host="localhost", port=5000, debug = True)