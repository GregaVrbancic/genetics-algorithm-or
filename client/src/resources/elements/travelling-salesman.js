import io from 'socket.io-client';

export class TravellingSalesman {
  constructor() {
    this.title = 'Advanced Genetic Algorithm Example - Travelling Salesman';
    this.description = 'In this advanced example the genetic algorithm is used for solving travelling salesman problem.';
    this.info = 'The higher number of locations you set, the more difficult it is for genetic algorithm to solve the problem and also more time consuming it is.';
    this.room = '';
    this.numLocations = 30;
    this.numGenerations = 300;
    this.responses = [];
    this.running = false;
    this.showBest = false;
    this.socket = io.connect('/travelling-salesman');
  }

  activate() {
    this.socket.on('connected response', response => {
      console.log(response);
      this.room === '' ? this.room = response.room : this.room = this.room;
      this.socket.off('connected response');
    });
    this.socket.on('server response', response => {
      console.log('response: ' + JSON.stringify(response));
      this.running = false;
      this.response = response;
    });
  }

  detached() {
    this.socket.emit('leave', { room: this.room });
    this.room = '';
    this.socket.off('server response', function() {
      console.log('deactivate listener on "server response"');
    });
  }

  sendStartCommand() {
    this.responses = [];
    console.log('send start command - numLocations: ' + this.numLocations + ' - numGenerations: ' + this.numGenerations);
    this.running = true;
    this.socket.emit('start', { numLocations: this.numLocations, numGenerations: this.numGenerations, room: this.room });
  } 

  clickShowBest() {
    this.showBest = !this.showBest;
  }
}
