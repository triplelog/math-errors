module.exports = function (registry) {
  registry.inlineMacro('$', function () {
    var self = this
    self.process(function (parent, target, attrs) {
      var text;
      console.log(JSON.stringify(attrs));
      console.log(target);
      text = target;
      return self.createInline(parent, 'quoted', text, { 'type': 'strong' }).convert()
    })
  })
}