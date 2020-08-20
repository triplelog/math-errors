
const https = require('https');

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