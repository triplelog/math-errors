importScripts('wasmhello.js');

var l = Module.cwrap("LatexIt","string",["string"]);
var p = Module.cwrap("PlotIt","string",["string","number","number","number"]);
var a = Module.cwrap("AddRules","string",["string","string"]);

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
	else if (message[0] == "plot"){
		svg = "";
		p(message[1],message[2],message[3],message[4],message[5]);
		svg += '<input type="range" id="domainSlider" min="0" max="'+(message[6]*2)+'" value="'+message[6]+'"></input>';
		result = ["svg",message[1],svg];
	}
	else if (message[0] == "rules"){
		a(message[1],message[2]);
		result = ["rules",message[1],"done"];
	}
	postMessage(result);
}