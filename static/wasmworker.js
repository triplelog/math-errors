importScripts('wasmhello.js');

var l = Module.cwrap("LatexIt","string",["string"]);
var p = Module.cwrap("PlotIt","string",["string","number","number","number"]);

var latex = "";
function addLatex(x) {
	latex += x;
}
	
var svg = "";
function addSVG(x) {
	svg += x;
}


onmessage = function(e) {
	var message = e.data;
	var result = [];
	if (message[0] == "latex"){
		latex = "";
		l(message[1]);
		result = ["latex",message[1],latex];
	}
	else {
		svg = "";
		p(message[1]);
		result = ["svg",message[1],svg];
	}
	postMessage(result);
}