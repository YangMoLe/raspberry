const http = require('node:http');
const createClient = require('oebb-hafas');
const hostname = '127.0.0.1';
const port = 2999;

const client = createClient("raspberrypi-kitchen")


const server = http.createServer((req, res) => {
  const from = '8100013';
  const to = '1190100';

  if (from && to) {
    client.journeys(from, to, { results: 3 })
      .then(journeys => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        console.log("ok")
        res.end(JSON.stringify(journeys));
      })
      .catch(error => {
        res.statusCode = 500;
        res.setHeader('Content-Type', 'text/plain');
        res.end('Internal Server Error\n');
        console.error(error);
      });
  } else {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Bad Request: from and to parameters are missing\n');
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
