
const https = require('https');
//const http = require('http');
var fs = require("fs");
//var myParser = require("body-parser");
var qs = require('querystring');
const { exec } = require('child_process');
const bodyParser = require('body-parser');
var parse = require('csv-parse');
var nunjucks = require('nunjucks');
var crypto = require("crypto");
//const flate = require('wasm-flate');
const options = {
  key: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/matherrors.com/fullchain.pem')
};
const { PerformanceObserver, performance } = require('perf_hooks');

var tempKeys = {};
const User = require('./models/user');
const mongoose = require('mongoose');
mongoose.connect('mongodb://matherrors:kZGWGda3A@localhost:27017/matherrors?authSource=matherrors', {useNewUrlParser: true, useFindAndModify: false, useCreateIndex: true, useUnifiedTopology: true });

var schema = new mongoose.Schema({"subj": String, "nam": String});
var Tankk = mongoose.model('Tankk', schema);
var dog = new Tankk({"subj":"a","nam":"b"});
dog.save(function(err,result){
	console.log("err1: ",err);
	console.log("res2: ",result);
	Tankk.countDocuments({}, function(err,result){
		console.log("res3: ",result);
	});
});

var passport = require('passport')
var LocalStrategy = require('passport-local').Strategy;
// use static authenticate method of model in LocalStrategy
//passport.use(User.createStrategy());
 
// use static serialize and deserialize of model for passport session support
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

var express = require('express');



var app2 = express();
const session = require("express-session");
app2.use(session({ secret: "cats", resave: true, saveUninitialized: true }));
app2.use(express.urlencoded({ extended: true }));
app2.use(bodyParser.json());
app2.use(bodyParser.urlencoded({extended: false}));
app2.use(passport.initialize());
app2.use(passport.session());

app2.get('/account',
  function(req, res){
  	if (!req.isAuthenticated()){
  		if (req.query.e && req.query.e=='duplicate'){
  			res.write(nunjucks.render('./templates/loginregister.html',{
				duplicate: true,
			}));
			res.end();
  		}
  		else if (req.query.e && req.query.e=='badlogin'){
  			res.write(nunjucks.render('./templates/loginregister.html',{
				badlogin: true,
			}));
			res.end();
  		}
  		else {
  			res.write(nunjucks.render('./templates/loginregister.html',{}));
			res.end();
  		}
		
  	}
  	else {
  		var tkey = crypto.randomBytes(100).toString('hex').substr(2, 18);
		tempKeys[tkey] = {username:req.user.username};

  		res.write(nunjucks.render('./templates/account.html',{
  			username: req.user.options.displayName || req.user.username,
  			name: req.user.name || '',
  		}));
		res.end();
  	}
  	
  }
);


app2.post('/register',
  function(req, res){
  	console.log('registering: ',performance.now());
  	var progress = {};
  	progress.arithmetic = [{name:'Addition',goals:[{name:'Error Free',progress:0},{name:'Carry Error',progress:0},{name:'Carry 0 of 2',progress:0},{name:'Carry 1 of 2',progress:0},{name:'Match Error',progress:0}]}];
	progress.arithmetic.push({name:'Subtraction',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
	progress.arithmetic.push({name:'Multiplication',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
	progress.arithmetic.push({name:'Division',goals:[{name:'Error Free',progress:0},{name:'Match Error',progress:0}]});
  	var user = new User({username: req.body.username.toLowerCase(), progress: progress, options: {displayName: req.body.username}});
	User.register(user,req.body.password, function(err) {
		if (err) {
		  if (err.name == 'UserExistsError'){
		  	res.redirect('../account?e=duplicate');
		  }
		  else {
		  	console.log(err);
		  }
		  
		}
		else {
		
			console.log('user registered!',performance.now());
			var robot = 'python3 python/robohash/createrobo.py '+req.body.username.toLowerCase()+' 1';
			var child = exec(robot, function(err, stdout, stderr) {
				console.log('robot created: ',performance.now());
				req.login(user, function(err) {
				  if (err) { res.redirect('/'); }
				  else {
				  	console.log('logged in: ',performance.now());
				  	res.redirect('../account');
				  }
				});
			});
			
			
			
		}
		

	});
  }
);

function usernameToLowerCase(req, res, next){
	req.body.username = req.body.username.toLowerCase();
	next();
} 
app2.post('/login',  usernameToLowerCase,
	passport.authenticate('local', { successRedirect: '/account', failureRedirect: '/account?e=badlogin' })
);

app2.get('/logout', 
	function(req, res) {
	  req.logout();
	  res.redirect('../');
	}
);




module.exports = {loginApp: app2, tempKeys: tempKeys, mongoose: mongoose}