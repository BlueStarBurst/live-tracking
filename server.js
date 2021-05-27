const express = require('express');
var fs = require('fs');
var http = require('http');
var https = require('https');
const app = new express();

const { networkInterfaces } = require('os');

const nets = networkInterfaces();
const results = Object.create(null); // Or just '{}', an empty object

//console.log(nets);

for (const name of Object.keys(nets)) {
  for (const net of nets[name]) {
    // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
    if (net.family === 'IPv4' && !net.internal) {
      if (!results[name]) {
        results[name] = [];
      }
      results[name].push(net.address);
      console.log(net.address);
    }
  }
}

console.log(results);

// var location = 'docs';

// app.get('/', function (request, response) {
//   console.log("GET")
//   response.sendFile(__dirname + '/' + location + '/index.html');
// });

// app.use(express.static(location))

const serverConfig = {
  key: fs.readFileSync(__dirname + '/server/key.pem'),
  cert: fs.readFileSync(__dirname + '/server/cert.pem'),
};

app.get('/', function(req, res) {
  res.sendFile(__dirname + '/docs/index.html');
});

app.use(express.static('docs'))

const httpsServer = https.createServer(serverConfig, app);
//httpsServer.listen(HTTPS_PORT, '0.0.0.0');

httpsServer.listen(443, () => {
  console.log("running!");
});

// app.listen(3000, () => {
//   console.log("server running!");
// })

// set up plain http server
var http = express();

// set up a route to redirect http to https
http.get('*', function(req, res) {  
    res.redirect('https://' + req.headers.host + req.url);

    // Or, if you don't want to automatically detect the domain name from the request header, you can hard code it:
    // res.redirect('https://example.com' + req.url);
})

// have it listen on 8080
http.listen(80);