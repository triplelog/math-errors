const katex = require('katex');
const assert = require('assert');
const bindingP = require.resolve(`../build/Release/bindingP`);
const maincppp = require(bindingP);
var retHelloP = maincppp.hello();

module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('rule')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = {constraints:[]};
      var lines = reader.lines;
      for (var i = 0; i < lines.length; i++) {
      	if (lines[i].substr(0,4).toLowerCase() == "in: "){
      		var html = katex.renderToString(maincppp.latexify(lines[i].substr(4)), {
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
      	else{
      		var html = katex.renderToString(maincppp.latexify(lines[i]), {
				throwOnError: false
		  	});
      		cards['constraints'].push(html);
      	}
      }
      var blk = self.createBlock(parent, 'instruction', "",{cards:cards,type:"rule"});
      return blk;
    })
  })
  registry.block(function () {
    var self = this
    self.named('error')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = {constraints:[]};
      var lines = reader.lines;
      for (var i = 0; i < lines.length; i++) {
      	if (lines[i].substr(0,4).toLowerCase() == "in: "){
      		var html = katex.renderToString(maincppp.latexify(lines[i].substr(4)), {
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
      	else{
      		var html = katex.renderToString(maincppp.latexify(lines[i]), {
				throwOnError: false
		  	});
      		cards['constraints'].push(html);
      	}
      }
      var blk = self.createBlock(parent, 'instruction', "",{cards:cards,type:"error"});
      return blk;
    })
  })
  registry.blockMacro(function () {
    var self = this
    self.named('example')
    self.process(function (parent, target, attrs) {
    	
      var jsonmessage = maincppp.onerule(target);
      console.log(jsonmessage);
	  var parsed = JSON.parse(jsonmessage);
      var blk = self.createBlock(parent, 'example', "", {block:parsed.input});
      return blk;
    })
  })
}