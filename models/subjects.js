const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const SubjectData = new Schema({subject:String,topics:{}});
module.exports = mongoose.model('SubjectData', SubjectData);