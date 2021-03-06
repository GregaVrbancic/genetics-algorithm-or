from app import app, genetic, socketio
from flask import render_template, send_from_directory, json
from flask_socketio import emit, disconnect, join_room, leave_room
from threading import Thread, Event
from pyevolve import G1DList, GAllele, GSimpleGA, Crossovers, Consts
from math import sqrt
from PIL import Image, ImageDraw, ImageFont
import datetime, random, string
import imageio

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('../client/scripts', path)


@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory('./gen_imgs', path)

@app.route('/gif/<path:path>')
def send_gif(path):
    return send_from_directory('./gifs', path)

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
    print('Command start on namespace travelling-salesman received: ' + str(command));
    thread = Thread()
    thread_stop_event = Event()

    if not thread.isAlive():
        print('Starting TravellingSalesmanThread...')
        thread = TravellingSalesmanThread(command)
        thread.start()

class GuessWordThread(Thread):
    def __init__(self, command):
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

class TravellingSalesmanThread(Thread):
    def __init__(self, command):
        self.coords = [(random.randint(0, 1240), random.randint(0, 1024)) for i in xrange(int(command['numLocations']))]
        self.distance_matrix = []
        self.num_locations = int(command['numLocations'])
        self.num_generations = int(command['numGenerations'])
        self.room = command['room']
        self.images = []
        super(TravellingSalesmanThread, self).__init__()
    
    def solveTSP(self):
        print('try to solve TSP')

        def get_distance_matrix(coords):
            """ A distance matrix """
            matrix={}
            for i,(x1,y1) in enumerate(coords):
                for j,(x2,y2) in enumerate(coords):
                    dx, dy = x1-x2, y1-y2
                    dist=sqrt(dx*dx + dy*dy)
                    matrix[i,j] = dist
            return matrix

        def get_tour_length(matrix, tour):
            """ Returns the total length of the tour """
            total = 0
            t = tour.getInternalList()
            for i in range(self.num_locations):
                j      = (i+1)%self.num_locations
                total += matrix[t[i], t[j]]
            return total

        def G1DListTSPInitializator(genome, **args):
            """ The initializator for the TSP """
            lst = [i for i in xrange(genome.getListSize())]
            random.shuffle(lst)
            genome.setInternalList(lst)

            self.distance_matrix = get_distance_matrix(self.coords)

        def write_to_img(coords, tour, img_file):
            """ The function to plot the graph """
            padding=20
            coords=[(x+padding,y+padding) for (x,y) in coords]
            maxx,maxy=0,0
            for x,y in coords:
                maxx=max(x,maxx)
                maxy=max(y,maxy)
            maxx+=padding
            maxy+=padding
            img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))

            font=ImageFont.load_default()
            d=ImageDraw.Draw(img);
            num_cities=len(tour)
            for i in range(num_cities):
                j=(i+1)%num_cities
                city_i=tour[i]
                city_j=tour[j]
                x1,y1=coords[city_i]
                x2,y2=coords[city_j]
                d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
                d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))

            for x,y in coords:
                x,y=int(x),int(y)
                d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
            del d
            img.save(img_file, "PNG")
            self.images.append(imageio.imread(img_file))

            print "The plot was saved into the %s file." % (img_file,)

        def evolve_callback(ga_engine):
            if ga_engine.currentGeneration % 10 == 0:
                write_to_img(self.coords, ga_engine.bestIndividual(), "./app/gen_imgs/%s_%d.png" % (self.room, ga_engine.currentGeneration,))

        genome = G1DList.G1DList(len(self.coords))
        genome.evaluator.set(lambda chromosome: get_tour_length(self.distance_matrix, chromosome))
        genome.crossover.set(Crossovers.G1DListCrossoverEdge)
        genome.initializator.set(G1DListTSPInitializator)

        ga = GSimpleGA.GSimpleGA(genome)
        ga.setGenerations(self.num_generations)
        ga.setMinimax(Consts.minimaxType["minimize"])
        ga.setCrossoverRate(1.0)
        ga.setMutationRate(0.02)
        ga.setPopulationSize(80)
        ga.stepCallback.set(evolve_callback)

        ga.evolve(freq_stats=100)
        best = ga.bestIndividual()

        kargs = { 'duration': 2 }
        imageio.mimsave("./app/gifs/%s.gif"  % self.room, self.images, 'GIF', ** kargs)
        socketio.emit('server response', { 'gifUrl': "%s.gif" % (self.room,)}, namespace='/travelling-salesman', room=self.room, broadcast=False)

    def run(self):
        self.solveTSP()
