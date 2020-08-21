'use strict';
const markdown = require('markdown-it');
var iterator = require('markdown-it-for-inline');
var repmath = require('./markdown-it-math.js');
var md = new markdown();
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
	
	var mdoptions = {
	  validate: function(params) {
		return params.trim().match(/^rule/) || params.trim().match(/^error/) || params.trim().match(/^example/);
	  },
 
	  render: function (tokens, idx) {
		var m = tokens[idx].info.trim().match(/^example/);
		var ex;
		if (m){
			  console.log("filen: ",filen);
			  if (filen != ""){
			  	maincppp.makelesson(filen);
			  }
			  ex = tokens[idx].info.trim().replace('example','').replace(':::','').trim();
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
			  var newStr = nunjucks.render('templates/example.njk',{parsed:parsed});
			  return newStr;
		}
		else {
			return '\n';
		}
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
		  var cards = {constraints:[],explanation:""};
		  var lines = tokens[idx].markup.split('\n').slice(1,);
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
			cards['explanation']= md.render(cards['explanation']);
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
	};
	return mdoptions;
}






module.exports = function(filen) {return mdoptionsfn(filen);};
