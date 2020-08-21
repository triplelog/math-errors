const markdown = require('markdown-it');
var md = new markdown();

var mdoptions = {
  validate: function(params) {
    return params.trim().match(/^rule\s+(.*)$/);
  },
 
  render: function (tokens, idx) {
    var m = tokens[idx].info.trim().match(/^rule\s+(.*)$/);
 
    if (tokens[idx].nesting === 1) {
      // opening tag
      return '<details><summary>' + md.utils.escapeHtml(m[1]) + '</summary>\n';
 
    } else {
      // closing tag
      return '</details>\n';
    }
  },
  
  content: function (tokens, idx) {
  	  console.log("CCC:",tokens[idx].markup);
  	  var cards = {constraints:[],explanation:""};
      var lines = tokens[idx].markup.split('\n').slice(1,);
      var isText = false;
      for (var i = 0; i < lines.length; i++) {
      	console.log(lines[i]);
      	if (!isText){
			if (lines[i].substr(0,4).toLowerCase() == "in: "){
				var input = maincppp.latexify(lines[i].substr(4));
				var html = katex.renderToString(input, {
					throwOnError: false
				});
				cards['in']=html;
			}
			else if (lines[i].substr(0,5).toLowerCase() == "out: "){
				var html = katex.renderToString(maincppp.latexify(lines[i].substr(5)), {
					throwOnError: false
				});
				cards['out']=html;
			}
			else if (lines[i].substr(0,3) == "eee"){
				isText = true;
			}
			else{
				var html = katex.renderToString(maincppp.latexify(lines[i]), {
					throwOnError: false
				});
				cards['constraints'].push(html);
			}
      	}
      	else {
      		//render the asciidoc
      		cards['explanation']+= lines[i]+"\n";
      	}
      }
      if (cards['explanation'].length > 0){
      	cards['explanation']= asciidoctor2.convert(cards['explanation'],{ 'extension_registry': registry2, safe: 'safe', backend: 'html5', template_dir: '../templates' });
      }
  }
};
module.exports = mdoptions;

