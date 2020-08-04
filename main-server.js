'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);

//const postfix = require('./postfix.js');

const mongoose = require('mongoose');
mongoose.connect('mongodb://matherrors:kZGWGda3A@localhost:27017/matherrors', {useNewUrlParser: true});
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
const SubjectData = require('./models/subjects');
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
  		console.log(performance.now());
		var dm = JSON.parse(message);
		console.log(performance.now());
		if (dm.operation == 'key'){
			if (tempKeys[dm.message]){
				username = tempKeys[dm.message].username;
			}
		}
		else if (dm.type == 'question'){
			console.log(performance.now());
			var stdout = maincpp.question();
			console.log(performance.now(), question);

			console.log(performance.now());
			var jsonmessage = {'type':'question','question':stdout};
			ws.send(JSON.stringify(jsonmessage));
			stdout = maincpp.answers();
			console.log(stdout);
		}
		else if (dm.type == 'solve'){//TODO: redo this whole thing
			console.log(performance.now());
			var question = dm.question;
			console.log(performance.now());
			var stdout = maincpp.question();
			console.log(performance.now(), question);
			var outStr = "";
		
			var len = stdout.length;
			var nodeStr = "......";
			var inAction = false;
		
			var idx = 0;
			var allStrings = [];
			var allSteps = [];
			for (var i=0;i<len;i++){
				nodeStr += stdout[i];
				nodeStr = nodeStr.substring(1,7);
	
				if (nodeStr == "-DOJS-"){
					inAction = true;
				}
				else if (nodeStr == "-ODJS-"){
					inAction = false;
				
					outStr = outStr.replace("#tree-simple","#tree-simple"+idx);
					outStr = outStr.replace("var chart =","var chart"+idx+" =");
					outStr = outStr.substring(0,outStr.length-5);
					allStrings.push(outStr);
					allSteps.push("node"+i);
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
			var jsonmessage = {'type':'answer','answer':outStr};
			ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'check'){
			console.log(performance.now());
			var stdout = maincpp.check(dm.answer);
			console.log(performance.now(), dm.answer);
			stdout = maincpp.solution(dm.answer);
			console.log(performance.now());
			var outStr = "";
		
			var len = stdout.length;
			var nodeStr = "......";
			var inAction = false;
		
			var idx = 0;
			var allStrings = [];
			var allSteps = [];
			for (var i=0;i<len;i++){
				nodeStr += stdout[i];
				nodeStr = nodeStr.substring(1,7);
	
				if (nodeStr == "-DOJS-"){
					inAction = true;
				}
				else if (nodeStr == "-ODJS-"){
					inAction = false;
				
					outStr = outStr.replace("#tree-simple","#tree-simple"+idx);
					outStr = outStr.replace("var chart =","var chart"+idx+" =");
					outStr = outStr.substring(0,outStr.length-5);
					allStrings.push(outStr);
					allSteps.push("node"+i);
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
			var jsonmessage = {'type':'answer','answer':outStr};
			ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'auto'){
			console.log(performance.now());
			var stdout = maincpp.auto(dm.answer);
			var outArray = [];
			eval(stdout);
			console.log(performance.now(), dm.answer);
			var jsonmessage = {'type':'auto',answer:dm.answer,'auto':outArray};
			ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'previewQuestion'){
			if (dm.qstr.length >= 10000){
				return;
			}
			var qh = maincpp.previewQuestion(dm.qstr);
			
			var jsonmessage = {'type':'preview','preview':qh};
			ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'saveQuestion'){
			if (dm.qstr.length >= 10000){
				return;
			}
			fs.appendFile('questions/de/default.csv', "\n"+dm.qstr, function (err) {
			  if (err) throw err;
			});
			
			//var jsonmessage = {'type':'created'};
			//ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'saveRule'){
			var subject = dm.subject;
			var topic = dm.topic;
			console.log(subject);
			console.log(topic);
			SubjectData.findOne({subject:subject}, function(err,result) {
				if (result == null){
					var topics = {};
					topics[topic]={name:"",explanation:"",rules:[]};
					var subjectData = new SubjectData({subject:subject,topics:topics});
					subjectData.save(function(err,result){
						console.log("error creating: ",err);
					});
				}
				else {
					result.topics[topic]={name:"",explanation:"",rules:[]};
					result.markModified('topics');
					result.save(function(err,result){
						console.log("error updating: ",err);
					});
				}
			});
				

			
			
			
			//var jsonmessage = {'type':'created'};
			//ws.send(JSON.stringify(jsonmessage));
		}
		
  	});
});

var startTime = performance.now();

const maincpp = require(binding);
var retHello = maincpp.hello();
var rules = [];
eval(retHello);
console.log("hello?: ",retHello);
console.log(startTime, performance.now(), rules.length);

app.get('/question',
	function(req, res){
		
		
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));
		res.write(nunjucks.render('templates/question.html',{

		}));
		res.end();

		
	
    }
    
);
app.get('/createquestion',
	function(req, res){
		
		
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));
		res.write(nunjucks.render('templates/createquestion.html',{

		}));
		res.end();

		
	
    }
    
);
app.get('/createrule',
	function(req, res){
		
		
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));
		res.write(nunjucks.render('templates/createrule.html',{

		}));
		res.end();

    }
    
);
app.get('/topic',
	function(req, res){
		
		
		res.write(nunjucks.render('templates/topic.html',{
			rules: rules,
		}));
		res.end();
	}
);
app.get('/history',
	function(req, res){
		
		var questions = [];
		var question = {};
		question.id = 0;
		question.question = "Why?";
		question.answer = "42";
		question.errors = ["yes","no"];
		questions.push(question);
		question.grade = "☹️";
		
		question = {};
		question.id = 1;
		question.question = "When?";
		question.answer = "42";
		question.errors = ["one","two"];
		question.grade = "🤔";
		questions.push(question);
		res.write(nunjucks.render('templates/history.html',{
			questions: questions,
		}));
		res.end();
	}
);



