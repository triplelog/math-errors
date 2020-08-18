const katex = require('katex');
module.exports = function (registry) {
  registry.block(function () {
    var self = this
    self.named('tree')
    self.onContext('paragraph')
    self.process(function (parent, reader) {
      var cards = [];
      var lines = reader.lines;
      for (var i = 0; i < lines.length; i++) {
      	
      	var currentMath = "";
      	var insideDollar = false;
        for (var ii = 0;ii < lines[i].length; ii++) {
        	if (ii < lines[i].length - 17 && lines[i].substr(ii,17) == "math:infix[math=\"" && !insideDollar){
        		insideDollar = true;
        		ii += 17;
        		console.log("found");
        	}
        	else if (lines[i][ii] == "\"" && insideDollar){
				//TODO: replace [ and ] from currentMath
				console.log(currentMath);
				var newString = katex.renderToString(currentMath, {
						throwOnError: false
				  });
				console.log(newString);
				lines[i] = lines[i].replace("math:infix[math=\""+currentMath+"\"]",newString);
				ii += newString.length - (currentMath.length+19);
				insideDollar = false;
				currentMath = "";
				
        	}
        	else if (insideDollar){
        		currentMath += lines[i][ii];
        	}
        }
        cards.push(lines[i]);
      }
      console.log(JSON.stringify(cards));
      var blk = self.createBlock(parent, 'tree', "",{cards:cards});
      return blk;
    })
  })
}