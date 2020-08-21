'use strict';
const markdown = require('markdown-it');
var md = new markdown();
const katex = require('katex');
const assert = require('assert');
const bindingP = require.resolve(`../build/Release/bindingP`);
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
var nunjucks = require('nunjucks');

var mdoptions = {
  validate: function(params) {
    return params.trim().match(/^rule/) || params.trim().match(/^error/) || params.trim().match(/^example/);
  },
 
  render: function (tokens, idx) {
    var m = tokens[idx].info.trim().match(/^example/);
 	if (m){
 		console.log(tokens[idx].info.trim().replace('example','').replace(':::','').trim());
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
  	  console.log("content: ",tokens[idx]);
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






module.exports = mdoptions;
