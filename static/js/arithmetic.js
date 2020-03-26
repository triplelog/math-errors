class asmElement extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
	var _this = this;
	this.input_numbers = [];
	this.sumButtons = false;
  	this.innerHTML = `<div class="asdBlock">
			
			</div>
			<div>
				<button class="submitButton">Submit</button>
			</div>`;
	this.querySelector('.submitButton').addEventListener('click',this.submitAnswer);
  }
  
  /*
  static get observedAttributes() { return ["src"]; }
  attributeChangedCallback(name, oldValue, newValue) {
	  if (name == 'src' && oldValue && oldValue != '' && ws.readyState == 1){
	  	var jsonmessage = {'operation':'view','id':newValue,'loc':this.getAttribute('data-loc'),'style':this.getAttribute('data-style')}
		ws.send(JSON.stringify(jsonmessage));
	  }
  }*/
  
  newQuestion(numbers,carries,answer){
		this.input_numbers = numbers;
		var el = this.querySelector('.asdBlock');
		el.innerHTML = '';
		var div = document.createElement('div');
	
		if (2==2){
			div.classList.add('carryRow');
			for (var i=0;i<carries.length;i++){
				var span = document.createElement('span');
				span.textContent = carries[i];
				div.appendChild(span);
			}
			el.appendChild(div);
		}
	
	
		for (var i=0;i<numbers.length;i++){
			div = document.createElement('div');
			div.classList.add('addRow');
			for (var ii=numbers[i].length-1;ii>=0;ii--){
				var span = document.createElement('span');
				span.textContent = numbers[i][ii];
				div.appendChild(span);
			}
			if (i == numbers.length-1){
				var span = document.createElement('span');
				span.textContent = '+';
				div.appendChild(span);
			}
			el.appendChild(div);
		}
	
		div = document.createElement('div');
		div.classList.add('lineRow');
		div.appendChild(document.createElement('hr'));
		el.appendChild(div);
	
		if (this.sumButtons){
			div = document.createElement('div');
			div.classList.add('sumRow');
			for (var ii=0;ii<answer.length;ii++){
				var span = document.createElement('span');
				span.id = 'answer'+ii;
				span.textContent = answer[answer.length-ii-1];
				span.addEventListener('click',this.updateSum);
				div.appendChild(span);
		
		
		
			}
			el.appendChild(div);
		}
		else {
			div = document.createElement('div');
			div.classList.add('sumRow');
			var input = document.createElement('input');
			input.setAttribute('type','text');
			div.appendChild(input);
			el.appendChild(div);
		}
  }
  
  submitAnswer(){
		var answer = 0;
		if (this.sumButtons){
			var el = document.getElementById('asdBlock');
			var ell = el.querySelectorAll('.sumRow > span');
			for (var i=ell.length-1;i>=0;i--){
				if (isNaN(parseInt(ell[i].textContent))){
					answer *= 10;
				}
				else {
					answer *= 10;
					answer += parseInt(ell[i].textContent);
				}
			}
		}
		else {
			var el = document.getElementById('asdBlock');
			var ell = el.querySelector('.sumRow > input');
			answer = parseInt(ell.value);
		}
		var jsonmessage = {type:'arithmetic',subtype:'addition',message:[]};
		jsonmessage.message = [this.input_numbers[0],this.input_numbers[1],''+answer];
		ws.send(JSON.stringify(jsonmessage));
  }
  
  updateSum(evt){
		var el = evt.target;
		var x = parseInt(el.textContent);
		if (isNaN(x)){
			x = 0;
		}
		if (x<9){
			x++;
		}
		el.textContent = x;
  }
  
}

customElements.define('me-asm', asmElement);




var ws = new WebSocket('wss://matherrors.com:8080');
ws.onopen = function(evt) {
	var jsonmessage = {'operation':'key','message':key};
	ws.send(JSON.stringify(jsonmessage));
}
ws.onmessage = function(evt){
	var dm = JSON.parse(evt.data);
	var question = dm.question;
	var id = dm.id;
	var el = document.getElementById('me-'+id);
	el.newQuestion(question[0],question[1],question[2]);
	console.log(dm.update);
	
}