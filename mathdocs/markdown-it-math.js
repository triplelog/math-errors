'use strict';
const markdown = require('markdown-it');
var md = new markdown();
const katex = require('katex');
const assert = require('assert');
const bindingP = require.resolve(`../build/Release/bindingP`);
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();
var nunjucks = require('nunjucks');

module.exports = function(tokens,idx) {
	console.log("math?? ", tokens[idx].content);
  return tokens[idx].content;
};