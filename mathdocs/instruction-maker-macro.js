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
      var blk = self.createBlock(parent, 'example', "", {parsed:parsed});
      return blk;
    })
  })
}