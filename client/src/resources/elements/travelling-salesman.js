import io from 'socket.io-client';
import { HttpClient } from 'aurelia-fetch-client';

let httpClient = new HttpClient();

export class TravellingSalesman {
  constructor() {
    this.title = 'Advanced Genetic Algorithm Example - Travelling Salesman';
    this.description = 'In this advanced example the genetic algorithm is used for solving travelling salesman problem.';
    this.info = 'The more markers you set on the map, more difficult it is for genetic algorithm to solve the problem and also more time consuming it is.';
    this.instruction = 'Select at least 3 locations on map and then click run!';
    this.showSpinner = true;
    this.showError = false;
    this.geolocation = null;
    // this.markers = [];
    this.markers = [
      { id: 0, title: 'Location1', latitude: 46.36683133695191, longitude: 15.395643711090088 },
      { id: 1, title: 'Location2', latitude: 46.37725420510028, longitude: 15.791151523590088 },
      { id: 2, title: 'Location3', latitude: 46.51304304047058, longitude: 15.894148349761963 },
      { id: 3, title: 'Location4', latitude: 46.45488927067796, longitude: 15.763685703277588 },
      { id: 4, title: 'Location5', latitude: 46.544694144765536, longitude: 15.687628984451294 },
      { id: 5, title: 'Location5', latitude: 46.53926280368402, longitude: 15.626860857009888 }
    ];
    this.idCounter = 0;
    this.room = '';
    this.responses = [];
    this.socket = io.connect('/travelling-salesman');
    this.osmUrl = 'http://router.project-osrm.org/table/v1/driving/';
  }

  activate() {
    this.socket.on('connected response', response => {
      console.log(response);
      this.room === '' ? this.room = response.room : this.room = this.room;
      this.socket.off('connected response');
    });
    this.socket.on('server response', response => this.responses.unshift(response));
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((location) => {
        this.geolocation = location;
        this.showSpinner = false;
      }, (error) => {
        this.setDefaultLocation();
        this.showSpinner = false;
      });
    } else {
      this.setDefaultLocation();
      this.showSpinner = false;
    }
  }

  detached() {
    this.socket.emit('leave', { room: this.room });
    this.room = '';
    this.socket.off('server response', function() {
      console.log('deactivate listener on "server response"');
    });
  }

  setDefaultLocation() {
    return {
      coords: {
        latitude: 37.323,
        longitude: -122.0527,
        accuracy: 0
      }
    };
  }

  mapClickHandler(event) {
    if (event.detail) {
      this.markers.unshift({
        id: this.idCounter,
        latitude: event.detail.latLng.lat(),
        longitude: event.detail.latLng.lng(),
        title: 'Location ' + (this.idCounter + 1),
        infoWindow: {
          content: `
                <div id="content">
                  <div id="siteNotice"></div>
                  <h4 class="marker">Location ` + (this.idCounter + 1) + `</h4>
                  <div id="bodyContent">
                    <ul class="list-unstyled">
                      <li>Latitude: ` + event.detail.latLng.lat() + `</li>
                      <li>Longitude: ` + event.detail.latLng.lng() + `</li>
                    </ul>
                  </div>
                </div>`
        }
      });
      this.idCounter++;
    }
  }

  deleteMarker(marker) {
    console.log('delete marker with id: ' + marker.id);

    this.markers.splice(this.markers.findIndex((el) => {
      return el.id === marker.id;
    }), 1);
  }

  sendStartCommand() {
    console.log('obtaing distance table');
    let query = '';
    for (let i = 0; i < this.markers.length; i++) {
      query += this.markers[i].latitude + ',' + this.markers[i].longitude;
      if (i !== this.markers.length - 1) {
        query += ';';
      }
    }
    httpClient.fetch(this.osmUrl + query)
      .then(response => response.json())
      .then(data => {
        if (data.code === 'Ok') {
          this.socket.emit('start', { locations: this.markers, durations: data.durations, room: this.room });
        } else {
          this.showError = true; 
        }
      });
  } 
}
