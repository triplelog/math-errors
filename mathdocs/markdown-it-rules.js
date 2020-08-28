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
		if (xstr[0] == "-"){xstr = xstr.substr(0,6);}
		else{xstr = xstr.substr(0,5);}
		if (y>=range[0] && y<=range[1]){
			var ystr = "" + (100-100*(y-range[0])/(range[1]-range[0]));
			if (ystr[0] == "-"){ystr = ystr.substr(0,6);}
			else{ystr = ystr.substr(0,5);}
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
function convertX(x,domain,shift=0){
	if (x>=domain[0] && x<=domain[1]){
		var xstr = "" + (shift+100*(x-domain[0])/(domain[1]-domain[0]));
		if (xstr[0] == "-"){xstr = xstr.substr(0,6);}
		else{xstr = xstr.substr(0,5);}
		return xstr;
	}
	else {
		return "";
	}
}
function convertY(y,range,shift=0){
	if (y>=range[0] && y<=range[1]){
		var ystr = "" + (shift+100-100*(y-range[0])/(range[1]-range[0]));
		if (ystr[0] == "-"){ystr = ystr.substr(0,6);}
		else{ystr = ystr.substr(0,5);}
		return ystr;
	}
	else {
		return "";
	}
}
function makeGraph(input){
	var fn = input.trim().split("\n")[0];
	var domain = [-20,20];
	var range = [-20,20];
	var svg = '<svg version="1.1" baseProfile="full" viewBox="0 0 100 100" width="200" height="200" xmlns="http://www.w3.org/2000/svg">';
	
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
			
			if (i%5 == 0 && i != 0){
				svg += '<circle cx="'+convertX(i,domain)+'" cy="'+convertY(0,range,3)+'" r="4px" fill="white"/>';
				svg += '<text fill="black" font-size="6px" text-anchor="middle" dominant-baseline="hanging" x="'+convertX(i,domain)+'" y="'+convertY(0,range,1)+'">&nbsp;'+i+'&nbsp;</text>';
			}
		}
		for (var ii=Math.floor(range[0])+1;ii<Math.floor(range[1])+1;ii++){
			if (ii%5 == 0 && ii != 0){
				svg += '<circle cx="'+convertX(0,domain,-3)+'" cy="'+convertY(ii,range)+'" r="4px" fill="white"/>';
				svg += '<text font-size="6px" text-anchor="end" dominant-baseline="middle" x="'+convertX(0,domain,-1)+'" y="'+convertY(ii,range,1)+'">'+ii+'</text>';
			}	
		}
	}
	svg += '<path d="M'+convertCoordinates(0,range[1],domain,range)+' V100 M'+convertCoordinates(domain[0],0,domain,range)+' H100" stroke="rgb(160,160,160)"/>';
	
	
	var path = "M";
	console.log(fn);
	var outStr = maincppp.graphpoints(fn,""+domain[0],""+domain[1]);
	var points = outStr.split(";").slice(0,1001);
	//console.log(outStr);
	for (var i=0;i<1001;i++){
		path += convertCoordinates(points[i].split(",")[0],points[i].split(",")[1],domain,range)+ " ";
	}
	svg += '<path d="'+path+'" stroke="rgb(60,60,60)" fill="none"/>';
	
	svg += '</svg>';
	return svg;
}




module.exports = function(filen) {return mdoptionsfn(filen);};
