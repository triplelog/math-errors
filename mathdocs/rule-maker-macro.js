module.exports = function (registry) {
  registry.preprocessor(function () {
    var self = this
    self.process(function (doc, reader) {
      var lines = reader.lines
      for (var i = 0; i < lines.length; i++) {
      	var currentMath = "";
      	var insideDollar = false;
        for (var ii = 0;ii < lines[i].length; ii++) {
        	if (lines[i][ii] == "$" && !insideDollar){
        		insideDollar = true;
        	}
        	else if (lines[i][ii] == "$" && insideDollar){
        		if (ii < lines[i].length-1 && lines[i][ii+1] != " "){
        			currentMath += lines[i][ii];
        		}
        		else if (currentMath == ""){
        			//is $$ math
        		}
        		else {
        			//TODO: replace [ and ] from currentMath
        			var newString = "math:infix[math=\""+currentMath+"\"]";
        			lines[i] = lines[i].replace("$"+currentMath+"$",newString);
        			ii += newString.length - (currentMath.length+2);
        			insideDollar = false;
        			currentMath = "";
        		}
        	}
        	else if (insideDollar){
        		currentMath += lines[i][ii];
        	}
        }
        console.log(lines[i]);
      }
      return reader
    })
  })
  registry.inlineMacro('math', function () {
    var self = this
    self.process(function (parent, target, attrs) {
      var text;
      console.log(target);
      text = '<span class="katex">'+attrs.math+'</span>';
      return self.createInline(parent, 'quoted', text, { }).convert()
    })
  })
}