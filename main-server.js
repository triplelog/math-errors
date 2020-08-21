'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const bindingA = require.resolve(`./build/Release/bindingA`);
const bindingP = require.resolve(`./build/Release/bindingP`);

//const postfix = require('./postfix.js');



var fromLogin = require('./login-server.js');
var app = fromLogin.loginApp;
var tempKeys = fromLogin.tempKeys;
var mymongoose = fromLogin.mongoose;


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


const katex = require('katex');
const markdown = require('markdown-it');
var mdoptions = require('./mathdocs/markdown-it-rules.js')("");
var md = new markdown();




const User = require('./models/user');
//const SubjectData = require('./models/subjects');
var schema = new mymongoose.Schema({subject: String, topics:{}});
var SubjectData = mymongoose.model('SubjectData', schema);

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
			var jsonmessage = {'type':'question','question':outS};
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
		else if (dm.type == 'saveLesson'){
			var subject = dm.subject.toLowerCase();
			var topic = dm.topic.toLowerCase();
			var slug = dm.slug.toLowerCase();
			var lesson = dm.lesson;
			
			
			console.log(subject);
			console.log(topic);
			SubjectData.findOne({subject:subject}, function(err,result) {
				if (result == null){
					var topics = {};
					topics[topic]=[{slug:slug,lesson:lesson}];
					SubjectData.create({subject:subject,topics:topics},function(err,result){
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
							if (result.topics[topic][i].slug == slug){
								result.topics[topic][i] = {slug:slug,lesson:lesson};
								foundMatch = true;
								break;
							}
						}
						if (!foundMatch){
							result.topics[topic].push({slug:slug,lesson:lesson});
						}
					}
					else {
						result.topics[topic] = [{slug:slug,lesson:lesson}];
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
		/*
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
				
		}*/
		else if (dm.type == 'previewText'){
			var html = "";
			var jsonmessage;
			if (dm.rules){
				md.use(require('@gerhobbelt/markdown-it-container'), 'rule' , mdoptions);
				html = md.render('::: rule\n'+dm.rules+'\n:::\n');
				console.log(html);
				jsonmessage ={'type':'previewText','rules':html};
			}
			else if (dm.errors){
				md.use(require('@gerhobbelt/markdown-it-container'), 'rule' , mdoptions);
				html = md.render('::: error\n'+dm.errors+'\n:::\n');
				console.log(html);
				jsonmessage ={'type':'previewText','errors':html};
			}
			else if (dm.examples){
				console.log(dm.lesson);
				var mdoptions2 = require('./mathdocs/markdown-it-rules.js')(dm.lesson);
				md.use(require('@gerhobbelt/markdown-it-container'), 'rule' , mdoptions2);
				html = md.render('::: example '+dm.examples+' :::\n');
				console.log(html);
				jsonmessage ={'type':'previewText','examples':html};
			}
			ws.send(JSON.stringify(jsonmessage));
		}
		else if (dm.type == 'previewLesson'){
			var html = "";
			var jsonmessage;
			console.log(dm.message);
			var mdoptions2 = require('./mathdocs/markdown-it-rules.js')(dm.message);
			md.use(require('@gerhobbelt/markdown-it-container'), 'rule' , mdoptions2);
			html = md.render(dm.message);
			jsonmessage ={'type':'previewLesson','message':html};

			ws.send(JSON.stringify(jsonmessage));
		}
		
  	});
});

var startTime = performance.now();

const maincpp = require(binding);
var retHello = maincpp.hello();
const maincppa = require(bindingA);
var retHelloA = maincppa.hello();
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
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

		
app.get('/createlesson',
	function(req, res){
		
		var info = {};
		var correct = [];
		var errors = [];
		var examples = [];
		var dewey = '';
		if (req.query && req.query.s && req.query.t && req.query.l){
			dewey += req.query.s.toLowerCase() + '.';
			dewey += req.query.t.toLowerCase() + '.';
			dewey += req.query.l.toLowerCase();
		}
		console.log(performance.now());
		

		var html = "";

		SubjectData.find({subject:dewey.split('.')[0]}, function(err,result) {
			var lesson = "";
			for (var i=0;i<result.length;i++){
				console.log(result[i].topics);
				if (result[i].topics[dewey.split('.')[1]]){
					
					var arr = result[i].topics[dewey.split('.')[1]];
					for (var ii=0;ii<arr.length;ii++){
						console.log(arr[ii]);
						if (arr[ii].slug == dewey.split('.')[2]){
							lesson = arr[ii].lesson;
						}
					}
				}
			}
			console.log(lesson);
			var json = {};
			if (lesson && lesson != ""){
				json = parseLesson(lesson);
			}
			console.log(json);
			res.write(nunjucks.render('templates/createlesson.html',{
				info: json.info,
				rules: json.rules,
				errors: json.errors,
				examples: json.examples,
			}));
			res.end();
			/*
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
			*/
			
		
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


function parseLesson(lesson){
	var lines = lesson.split('\n');
	var rules = [];
	var errors = [];
	var examples = [];
	var currentType = "explanation";
	var currentToken = "";
	var info = {};
	for (var i=0;i<lines.length;i++){
		if (lines[i].substr(0,3) == ":::"){
			if (currentType == "" || currentType == "explanation"){
				if (currentType == "explanation"){
					info.explanation = currentToken;
				}
				if (lines[i].match(/rule/)){
					currentType = "rule"; currentToken = "";
					continue;
				}
				else if (lines[i].match(/error/)){
					currentType = "error"; currentToken = "";
					continue;
				}
				else if (lines[i].match(/example/)){
					currentType = "example"; currentToken = "";
					continue;
				}
			}
			else if (currentType == "rule"){
				rules.push(currentToken);
				currentType = ""; currentToken = "";
			}
			else if (currentType == "error"){
				errors.push(currentToken);
				currentType = ""; currentToken = "";
			}
			else if (currentType == "example"){
				examples.push(currentToken);
				currentType = ""; currentToken = "";
			}
		}
		else if (lines[i].substr(0,10) == ":subtople:"){
			info.subtople = lines[i].substr(10).trim();
			currentType = "explanation"; currentToken = "";
		}
		else if (lines[i].substr(0,6) == ":name:"){
			info.name = lines[i].substr(6).trim();
			currentType = "explanation"; currentToken = "";
		}
		else {
			currentToken += lines[i]+'\n';
		}
	}
	return {rules:rules,errors:errors,examples:examples,info:info};
}


