'use strict';
const markdown = require('markdown-it');
var iterator = require('markdown-it-for-inline');
var repmath = require('./markdown-it-math.js');
var md = new markdown();
md.use(require('../mathdocs/markdown-it-input.js'));
md.use(iterator, 'math_replace', 'text', function (tokens, idx) {
              tokens[idx].content = repmath(tokens,idx);
            });
const katex = require('katex');
const assert = require('assert');
const bindingP = require.resolve(`../build/Release/bindingP`);
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
var nunjucks = require('nunjucks');

function mdoptionsfn(filen){
	console.log("filen: ",filen);
	if (filen != ""){
		maincppp.makelesson(filen);
	}
	var mdoptions = {
	  validate: function(params) {
		return params.trim().match(/^rule/) || params.trim().match(/^error/) || params.trim().match(/^example/) || params.trim().match(/^graph/);
	  },
 
	  render: function (tokens, idx) {
		

		if (tokens[idx].nesting === 1) {
		  // opening tag
		  return '\n';
 
		} else {
		  // closing tag
		  return '\n';
		}
	  },
  
	  content: function (tokens, idx) {
		  if (tokens[idx].markup.length < 1){
			return "";
		  }
		  if (tokens[idx-1].info.trim().match(/^graph/)) {
		  	var newStr = makeGraph(tokens[idx].markup);
		  	console.log(newStr);
		  	return newStr;
		  }
		  else if (tokens[idx-1].info.trim().match(/^example/)) {

		  	  var lines = tokens[idx].markup.split('\n');
		  	  var newStr = "";
		  	  for (var iii = 0; iii < lines.length; iii++) {
		  	  	  if (lines[iii].trim().length < 1){continue;}
				  var ex = lines[iii].trim();
				  console.log("ex: ",ex);
				  var jsonmessage = maincppp.onerule(ex);
				  console.log(jsonmessage);
				  jsonmessage = jsonmessage.replace(/\\/g,"\\\\");
				  console.log(jsonmessage);
				  var parsed = JSON.parse(jsonmessage);
				  for (var i=0;i<parsed.length;i++){
					parsed[i].start = katex.renderToString(parsed[i].start, {throwOnError: false});
					parsed[i].input = katex.renderToString(parsed[i].input, {throwOnError: false});
					parsed[i].output = katex.renderToString(parsed[i].output, {throwOnError: false});
					parsed[i].final = katex.renderToString(parsed[i].final, {throwOnError: false});
					for (var ii=0;ii<parsed[i].map.length;ii++){
						parsed[i].map[ii] = katex.renderToString(parsed[i].map[ii], {throwOnError: false});
					}
				  }
				  newStr += nunjucks.render('templates/example.njk',{parsed:parsed}) + "\n";
			  }
			  return newStr;
		  }
		  else {
			  var cards = {constraints:[],explanation:""};
			  var lines = tokens[idx].markup.split('\n');
			  var isText = false;
			  for (var i = 0; i < lines.length; i++) {
				if (lines[i].length < 2){continue;}
				if (!isText){
					if (lines[i].substr(0,4).toLowerCase() == "in: "){
						var input = maincppp.latexify(lines[i].substr(4));
						var html = katex.renderToString(input, {
							throwOnError: false
						});
						cards['in']=html;
					}
					else if (lines[i].substr(0,5).toLowerCase() == "out: "){
						var html = katex.renderToString(maincppp.latexify(lines[i].substr(5)), {
							throwOnError: false
						});
						cards['out']=html;
					}
					else if (lines[i].substr(0,2) == "ee"){
						isText = true;
					}
					else{
						var html = katex.renderToString(maincppp.latexify(lines[i]), {
							throwOnError: false
						});
						cards['constraints'].push(html);
					}
				}
				else {
					//render the asciidoc
					cards['explanation']+= lines[i]+"\n";
				}
			  }
			  if (cards['explanation'].length > 0){
				cards['explanation']= md.utils.unescapeAll(md.render(cards['explanation']));
			  }
			  //console.log(cards);
			  var newStr = "";
			  if (tokens[idx-1].info.trim().match(/^rule/)){
				newStr = nunjucks.render('templates/instruction.njk',{cards: cards,type: "rule"});
			  }
			  else {
				newStr = nunjucks.render('templates/instruction.njk',{cards: cards,type: "error"});
			  }

			  return newStr;
		  }
	  }
	};
	return mdoptions;
}

function makeGraph(input){
	var fn = input.split("\n")[0];
	var domain = [-10,10];
	var range = "auto";
	var svg = '<svg version="1.1" baseProfile="full" width="100" height="100" xmlns="http://www.w3.org/2000/svg">';
	svg += '<path d="M50 0 V100 M0 50 H100"/>';
	svg += '</svg>';
	return svg;
}




module.exports = function(filen) {return mdoptionsfn(filen);};
