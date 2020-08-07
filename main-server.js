'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const bindingA = require.resolve(`./build/Release/bindingA`);

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
			var stdout = maincpp.question("algebra");
			console.log(performance.now(), question);

			console.log(performance.now());
			var jsonmessage = {'type':'question','question':stdout};
			ws.send(JSON.stringify(jsonmessage));
			stdout = maincpp.answers();
			console.log(stdout);
		}
		else if (dm.type == 'check'){
			console.log(performance.now());
			var stdout = maincppa.check(dm.answer);
			console.log(performance.now(), dm.answer);
			stdout = maincppa.solution(dm.answer);
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
			var stdout = maincppa.auto(dm.answer);
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
		else if (dm.type == 'makeanswers'){
			console.log("___",performance.now());
			var outS = maincppa.makeanswers("Hello");
			console.log("___",outS,performance.now());
			
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
			var subject = dm.subject.toLowerCase();
			var topic = dm.topic.toLowerCase();
			var name = dm.name.toLowerCase();
			var explanation = dm.explanation;
			var instructions = dm.instructions;
			console.log(subject);
			console.log(topic);
			SubjectData.findOne({subject:subject}, function(err,result) {
				if (result == null){
					var topics = {};
					topics[topic]=[{name:name,explanation:explanation,instructions:instructions}];
					var subjectData = new SubjectData({subject:subject,topics:topics});
					subjectData.save(function(err,result){
						if (err){
							console.log("error: ", err);
						}
						else {
							console.log(JSON.stringify(topics[topic]));
						}
					});
				}
				else {
					var foundMatch = false;
					if (result.topics[topic]){
						for (var i=0;i<result.topics[topic].length;i++){
							if (result.topics[topic][i].name == name){
								result.topics[topic][i] = {name:name,explanation:explanation,instructions:instructions};
								foundMatch = true;
								break;
							}
						}
						if (!foundMatch){
							result.topics[topic].push({name:name,explanation:explanation,instructions:instructions});
						}
					}
					else {
						result.topics[topic] = [{name:name,explanation:explanation,instructions:instructions}];
					}
					
					
					result.markModified('topics');
					result.save(function(err,result){
						if (err){
							console.log("error: ", err);
						}
						else {
							console.log(JSON.stringify(result.topics[topic]));
						}
					});
				}
			});
				

			
			
			
			//var jsonmessage = {'type':'created'};
			//ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'deleteRule'){
			var subject = dm.subject.toLowerCase();
			var topic = dm.topic.toLowerCase();
			var name = dm.name.toLowerCase();
			var explanation = dm.explanation;
			var instructions = dm.instructions;
			console.log(subject);
			console.log(topic);
			SubjectData.findOne({subject:subject}, function(err,result) {
				if (result == null){
					
				}
				else {
					var foundMatch = false;
					for (var i=0;i<result.topics[topic].length;i++){
						if (result.topics[topic][i].name.toLowerCase() == name){
							result.topics[topic].splice(i,1);
							foundMatch = true;
							break;
						}
					}
					if (!foundMatch){
						return;
					}
					
					result.markModified('topics');
					result.save(function(err,result){
						if (err){
							console.log("error: ", err);
						}
						else {
							console.log(JSON.stringify(result.topics[topic]));
						}
					});
				}
			});
				
		}
		
  	});
});

var startTime = performance.now();

const maincpp = require(binding);
var retHello = maincpp.hello();
const maincppa = require(bindingA);
var retHelloA = maincppa.hello();
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
app.get('/questiona',
	function(req, res){
		
		
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));
		res.write(nunjucks.render('templates/answer.html',{

		}));
		res.end();

		
	
    }
    
);
app.get('/createquestion',
	function(req, res){
		
		
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));
		SubjectData.find({}, function(err,result) {
			res.write(nunjucks.render('templates/createquestion.html',{
			
			}));
			res.end();
			
		
		});
		

		
	
    }
    
);
app.get('/createrule',
	function(req, res){
		
		var info = {};
		var correct = [];
		var errors = [];
		var examples = [];
		var dewey = '';
		if (req.query && req.query.s && req.query.t && req.query.r){
			dewey += req.query.s.toLowerCase() + '.';
			dewey += req.query.t.toLowerCase() + '.';
			dewey += req.query.r.toLowerCase();
		}
		console.log(performance.now());
		//var jsonmessage = {'type':'imageSrc','src':inSrc.replace('static/','../')};
		//ws.send(JSON.stringify(jsonmessage));

		SubjectData.find({}, function(err,result) {
			var subjects = [];
			for (var i=0;i<result.length;i++){
				subjects.push(result[i]);
				for (var topic in result[i].topics){
					for (var r=0;r<result[i].topics[topic].length;r++){
						var rule = result[i].topics[topic][r];
						var thisDewey = result[i].subject + '.' + topic + '.' + rule.name;
						console.log(thisDewey,dewey);
						if (thisDewey == dewey){
							info = {subtop:result[i].subject + '.'+topic,name:rule.name,explanation:rule.explanation};
							console.log(info);
							for (var ii=0;ii<rule.instructions.length;ii++){
								if (rule.instructions[ii].split(',')[2]=="c"){
									correct.push(rule.instructions[ii]);
								}
								else if (rule.instructions[ii].split(',')[2]=="e" || rule.instructions[ii].split(',')[2]=="i"){
									errors.push(rule.instructions[ii]);
								}
								else if (rule.instructions[ii].split(',')[2]=="x"){
									examples.push(rule.instructions[ii]);
								}
							}
							
						}
					}
				}
				
			}
			res.write(nunjucks.render('templates/createrule.html',{
				subjects: subjects,
				info: info,
				correct:correct,
				errors:errors,
				examples:examples,
			}));
			res.end();
			for (var i=0;i<result.length;i++){
				subjects.push(result[i]);
				var csvStr = "";
				for (var topic in result[i].topics){
					for (var r=0;r<result[i].topics[topic].length;r++){
						var rule = result[i].topics[topic][r];
						csvStr += "Rule,"+result[i].subject+"."+topic+"."+rule.name+","+rule.explanation+"\n";
						for (var ii=0;ii<rule.instructions.length;ii++){
							csvStr += rule.instructions[ii]+"\n";
						}
					}
				}
				fs.writeFile('cpp/subjects/'+result[i].subject+".csv", csvStr, function (err) {});
			}
			
		
		});

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



