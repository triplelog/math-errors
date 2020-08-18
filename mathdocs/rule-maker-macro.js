module.exports = function (registry) {
  registry.preprocessor(function () {
    var self = this
    self.process(function (doc, reader) {
      var lines = reader.lines
      for (var i = 0; i < lines.length; i++) {
        lines[i].replace('[','|');
        console.log(lines[i]);
      }
      return reader
    })
  })
  registry.inlineMacro('math', function () {
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