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

server1.listen(12312);

const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('\n');
}).listen(8080);

const WebSocket = require('ws');
//const wss = new WebSocket.Server({ port: 8080 , origin: 'http://tabdn.com'});
const wss = new WebSocket.Server({ server });
wss.on('connection', function connection(ws) {
  	var x = ""+Math.floor(Math.random() * 1000);
	var y = ""+Math.floor(Math.random() * 1000);
	var jsonmessage = {'question':[[x,y],['','','',''],['','','','']],'id':0};
	var username = '';
	ws.send(JSON.stringify(jsonmessage));
  	ws.on('message', function incoming(message) {
		var dm = JSON.parse(message);
		if (dm.operation == 'key'){
			if (tempKeys[dm.message]){
				username = tempKeys[dm.message].username;
			}
		}
		else if (dm.type == 'arithmetic'){
			if (dm.subtype == 'addition'){
				console.log('a',performance.now());
				var errorInfo = maincpp.addwrong(dm.message[0][0],dm.message[0][1],dm.message[1]);
				console.log(errorInfo, 'b', performance.now());
				errorInfo = addIntsWrongJS([dm.message[0][0],dm.message[0][1]],dm.message[1])
				console.log(errorInfo, 'c', performance.now());
				if (errorInfo.indexOf('carry')>-1){
					if (username != ''){
						User.updateOne({username: username}, {$inc:{"progress.arithmetic.0.goals.1.progress":10}}, function (err2, result2) {
							if (err2 || !result2 || result2.n == 0){
								console.log("Did not update");
							}
						});
						console.log(username);
					}
					console.log('Carry Error');
				}
				var x = ""+Math.floor(Math.random() * 1000);
				var y = ""+Math.floor(Math.random() * 1000);
				var jsonmessage = {'question':[[x,y],['','','',''],['','','','']],'update':'yes','id':0};
				ws.send(JSON.stringify(jsonmessage));
			}
		}
		
  	});
});


app.get('/arithmetic',
	function(req, res){
		
		var types = [{name:'Addition',goals:[{name:'Error Free',progress:0},{name:'Carry Error',progress:10},{name:'Carry 0 of 2',progress:60},{name:'Carry 1 of 2',progress:0},{name:'Match Error',progress:0}]}];
		types.push({name:'Subtraction',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
		types.push({name:'Multiplication',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
		types.push({name:'Division',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
		if (req.isAuthenticated()){
			console.log(req.user.progress.arithmetic[0].goals);
			console.log(req.user.progress.arithmetic[0].goals[1]);
			types = req.user.progress.arithmetic;
		}
		//nocarry is miss 1 of 1
		//onecarry is miss exactly 1 of 2
		//twocarries is miss 2 of 2
		var tkey = crypto.randomBytes(100).toString('hex').substr(2, 18);
		if (req.isAuthenticated()){
			tempKeys[tkey] = {username:req.user.username};
		}
		
		res.write(nunjucks.render('topics/arithmetic.html',{
			type: 'Arithmetic',
			types: types,
			key: tkey,
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

function addIntsWrongJS(strs, answer){
	if (strs.length == 1){
		return "size is 1";
	}
	else if (strs.length == 0){
		return "size is 0";
	}

    
    
    
	var answerDigits = [];
	for (var it = answer.length-1;it>= 0;it--){
		answerDigits.push(parseInt(answer[it]));
	}
	var ii;
	var sz = 0;
	
	var digits = [];
	for (ii=0;ii<strs.length;ii++){
		onestr = [];
		for (var it = strs[ii].length-1;it>= 0;it--){
			onestr.push(parseInt(strs[ii][it]));
		}
		if (onestr.length>sz){
			sz = onestr.length;
		}
		digits.push(onestr);
	}
	var dsz = digits.length;
	var adsz = answerDigits.length;
	for (ii=0;ii<dsz;ii++){
		int i;
		for (i = digits[ii].length;i<sz;i++){
			digits[ii].push(0);
		}
	}
	
	
	var digits0 = [0,0,0,0,0];
	var errors = "";
	var returnString = "";
	var iii;
	var isPossible = true;
		
	var i; var di;
	var carry = 0;
	var digit = 0;
	var newdigit = 0;
	for (iii=0;iii<100000;iii++){
		errors = "";
		di = 0;
		isPossible = true;
		carry = 0;
		digit = 0;
		newdigit = 0;
		
		for (i=0;i<sz;i++){
			digit = carry;
			for (ii=0;ii<dsz;ii++){
				newdigit = digit + digits[ii][i];
				if (newdigit/10 > digit/10 && iii % 1000 > 970){
					digit = newdigit - 10;
					//std::string d(1,i+'2'); //next digit will be wrong, and start at 1 not 0 -- only up to 9th digit
					//errors += "You missed a carry on "+d+"rd digit from right.\n";
					errors += "You missed a carry.\n";
				}
				else {
					digit = newdigit;
				}
			}
			if (digit>9){
				digits0[di] = digit%10;
				di++;
				carry = digit/10;
			}
			else {
				digits0[di] = digit;
				di++;
				carry = 0;
			}
			
			if (adsz <= i || digits0[i] !=answerDigits[i]){
				isPossible = false;
				break;
			}
		}
		if (!isPossible){continue;}
		while (carry > 0){
			if (carry>9){
				digits0[di] = carry%10;
				di++;
				carry = carry/10;
			}
			else {
				digits0[di] = carry;
				di++;
				carry = 0;
			}
			if (adsz <= i || digits0[i] !=answerDigits[i]){
				isPossible = false;
				break;
			}
			i++;
		}
		if (isPossible && adsz == di){
			returnString = errors;
			//returnString += "The correct answer is " + addInts(strs);
		}
		
	}
	return returnString;
	//return "done";
}



