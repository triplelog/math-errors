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
      	if (lines.substr(0,4).toLowerCase() == "in: "){
      		cards['in']=lines.substr(4);
      	}
      	else if (lines.substr(0,5).toLowerCase() == "out: "){
      		cards['out']=lines.substr(5);
      	}
      }
      var blk = self.createBlock(parent, 'tree', "",{cards:cards});
      return blk;
    })
  })
}