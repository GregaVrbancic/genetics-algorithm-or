import io from 'socket.io-client';

export class WordGuess {
  constructor() {
    this.title = 'Basic Genetic Algorithm Example';
    this.description = 'In this example the genetic algorithm is used for guessing the sequence of letters.';
    this.info = 'The longer is sequence of letters, more difficult it is for genetic algorithm to "guess" it and also more time consuming it is.';
    this.instruction = 'Type in few words and click run!';
    this.responses = [];
    this.sequence = '';
    this.room = '';
    this.socket = io.connect('http://localhost:5000/word-guess');
  }

  attached() {
    this.socket.on('connected response', response => {
      console.log(response);
      this.room === '' ? this.room = response.room : this.room = this.room;
      this.socket.off('connected response');
    });
    this.socket.on('server response', response => this.responses.unshift(response));
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
    console.log('send start command: ' + this.sequence);
    this.socket.emit('start', { command: this.sequence, room: this.room });
  }
}
