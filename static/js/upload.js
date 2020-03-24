var ctypestr = "";
var filen = "";
var syncWorker = new Worker('../wasm/uploadworker.js');
var syncWorker2 = new Worker('../wasm/datatypeworker.js');

document.getElementById('dropArea').addEventListener('drop', handleDrop, false);
var names = ['dragenter', 'dragover', 'dragleave', 'drop'];
names.forEach(eventName => {
  document.getElementById('dropArea').addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
	e.preventDefault();
    e.stopPropagation();
}
function handleDrop(e) {
  
  let dt = e.dataTransfer;
  let files = dt.files;
  //document.getElementById('dropArea').style.display = 'none';
  var ffile = files[0];
	syncWorker.postMessage(ffile);
	syncWorker.onmessage = function(e) {
		//ctypestr = toTable(e.data.result,e.data.ctypestr);
		document.getElementById('dataTableModified').innerHTML = '';
		setTimeout(fullCompression,10,ffile);
	};
}


document.querySelector('#dataFile').addEventListener('change', function(inp) {
	
	//document.getElementById('dropArea').style.display = 'none';
	var ffile = this.files[0];
	syncWorker.postMessage(ffile);
	syncWorker.onmessage = function(e) {
		//ctypestr = toTable(e.data.result,e.data.ctypestr);
		
		//if (filen != ""){createConfirmForm();}
		document.getElementById('dataTableModified').innerHTML = '';
		setTimeout(fullCompression,10,ffile);
	};
	
	

}, false);



function fullCompression(to_compress) {
	var readerF = new FileReader();
	readerF.onload = function() {
		console.log("Compressing")
	
		var mybase64 = this.result;
		var index = mybase64.indexOf('base64,');
		var csvindex = mybase64.substring(0,index).indexOf('text/csv');
		
		if (csvindex>-1){
			mybase64 = mybase64.substring(index+7);
			var compbase64 = pako.deflate(mybase64,{to:'string'});
			dataChanged(btoa(compbase64));
		}
		else {
			var xlsindex = mybase64.substring(0,index).indexOf('excel');
			if (xlsindex>-1){
				mybase64 = mybase64.substring(index+7);
				dataChanged(mybase64,'xls');
			}
			else {
				var xlsxindex = mybase64.substring(0,index).indexOf('openxml');
				if (xlsxindex>-1) {
					mybase64 = mybase64.substring(index+7);
					dataChanged(mybase64,'xlsx');
				}
			}
		}

		

		
	}
	
	readerF.readAsDataURL(to_compress);
}


function toTable(input_str,ctypestr){
	
	var data = Papa.parse(input_str);
	var datatypes = [];
	var ncols = Math.max(data.data[0].length,data.data[1].length);
	
	var dataCopyStr = '';
	
	
	//var table = document.getElementById("dataTable");
	//table.innerHTML = '';
	//var thead = document.createElement("thead");
		//var tr = document.createElement("tr");
			for (var i=0;i<data.data[0].length;i++) {
				//var th = document.createElement("th");
				//var tdiv = document.createElement("div");
				//var tspan = document.createElement("span");
				//tspan.textContent = data.data[0][i]+' ';
				if (i<data.data[0].length-1){
					dataCopyStr += data.data[0][i]+', ';
				}
				else {
					dataCopyStr += data.data[0][i]+'\n';
				}
				
				//tdiv.appendChild(tspan);
				//th.appendChild(tdiv);
				//th.classList.add('rotate');
				//tr.appendChild(th);
				
			}
		//thead.appendChild(tr);
	//table.appendChild(thead);
	//var tbody = document.createElement("tbody");
		for (var ii=1;ii<data.data.length-1;ii++) {
			//var tr2 = document.createElement("tr");
			for (var i=0;i<data.data[ii].length;i++) {
				//var td = document.createElement("td");
				//td.textContent = data.data[ii][i];
				if (i<data.data[0].length-1){
					dataCopyStr += data.data[ii][i]+', ';
				}
				else {
					dataCopyStr += data.data[ii][i]+'\n';
				}
				//tr2.appendChild(td);
			}
			//tbody.appendChild(tr2);
		}
	//table.appendChild(tbody);
	document.getElementById('dataCopy').value = dataCopyStr;
	
	//var ctypestr = '-1';
	/*
	var cheaders = [];
	var dtypes = ctypestr.split(',');
	for (var i=1;i<dtypes.length;i++) {
		if (dtypes[i] == '1' ){
			cheaders.push('Number');
		}
		else if (dtypes[i] == '2'){
			cheaders.push('Date');
		}
		else if (dtypes[i] == '0'){
			cheaders.push('String');
		}
		else {
			cheaders.push('Unknown');
		}
	}
	var headRow = thead.querySelector('tr');
	var headCells = headRow.querySelectorAll('th');
	for (var i=0;i<cheaders.length;i++){
		var th = headCells[i];
		var tdiv = th.querySelector("div");
		var tspan = tdiv.querySelector("span");
		tspan.innerHTML += ' <a href="#">'+cheaders[i]+'</a>';
	}
	*/
	return ctypestr;
}

function isMonth(input_str){
	input_str = input_str.replace('.','');
	if (input_str == 'january') {return true;}
	if (input_str == 'jan') {return true;}
	if (input_str == 'february') {return true;}
	if (input_str == 'feb') {return true;}
	if (input_str == 'march') {return true;}
	if (input_str == 'mar') {return true;}
	if (input_str == 'april') {return true;}
	if (input_str == 'apr') {return true;}
	if (input_str == 'may') {return true;}
	if (input_str == 'june') {return true;}
	if (input_str == 'jun') {return true;}
	if (input_str == 'july') {return true;}
	if (input_str == 'jul') {return true;}
	if (input_str == 'august') {return true;}
	if (input_str == 'aug') {return true;}
	if (input_str == 'september') {return true;}
	if (input_str == 'sep') {return true;}
	if (input_str == 'october') {return true;}
	if (input_str == 'oct') {return true;}
	if (input_str == 'november') {return true;}
	if (input_str == 'nov') {return true;}
	if (input_str == 'december') {return true;}
	if (input_str == 'dec') {return true;}
	return false;
}
function isDate(input_str){
	var threeparts = input_str.split('/');
	if (threeparts.length == 3) {
		if (parseInt(threeparts[0]) > 0 && parseInt(threeparts[0]) < 13 && parseInt(threeparts[0]).toString() == threeparts[0]){
			if (parseInt(threeparts[1]) > 0 && parseInt(threeparts[1]) < 32 && parseInt(threeparts[1]).toString() == threeparts[1]){
				if (parseInt(threeparts[2]).toString() == threeparts[2]){
					return 'MM/DD/YYYY';
				}
			}
		}
		if (parseInt(threeparts[0]) > 0 && parseInt(threeparts[0]) < 32 && parseInt(threeparts[0]).toString() == threeparts[0]){
			if (parseInt(threeparts[1]) > 0 && parseInt(threeparts[1]) < 12 && parseInt(threeparts[1]).toString() == threeparts[1]){
				if (parseInt(threeparts[2]).toString() == threeparts[2]){
					return 'DD/MM/YYYY';
				}
			}
		}
	}
	else if (threeparts.length == 2) {
		if (parseInt(threeparts[0]) > 0 && parseInt(threeparts[0]) < 13 && parseInt(threeparts[0]).toString() == threeparts[0]){
			if (parseInt(threeparts[1]) > 1500 && parseInt(threeparts[1]) < 2500 && parseInt(threeparts[1]).toString() == threeparts[1]){
				return 'MM/YYYY';
			}
		}
	}
	threeparts = input_str.replace(',','').split(' ');
	if (threeparts.length == 3) {
		if (isMonth(threeparts[0])){
			if (parseInt(threeparts[1]) > 0 && parseInt(threeparts[1]) < 32 && parseInt(threeparts[1]).toString() == threeparts[1]){
				if (parseInt(threeparts[2]).toString() == threeparts[2]){
					return 'MONTH DAY, YYYY';
				}
			}
		}
		if (parseInt(threeparts[0]) > 0 && parseInt(threeparts[0]) < 32 && parseInt(threeparts[0]).toString() == threeparts[0]){
			if (isMonth(threeparts[1])){
				if (parseInt(threeparts[2]).toString() == threeparts[2]){
					return 'DAY MONTH, YYYY';
				}
			}
		}
	}
	else if (threeparts.length == 2) {
		if (isMonth(threeparts[0])){
			if (parseInt(threeparts[1]) > 1500 && parseInt(threeparts[1]) < 2500 && parseInt(threeparts[1]).toString() == threeparts[1]){
				return 'MONTH YYYY';
			}
		}
	}
	return false;
}
function getDataType(input_str,head_str){
	input_str = input_str.trim().toLowerCase();
	head_str = head_str.trim().toLowerCase();
	if (input_str.length == 0) {
		return 'Blank';
	}
	else if (parseInt(input_str).toString() == input_str){
		if (head_str.indexOf('zip') == 0 && parseInt(input_str) <10000 && parseInt(input_str) > 0) {
			return 'Zip';
		}
		return 'Int';
	}
	else if (parseInt(input_str.replace('.','')).toString() == input_str.replace('.','')){
		if (head_str.indexOf('lat') == 0 && parseFloat(input_str) < 200 && parseFloat(input_str) > -200) {
			if (head_str.length < 6 || head_str.indexOf('latitude') == 0){
				return 'Lat';
			}
		}
		else if (head_str.indexOf('lon') == 0 && parseFloat(input_str) < 200 && parseFloat(input_str) > -200) {
			if (head_str.length < 6 || head_str.indexOf('longitude') == 0){
				return 'Lon';
			}
		}
		return 'Num';
	}
	else if (isDate(input_str)){
		return 'Date';//+isDate(input_str);
	}
	else if (parseInt(input_str.replace('/','')).toString() == input_str.replace('/','')){
		return 'Num';
	}
	else if (parseInt(input_str.replace('/','').replace('.','').replace('%','')).toString() == input_str.replace('/','').replace('.','').replace('%','')){
		return 'Percent';
	}
	else if (parseInt(input_str.replace('-','')).toString() == input_str.replace('-','')){
		if (input_str.length == 10 && input_str.indexOf('-') == 5) {
			return 'Zip';
		}
		else if (input_str.length == 8 && input_str.indexOf('-') == 3) {
			return 'Phone';
		}
	}
	else if (parseInt(input_str.replace('-','').replace('-','')).toString() == input_str.replace('-','').replace('-','')){
		if (input_str.length == 12 && input_str.indexOf('-') == 3) {
			return 'Phone';
		}
	}
	else if (input_str.indexOf('www.') > -1 || input_str.indexOf('http') > -1 || (input_str.indexOf('.com') > -1 && input_str.indexOf('@') == -1)){
		return 'Link';
	}
	else if ( (input_str.indexOf('.com') > -1 || input_str.indexOf('.edu') > -1 || input_str.indexOf('.org') > -1) && input_str.indexOf('@') > -1){
		return 'Email';
	}
	else if ( (input_str.indexOf('.com') == -1 && input_str.indexOf('.edu') == -1 && input_str.indexOf('.org') == -1) && input_str.indexOf('@') == 0){
		return 'Twitter';
	}
	
	return 'Not';
}