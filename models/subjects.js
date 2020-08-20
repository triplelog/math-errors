const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const SubjectData = new Schema({subject:String});
module.exports = mongoose.model('SubjectData', SubjectData, 'subjectdatass');