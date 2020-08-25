'use strict';
const markdown = require('markdown-it');
var md = new markdown();
md.use(require('../mathdocs/markdown-it-input.js'));
const katex = require('katex');
const assert = require('assert');
const bindingP = require.resolve(`../build/Release/bindingP`);
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
var nunjucks = require('nunjucks');

module.exports = function(tokens,idx,latex=false) {
	var input = tokens[idx].content;
	var currentMath = "";
	var insideDollar = false;
	for (var ii = 0;ii < input.length; ii++) {
		if (input[ii] == "$" && !insideDollar){
			insideDollar = true;
		}
		else if (input[ii] == "$" && insideDollar){
			if (ii < input.length-1 && (input[ii+1] == "0" || input[ii+1] == "1" || input[ii+1] == "2" || input[ii+1] == "3" || input[ii+1] == "4" || input[ii+1] == "5" || input[ii+1] == "6" || input[ii+1] == "7" || input[ii+1] == "8" || input[ii+1] == "9") ){
				currentMath += input[ii];
			}
			else if (currentMath == ""){
				//is $$ math
			}
			else {
				var newString;
				if (latex){
					newString = currentMath;
				}
				else{
					newString = maincppp.latexify(currentMath);
				}
				var oldString = "$"+currentMath+"$";
				console.log("ns:",newString);
				newString = katex.renderToString(newString, {
						throwOnError: false
				  });
				input = input.replace(oldString,newString);
				ii += newString.length - (oldString.length);
				insideDollar = false;
				currentMath = "";
			}
		}
		else if (insideDollar){
			currentMath += input[ii];
		}
	}
  return input;
};