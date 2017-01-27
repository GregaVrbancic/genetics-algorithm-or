import environment from './environment';

//Configure Bluebird Promises.
Promise.config({
  warnings: {
    wForgottenReturn: false
  }
});

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .plugin('aurelia-bootstrap')
    .plugin('aurelia-google-maps', config => {
      config.options({
        apiKey: 'AIzaSyDz0KY_Jg4jued9tqJCqxebCm0-BizLO6g', // use `false` to disable the key
        apiLibraries: 'drawing,geometry', //get optional libraries like drawing, geometry, ... - comma seperated list
        options: { panControl: true, panControlOptions: { position: 9 }, streetViewControl: false } //add google.maps.MapOptions on construct (https://developers.google.com/maps/documentation/javascript/3.exp/reference#MapOptions)
      });
    })
    .feature('resources');

  if (environment.debug) {
    aurelia.use.developmentLogging();
  }

  if (environment.testing) {
    aurelia.use.plugin('aurelia-testing');
  }

  aurelia.start().then(() => aurelia.setRoot());
}
