var canvas;
var ctx;

var canvasOffset;
var offsetX;
var offsetY;

var isDrawing = false;
var actArea = 1.;
canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");


function myf(x,xfn){
	if (xfn=='pic'){
		return 1;
	}

	return eval(xfn);
}

function drawCurve(ctx){
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.beginPath();
	ctx.moveTo(0,0);
	actArea = 0;

	for (var i=0;i<canvas.width+1;i++){
		ctx.lineTo(i,canvas.height-25*myf(i/100,xfn));
		actArea+=25*myf(i/100,xfn);
	}
	ctx.stroke();
	ctx.fillStyle='rgba(135,206,250, .25)';
	ctx.lineTo(canvas.width,canvas.height);
	ctx.lineTo(0,canvas.height);
	ctx.fill();
	ctx.fillStyle='black';
}

function guessArea(maxError){
	predArea = parseFloat(document.getElementById('predArea').value);
	document.getElementById('actArea').innerHTML = '<br />Predicted Area: '+predArea.toFixed(2)+'<br />Actual Area: '+actArea.toFixed(2)+'<br />Error: '+(Math.abs(predArea-actArea)*100.0/(actArea)).toFixed(2)+'%';
	if ((Math.abs(predArea-actArea)*100.0/(actArea))<maxError){
		document.getElementById('nextLevel').innerHTML = 'Next Level';
	}
}

offsetX = document.getElementById("canvas").offsetLeft;
offsetY = document.getElementById("canvas").offsetTop;

canvas.onmousedown = function (e) {
    handleMouseDown(e);
}
canvas.onmouseup = function(e) {
    handleMouseUp();
}
canvas.onmousemove = function(e) {
    handleMouseMove(e);
}


var startX;
var startY;
var rectangles = [];
var lastRec = [0,0,0,0];
var totalArea = 0;
if (xfn !='pic'){
	drawCurve(ctx);
}

function handleMouseUp() {
	isDrawing = false;
	canvas.style.cursor = "default";
	rectangles.push(lastRec);
	totalArea += Math.abs(lastRec[2])*Math.abs(lastRec[3]);
	document.getElementById('totalArea').innerHTML = totalArea;
}


function handleMouseMove(e) {
	if (isDrawing) {
		var mouseX = parseInt(e.clientX - offsetX);
		var mouseY = parseInt(e.clientY - offsetY);				
		
		drawCurve(ctx);
		for (var i=0;i<rectangles.length;i++){
			ctx.beginPath();
			ctx.rect(rectangles[i][0],rectangles[i][1],rectangles[i][2],rectangles[i][3]);
			ctx.stroke();
		}
		ctx.beginPath();
		ctx.rect(startX, startY, mouseX - startX, mouseY - startY);
		ctx.stroke();
		lastRec = [startX, startY, mouseX - startX, mouseY - startY];
		
	}
}

function handleMouseDown(e) {
	canvas.style.cursor = "crosshair";		
	isDrawing = true
	startX = parseInt(e.clientX - offsetX);
	startY = parseInt(e.clientY - offsetY);
}
