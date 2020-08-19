const katex = require('katex');
module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('instruction')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = {};
      var lines = reader.lines;
      for (var i = 0; i < lines.length; i++) {
      	console.log(lines[i].substr(0,5).toLowerCase());
      	if (lines[i].substr(0,4).toLowerCase() == "in: "){
      		cards['in']=lines[i].substr(4);
      	}
      	else if (lines[i].substr(0,5).toLowerCase() == "out: "){
      		cards['out']=lines[i].substr(5);
      	}
      }
      console.log(JSON.stringify(cards));
      var blk = self.createBlock(parent, 'instruction', "",{cards:cards});
      return blk;
    })
  })
}