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

const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('\n');
}).listen(8080);

const WebSocket = require('ws');
//const wss = new WebSocket.Server({ port: 8080 , origin: 'http://tabdn.com'});
const wss = new WebSocket.Server({ server });
wss.on('connection', function connection(ws) {
  var jsonmessage = [["323","691"],['','','',''],['','','','']];
  ws.send(JSON.stringify(jsonmessage));
  ws.on('message', function incoming(message) {
    var dm = JSON.parse(message);
	console.log(maincpp.addwrong(dm[0],dm[1],dm[2]));
	var x = ""+Math.floor(Math.random() * 1000);
	var y = ""+Math.floor(Math.random() * 1000);
	var jsonmessage = [[x,y],['','','',''],['','','','']];
  	ws.send(JSON.stringify(jsonmessage));
  });
});


app.get('/addition',
	function(req, res){
		var trophies = {'nocarry':false,'onecarry':false,'twocarries':false};
		//nocarry is miss 1 of 1
		//onecarry is miss exactly 1 of 2
		//twocarries is miss 2 of 2
		res.write(nunjucks.render('topics/arithmetic.html',{
			type: 'Addition',
		}));
		res.end();
	
    }
    
);
app.get('/subtraction',
	function(req, res){
		var trophies = {'noborrow':false,'oneborrow':false,'twoborrows':false};
		res.write(nunjucks.render('topics/arithmetic.html',{
			type: 'Subtraction',
		}));
		res.end();
	
    }
    
);





