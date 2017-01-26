from app import app, genetic, socketio
from flask import render_template, send_from_directory
from flask_socketio import emit, disconnect
from threading import Thread, Event
import datetime
import random

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('../client/scripts', path)

@socketio.on('connect', namespace='/word-guess')
def test_connect():
    print('Client connected to word-guess')

@socketio.on('start', namespace='/word-guess')
def test_message(command):
    print('Command start on namespace word-guess received: ' + command['command'])
    thread = Thread()
    thread_stop_event = Event()
    
    if not thread.isAlive():
        print('Starting GuessWordThread...')
        thread = GuessWordThread(command['command'])
        thread.start()

class GuessWordThread(Thread):
    def __init__(self, target):
        self.delay = 1
        self.geneset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"
        self.target = target
        super(GuessWordThread, self).__init__()

    def guessWord(self):
        startTime = datetime.datetime.now()

        def fnGetFitness(genes):
            return sum(1 for expected, actual in zip(self.target, genes) if expected == actual)

        def fnDisplay(candidate):
            timeDiff = datetime.datetime.now() - startTime
            socketio.emit('server response', {'genes': candidate.Genes, 'fitness': candidate.Fitness, 'time': str(timeDiff)}, namespace='/word-guess', broadcast=False)

        optimalFitness = len(self.target)
        best = genetic.get_best(fnGetFitness, len(self.target), optimalFitness, self.geneset, fnDisplay)


    def run(self):
        self.guessWord()
