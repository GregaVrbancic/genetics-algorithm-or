import io from 'socket.io-client';
//var socket = io('http://localhost:5000');

export class WordGuess {
  constructor() {
    this.title = 'Basic Genetic Algorithm Example';
    this.description = 'In this example the genetic algorithm is used for guessing the sequence of letters.';
    this.info = 'The longer is sequence of letters, more difficult is for genetic algorithm to "guess" it and also more time consuming it is.';
    this.responses = [];
    this.socket = io.connect('http://localhost:5000/word-guess');
  }

  activate() {
    this.socket.on('server response', response => this.responses.push(response));
  }

  deactivate() {
    this.socket.off('server response', function() {
      console.log('deactivate listener on "server response"');
    });
  }

  sendStartCommand() {
    console.log('send start command');
    this.socket.emit('start', {command: 'bla bla bla'});
  }
}
