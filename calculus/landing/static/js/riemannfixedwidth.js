var canvas;
var ctx;

var canvasOffset;
var offsetX;
var offsetY;

var isDrawing = false;
var actArea = 1.;
canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");


function myf(x){
	return x*x-3*x+8;
}

function drawCurve(ctx){
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.beginPath();
	ctx.moveTo(0,0);
	actArea = 0;
	for (var i=0;i<canvas.width+1;i++){
		ctx.lineTo(i,canvas.height-25*myf(i/100));
		actArea+=25*myf(i/100);
	}
	ctx.stroke();
	ctx.fillStyle='rgba(135,206,250, .25)';
	ctx.lineTo(canvas.width,canvas.height);
	ctx.lineTo(0,canvas.height);
	ctx.fill();
	ctx.fillStyle='black';
}

function guessArea(){
	predArea = parseFloat(document.getElementById('predArea').value);
	document.getElementById('actArea').innerHTML = '<br />Predicted Area: '+predArea.toFixed(2)+'<br />Actual Area: '+actArea.toFixed(2)+'<br />Error: '+(Math.abs(predArea-actArea)*100.0/(actArea)).toFixed(2)+'%';
}

function calcArea(){
	totalArea = eval(document.getElementById('rectArea').value);
	document.getElementById('totalArea').innerHTML = totalArea;
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
for (var i=0;i<nrect;i++){
	rectangles.push([canvas.width/nrect*i,canvas.height,canvas.width/nrect,0]);
}
var lastRec = [0,0,0,0];
var lastRecID = 0;
var totalArea = 0;
drawCurve(ctx);

function handleMouseUp() {
	isDrawing = false;
	canvas.style.cursor = "default";
	rectangles[lastRecID]=lastRec;
	if (nrect==3){
		document.getElementById('allAreas').innerHTML = rectangles[0][3]+', '+rectangles[1][3]+', '+rectangles[2][3];
	}
	else if (nrect==6){
		document.getElementById('allAreas').innerHTML = rectangles[0][3]+', '+rectangles[1][3]+', '+rectangles[2][3]+', '+rectangles[3][3]+', '+rectangles[4][3]+', '+rectangles[5][3];
	}
	
}


function handleMouseMove(e) {
	if (isDrawing) {
		var mouseX = parseInt(e.clientX - offsetX);
		var mouseY = parseInt(e.clientY - offsetY);				
		var rectid = 0;
		for (var i=0;i<nrect;i++){
			if (startX<canvas.width/nrect*(i+1)){
				rectid = i;
				break;
			}
		}
		drawCurve(ctx);
		for (var i=0;i<rectangles.length;i++){
			if (i!=rectid){
				ctx.beginPath();
				ctx.rect(rectangles[i][0],rectangles[i][1],rectangles[i][2],rectangles[i][3]);
				ctx.stroke();
			}
		}
		ctx.beginPath();
		ctx.rect(canvas.width/nrect*rectid, mouseY, canvas.width/nrect, canvas.height-mouseY);
		ctx.stroke();
		lastRec = [canvas.width/nrect*rectid, mouseY, canvas.width/nrect, canvas.height-mouseY];
		lastRecID = rectid;
		
	}
}

function handleMouseDown(e) {
	canvas.style.cursor = "crosshair";		
	isDrawing = true
	startX = parseInt(e.clientX - offsetX);
	startY = parseInt(e.clientY - offsetY);
}
