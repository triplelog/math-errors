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

function convertCoordinates(x,y,domain,range){
	if (x>=domain[0] && x<=domain[1]){
		var xstr = "" + (100*(x-domain[0])/(domain[1]-domain[0]));
		if (y>=range[0] && y<=range[1]){
			var ystr = "" + (100-100*(y-range[0])/(range[1]-range[0]));
			return xstr + " " + ystr;
		}
		else {
			return "";
		}
	}
	else {
		return "";
	}
}
function convertX(x,domain){
	if (x>=domain[0] && x<=domain[1]){
		var xstr = "" + (100*(x-domain[0])/(domain[1]-domain[0]));
		return xstr;
	}
	else {
		return "";
	}
}
function convertY(y,range){
	if (y>=range[0] && y<=range[1]){
		var ystr = "" + (100-100*(y-range[0])/(range[1]-range[0]));
		return ystr;
	}
	else {
		return "";
	}
}
function makeGraph(input){
	var fn = input.split("\n")[0];
	var domain = [-20,20];
	var range = [-20,20];
	var svg = '<svg version="1.1" baseProfile="full" viewBox="0 0 100 100" width="200" height="200" xmlns="http://www.w3.org/2000/svg">';
	svg += '<path d="M'+convertCoordinates(0,range[1],domain,range)+' V100 M'+convertCoordinates(domain[0],0,domain,range)+' H100" stroke="rgb(160,160,160)"/>';
	if (domain[1]-domain[0]>5){
		for (var i=Math.floor(domain[0])+1;i<Math.floor(domain[1])+1;i++){
			if (range[1]-range[0]>5){
				for (var ii=Math.floor(range[0])+1;ii<Math.floor(range[1])+1;ii++){
					if (i%5==0 && ii%5 == 0){
						svg += '<circle cx="'+convertX(i,domain)+'" cy="'+convertY(ii,range)+'" r=".6" fill="red"/>';
					}
					else if (i%5==0 || ii%5 == 0){
						svg += '<circle cx="'+convertX(i,domain)+'" cy="'+convertY(ii,range)+'" r=".4" fill="red"/>';
					}
					else {
						svg += '<circle cx="'+convertX(i,domain)+'" cy="'+convertY(ii,range)+'" r=".2" fill="red"/>';
					}
					
				}
			}
		}
	}
	var path = "M";
	for (var i=domain[0];i<=domain[1];i+= .01){
		path += convertCoordinates(i,2*i+1,domain,range)+ " ";
	}
	svg += '<path d="'+path+'" stroke="rgb(60,60,60)"/>';
	
	svg += '</svg>';
	return svg;
}




module.exports = function(filen) {return mdoptionsfn(filen);};
