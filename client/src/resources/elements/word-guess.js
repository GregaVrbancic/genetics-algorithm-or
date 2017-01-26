import io from 'socket.io-client';
//var socket = io('http://localhost:5000');

export class WordGuess {
  constructor() {
    this.value = 'This is word guess GA component';
    this.socket = io.connect('http://localhost:5000/io');
  }

  activate() {
    this.socket.on('server response', function(response) {
      console.log('response: ' + response);
    });
  }

  deactivate() {
    this.socket.off('server response', function() {
      console.log('deactivate listener on "server response"');
    });
  }

  sendEmit() {
    console.log('sendEmit!');
    this.socket.emit('my event', {data: 'something for you!'});
  }
}
