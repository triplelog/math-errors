'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const maincpp = require(binding);
//const postfix = require('./postfix.js');

//const mongoose = require('mongoose');
//mongoose.connect('mongodb://localhost:27017/matherrors', {useNewUrlParser: true});



const https = require('https');
//const http = require('http');
var fs = require("fs");
//var myParser = require("body-parser");
var qs = require('querystring');
const { exec } = require('child_process');
var nunjucks = require('nunjucks');
var crypto = require("crypto");
//var datatypes = require('./datatypes.js');

const options = {
  key: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/fullchain.pem')
};




//const User = require('./models/user');
//var passport = require('passport')
//var LocalStrategy = require('passport-local').Strategy;
// use static authenticate method of model in LocalStrategy
//passport.use(User.createStrategy());
 
// use static serialize and deserialize of model for passport session support
//passport.serializeUser(User.serializeUser());
//passport.deserializeUser(User.deserializeUser());

var express = require('express');


var app = express();
app.use('/',express.static('static'));


const server1 = https.createServer(options, app);
//const server1 = http.createServer(options, app);

server1.listen(12312);


app.get('/addition',
	function(req, res){
		
		res.write(nunjucks.render('topics/addition.html',{
		}));
		res.end();
	
    }
);



const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('\n');
}).listen(8080);

const WebSocket = require('ws');
//const wss = new WebSocket.Server({ port: 8080 , origin: 'http://tabdn.com'});
const wss = new WebSocket.Server({ server });
wss.on('connection', function connection(ws) {
  //ws.send();
  ws.on('message', function incoming(message) {
  	console.log(maincpp.addwrong("3123","691","3714"));
	console.log(maincpp.subtractwrong("612","498","224") );
  });
});
