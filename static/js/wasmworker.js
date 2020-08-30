importScripts('../wasmhello.js');

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
  console.log('Message received from main script');
  var workerResult = 'Result: ' + (e.data);
  console.log('Posting message back to main script');
  postMessage(workerResult);
}