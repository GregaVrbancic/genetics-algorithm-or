export class App {
  configureRouter(config, router) {
    config.title = 'GA Project';
    config.map([
      { route: ['', '/'], moduleId: 'resources/elements/word-guess', name: 'WordGuess', title: ' - word guess'},
      { route: 'travelling-salesman', moduleId: 'resources/elements/travelling-salesman', name: 'TravellingSalesman', title: ' - travelling salesman'}
    ]);

    this.router = router;
  }
}
