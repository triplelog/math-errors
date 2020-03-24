'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`./build/Release/binding`);
const maincpp = require(binding);
//const postfix = require('./postfix.js');

//const mongoose = require('mongoose');
//mongoose.connect('mongodb://localhost:27017/chartdn', {useNewUrlParser: true});



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
  key: fs.readFileSync('/etc/letsencrypt/live/chartdn.com/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/chartdn.com/fullchain.pem')
};
const { PerformanceObserver, performance } = require('perf_hooks');




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


console.log(maincpp.addwrong("3123","691","3714"));
console.log(maincpp.subtractwrong("612","498","224") );