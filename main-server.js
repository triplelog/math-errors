'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const maincpp = require(binding);
//const postfix = require('./postfix.js');

const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/matherrors', {useNewUrlParser: true});
var fromLogin = require('./login-server.js');
var app = fromLogin.loginApp;
var tempKeys = fromLogin.tempKeys;


const https = require('https');
var fs = require("fs");
var myParser = require("body-parser");
var qs = require('querystring');
const { exec } = require('child_process');
var nunjucks = require('nunjucks');
var crypto = require("crypto");

const options = {
  key: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/fullchain.pem')
};




const User = require('./models/user');
var passport = require('passport')
var LocalStrategy = require('passport-local').Strategy;
// use static authenticate method of model in LocalStrategy
passport.use(User.createStrategy());
 
// use static serialize and deserialize of model for passport session support
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

var express = require('express');

app.use('/',express.static('static'));


const server1 = https.createServer(options, app);

server1.listen(12313);

const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('\n');
}).listen(8081);

const WebSocket = require('ws');
//const wss = new WebSocket.Server({ port: 8080 , origin: 'http://tabdn.com'});
const wss = new WebSocket.Server({ server });
wss.on('connection', function connection(ws) {
	var username = '';
  	ws.on('message', function incoming(message) {
		var dm = JSON.parse(message);
		if (dm.operation == 'key'){
			if (tempKeys[dm.message]){
				username = tempKeys[dm.message].username;
			}
		}
		else if (dm.type == 'solve'){
			
		}
		
  	});
});


app.get('/tree',
	function(req, res){
		
		var wget = "./cpp/a.out 2+2";
		if (req.query && req.query.q){
			wget = "./cpp/a.out \""+req.query.q+"\"";
		}
		console.log(performance.now(), wget);
		var outStr = "";
		var child = exec(wget, function(err, stdout, stderr) {
			if (err){
				console.log(err);
				//send message--likely file size limit
				res.write(nunjucks.render('templates/bootstrap.html',{
					tree: "",
				}));
				res.end();
				return;
			}
			else {
		
				var len = stdout.length;
				console.log(performance.now(), len);
				var nodeStr = "......";
				var inAction = false;
				
				var idx = 0;
				var allStrings = [];
				for (var i=0;i<len;i++){
					nodeStr += stdout[i];
					nodeStr = nodeStr.substring(1,7);
			
					if (nodeStr == "-DOJS-"){
						console.log("Hi");
						inAction = true;
					}
					else if (nodeStr == "-ODJS-"){
						inAction = false;
						
						outStr = outStr.replace("#tree-simple","#tree-simple"+idx);
						outStr = outStr.replace("var chart =","var chart"+idx+" =");
						outStr = outStr.substring(0,outStr.length-5);
						allStrings.push(outStr);
						idx++;
						outStr = "";
					}
					else if (inAction){
						outStr += stdout[i];
					}
				}
				
				//console.log(allStrings);
				outStr =  "";
				for (var i=0;i<allStrings.length;i++){
					outStr += allStrings[i];
				}
				console.log(performance.now());
				//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
				//ws.send(JSON.stringify(jsonmessage));
				res.write(nunjucks.render('templates/bootstrap.html',{
					tree: outStr,
					nTrees: allStrings.length,
				}));
				res.end();
		
			}

		});
		
		
	
    }
    
);


