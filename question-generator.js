'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const bindingP = require.resolve(`./build/Release/bindingP`);


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
var iterator = require('markdown-it-for-inline');
var repmath = require('./mathdocs/markdown-it-math.js');
var md = new markdown();
md.use(require('./mathdocs/markdown-it-input.js'));




var schema = new mymongoose.Schema({subject: String, topics:{}});
var SubjectData = mymongoose.model('SubjectData', schema);
schema = new mymongoose.Schema({subject: String, topics:{}});
var QuestionData = mymongoose.model('QuestionData', schema);



var startTime = performance.now();

const maincpp = require(binding);
var retHello = maincpp.hello();
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
var rules = [];
eval(retHello);
console.log("hello?: ",retHello);
console.log(startTime, performance.now(), rules.length);


QuestionData.find({}, function(err,result) {
	for (var i=0;i<result.length;i++){
		var subject = result[i].subject;
		var topics = Object.keys(result[i].topics);
		for (var ii=0;ii<topics.length;ii++){
			var topic = topics[ii];

			var arr = result[i].topics[topic];
			for (var iii=0;iii<arr.length;iii++){
				var lesson = arr[iii].lesson;
				var question = arr[iii].question;
				console.log(question);
			
			}
		}
	}
});

function makeTOC() {
	toc = {};
	SubjectData.find({}, function(err,result) {
		for (var i=0;i<result.length;i++){
			var subject = result[i].subject;
			if (toc[subject]){
			
			}
			else {
				toc[subject] = {};
			}
			var topics = Object.keys(result[i].topics);
			for (var ii=0;ii<topics.length;ii++){
				var topic = topics[ii];
				if (toc[result[i].subject][topic]){
			
				}
				else {
					toc[result[i].subject][topic] = [];
				}
				var arr = result[i].topics[topic];
				for (var iii=0;iii<arr.length;iii++){
					var lesson = arr[iii].slug;
					toc[result[i].subject][topic].push(lesson);
				
				}
			}
		}
		console.log(toc);
	});
	
}
var toc = {};
makeTOC();
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
					currentType = "examples"; currentToken = "";
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
			else if (currentType == "examples"){
				var liness = currentToken.split("\n");
				for (var ii=0;ii<liness.length;ii++){
					if (liness[ii].trim().length>0){
						examples.push(liness[ii].trim());
					}
				}
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

function parseQuestion(input){
	var lines = input.split('\n');
	var question = {comp:"",constants:[]};
	var answer = {comp:"",constraints:[]};
	var tags = [];
	var layout = "";
	var currentType = "";
	var currentToken = "";
	var info = {};
	for (var i=0;i<lines.length;i++){
		if (lines[i].substr(0,3) == ":::"){
			if (currentType == ""){
				if (lines[i].match(/question/)){
					currentType = "question"; currentToken = "";
					question.comp = lines[i+1];
					answer.comp = lines[i+2];
					i+=2;
					continue;
				}
				else if (lines[i].match(/answer/)){
					currentType = "answer"; currentToken = "";
					continue;
				}
				else if (lines[i].match(/tag/)){
					currentType = "tags"; currentToken = "";
					continue;
				}
				else if (lines[i].match(/layout/)){
					currentType = "layout"; currentToken = "";
					continue;
				}
			}
			else if (currentType == "question"){
				currentToken = currentToken.replace("\n\n","\n").trim();
				question.constants = currentToken.split("\n");
				currentType = ""; currentToken = "";
			}
			else if (currentType == "answer"){
				answer.constraints.push(currentToken.replace("\n\n","\n").trim());
				currentType = ""; currentToken = "";
			}
			else if (currentType == "tags"){
				tags = currentToken.split("\n");
				currentType = ""; currentToken = "";
			}
			else if (currentType == "layout"){
				layout = currentToken;
				currentType = ""; currentToken = "";
			}
		}
		else if (lines[i].substr(0,10) == ":subtople:"){
			info.subtople = lines[i].substr(10).trim();
			currentType = ""; currentToken = "";
		}
		else if (lines[i].substr(0,6) == ":name:"){
			info.name = lines[i].substr(6).trim();
			currentType = ""; currentToken = "";
		}
		else {
			currentToken += lines[i]+'\n';
		}
	}
	return {question:question,answer:answer,layout:layout,tags:tags,info:info};
}
