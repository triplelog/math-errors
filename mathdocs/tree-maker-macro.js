module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('tree')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = [];
      var lines = reader.lines;
      console.log(JSON.stringify(lines));
      for (var i = 0; i < lines.length; i++) {
      	cards.push(lines[i]);
      }
      console.log(JSON.stringify(cards));
      var blk = self.createBlock(parent, 'tree', cards);
      return blk;
    })
  })
}