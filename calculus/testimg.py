<!DOCTYPE html>
<html>
<body>

<canvas id="myCanvas" width="640" height="480" style="background:red" tabindex="1" autofocus></canvas>
<script type="text/javascript">

var canvas = document.getElementById('myCanvas');
      var context = canvas.getContext('2d');
      var imageObj = new Image();

      imageObj.onload = function() {
        context.drawImage(imageObj, 0, 0);
      };
      imageObj.src = 'result0.png';

document.getElementById("myCanvas").focus();
window.addEventListener('keydown',this.check,false);

function check(e) {
var src_str = [];
src_str.push('junex0.png');
src_str.push('junex1.png');
    if(e.keyCode==39){
imageObj.onload = function() {
        context.drawImage(imageObj, 0, 0);
      };
      imageObj.src = src_str[1];
}
	if(e.keyCode==37){
imageObj.onload = function() {
        context.drawImage(imageObj, 0, 0);
      };
      imageObj.src = src_str[0];
}
}

</script>

</body>
</html>