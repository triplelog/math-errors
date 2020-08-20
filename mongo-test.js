
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