var https = require('http');

var express = require('express');
var express = require('express');

// set up plain http server
var http = express();

http.get('/', function (req, res) {
    res.redirect('https://' + req.headers.host + req.url);
})

// have it listen on 8080
http.listen(80);