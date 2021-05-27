const express = require('express');
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

var location = 'docs';

app.get('/', function(request, response){
    response.sendFile(__dirname + '/' + location + '/index.html');
});

app.use(express.static(location))

app.listen(3000, () => {
  console.log("server running!");
})