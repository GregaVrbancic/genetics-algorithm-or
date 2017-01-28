from app import app, genetic, socketio
from flask import render_template, send_from_directory
from flask_socketio import emit, disconnect, join_room, leave_room
from threading import Thread, Event
import datetime
import random, string

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('../client/scripts', path)

@socketio.on('connect', namespace='/word-guess')
def on_connect_word_guess():
    print('Client connected to word-guess')
    gen_room = generateRoom()
    join_room(gen_room)
    socketio.emit('connected response', {'room': gen_room}, namespace='/word-guess', broadcast=False)

@socketio.on('connect', namespace='/travelling-salesman')
def on_connect_travelling_salesman():
    print('Client connected to travelling-salesman')
    gen_room = generateRoom()
    join_room(gen_room)
    socketio.emit('connected response', {'room': gen_room}, namespace='/travelling-salesman', broadcast=False)

def generateRoom():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(15))

@socketio.on('leave', namespace='/word-guess')
def on_leave_word_guess(command):
    print('Client disconnected from word guess')
    leave_room(command['room'])

@socketio.on('leave', namespace='/travelling-salesman')
def on_leave_travelling_salesman():
    print('Client disconneted from travelling salesman')
    leave_room(command['room'])

@socketio.on('start', namespace='/word-guess')
def on_start_word_guess(command):
    print('Command start on namespace word-guess received: ' + command['command'])
    thread = Thread()
    thread_stop_event = Event()
    
    if not thread.isAlive():
        print('Starting GuessWordThread...')
        thread = GuessWordThread(command)
        thread.start()

@socketio.on('start', namespace='/travelling-salesman')
def on_start_travelling_salesman(command):
    print('Command start on namespace travelling-salesman received: ' + str(command))


class GuessWordThread(Thread):
    def __init__(self, command):
        self.delay = 1
        self.geneset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"
        self.target = command['command']
        self.room = command['room']
        super(GuessWordThread, self).__init__()

    def guessWord(self):
        startTime = datetime.datetime.now()

        def fnGetFitness(genes):
            return sum(1 for expected, actual in zip(self.target, genes) if expected == actual)

        def fnDisplay(candidate):
            timeDiff = datetime.datetime.now() - startTime
            socketio.emit('server response', {'genes': candidate.Genes, 'fitness': candidate.Fitness, 'time': str(timeDiff)}, namespace='/word-guess', room=self.room, broadcast=False)

        optimalFitness = len(self.target)
        best = genetic.get_best(fnGetFitness, len(self.target), optimalFitness, self.geneset, fnDisplay)


    def run(self):
        self.guessWord()
