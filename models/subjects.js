const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const SubjectData = new Schema({subject:String,topics:{type: Schema.Types.Mixed, required: true}});
module.exports = mongoose.model('SubjectData', SubjectData);