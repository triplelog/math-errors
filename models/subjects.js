const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const SubjectData = new Schema({subject:'string'});
module.exports = mongoose.model('SubjectData', SubjectData);