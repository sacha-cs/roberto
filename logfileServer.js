http = require('http');
fs = require('fs');

port = 8080;

http.createServer(function(req, res) {
    res.writeHead(200);
    fs.createReadStream('../BrickPi/logfile').pipe(res);
}).listen(port);

