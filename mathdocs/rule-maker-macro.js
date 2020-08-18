module.exports = function (registry) {
  registry.inlineMacro('math', function () {
    var self = this
    self.process(function (parent, target, attrs) {
      var text
      text = attrs[0];
      return self.createInline(parent, 'quoted', text, { 'type': 'strong' }).convert()
    })
  })
}