var mysql = require('mysql');
var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');
const fs = require('file-system');
const bcrypt = require('bcrypt');
const http = require('http');

var connection = mysql.createConnection({
	host     : '51.77.201.156',
	user     : 'guivdh',
	password : 'BKD6Vccy9SPRx56k',
	database : 'nodelogin'
});

var app = express();

app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));

app.use(bodyParser.urlencoded({extended : true}));
app.use(bodyParser.json());

app.get('/', function(request, response) {
	response.sendFile(path.join(__dirname + '/login.html'));
});

app.post('/auth', function(request, response) {
	var username = request.body.username;
	var password = request.body.password;
	if (username && password) {
		connection.query("SELECT * FROM nodelogin.accounts WHERE username = " + "'" + username + "'", function(error, results, fields) {
			bcrypt.compare(password, results[0]['password'], function(err, res) {
				if(res == false) {
					response.send('Incorrect Username and/or Password!');
				} else {
					request.session.loggedin = true;
					request.session.username = username;
					response.redirect('/home');
				}
				response.end();
			});
		});
	} else {
		response.send('Please enter Username and Password!');
		response.end();
	}
});

app.get('/nbrBots', function (request, response) {
	if (request.session.loggedin) {
		connection.query("SELECT count(id) as 'nbrBots' from master.request;", function (err, result, fields) {
			if (err) throw err;
			response.setHeader('Content-Type', 'application/json');
			response.end(JSON.stringify(result));
		});
	} else {
		response.send('Please login to view this page!');
	}
})

app.get('/requests', function (request, response) {
	if (request.session.loggedin) {
		connection.query("SELECT * from master.request;", function (err, result, fields) {
			if (err) throw err;
			response.setHeader('Content-Type', 'application/json');
			response.end(JSON.stringify(result));
		});
	} else {
		response.send('Please login to view this page!');
	}
})

app.get('/home', function(request, response) {
	if (request.session.loggedin) {
		data =fs.readFileSync('./content/index.html', 'utf8');
		response.send(data);
	} else {
		response.send('Please login to view this page!');
	}
	response.end();
});

app.listen(3000);