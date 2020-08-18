module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('tree')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = [];
      var lines = reader.lines
      for (var i = 0; i < lines.length; i++) {
      	cards.push(lines[i]);
      }
      var blk = self.createBlock(parent, 'tree', cards);
      return blk;
    })
  })
}