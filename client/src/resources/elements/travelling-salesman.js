import { HttpClient } from 'aurelia-fetch-client';

let httpClient = new HttpClient();

export class TravellingSalesman {
  constructor() {
    this.title = 'Advanced Genetic Algorithm Example - Travelling Salesman';
    this.description = 'In this advanced example the genetic algorithm is used for solving travelling salesman problem.';
    this.info = 'The more markers you set on the map, more difficult it is for genetic algorithm to solve the problem and also more time consuming it is.';
    this.instruction = 'Select at least 3 locations on map and then click run!';
    this.showSpinner = true;
    this.geolocation = null;
    this.markers = [];
    this.idCounter = 0;
    this.osmUrl = 'http://router.project-osrm.org/table/v1/driving/';
  }

  activate() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((location) => {
        this.geolocation = location;
        this.showSpinner = false;
      }, (error) => {
        setDefaultLocation();
        window.google.maps.event.trigger(this.map, 'resize');
        this.showSpinner = false;
      });
    } else {
      setDefaultLocation();
      this.showSpinner = false;
    }
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
    for(var i = 0; i < this.markers.length; i++) {
      query += this.markers[i].latitude + ',' + this.markers[i].longitude;
      if (i !== this.markers.length - 1) {
        query += ';';
      }
    }
    httpClient.fetch(this.osmUrl + query)
      .then(response => response.json())
      .then(data => {
         console.log(data);
      });
  } 
}
