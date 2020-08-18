module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('tree')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var lines = reader.getLines().map(function (l) { return l.toUpperCase() })
      return self.createBlock(parent, 'cards', lines)
    })
  })
}