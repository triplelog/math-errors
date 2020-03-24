var ws = new WebSocket('wss://chartdn.com:8080');
ws.onopen = function(evt) {
	var allcharts = document.querySelectorAll('chartdn-chart');
	for (var i=0;i<allcharts.length;i++){
		allcharts[i].setAttribute('data-loc',i);
		var jsonmessage = {'operation':'view','id':allcharts[i].getAttribute('src'),'loc':i,'style':allcharts[i].getAttribute('data-style')}
		ws.send(JSON.stringify(jsonmessage));
	}
}
ws.onmessage = function(evt){
	var dm;
	if (evt.data[0]=='{'){
		dm = JSON.parse(evt.data);
	}
	else {
		var strData = atob(evt.data);
		var charData = strData.split('').map(function(x){return x.charCodeAt(0);});
		var binData = new Uint8Array(charData);
		var newData = pako.inflate(binData,{to:'string'});
		dm = JSON.parse(newData);
	}
	if (dm.operation == 'chart'){
		var chartJSON = dm.message;
		var el = document.querySelector('chartdn-chart[data-loc="'+parseInt(dm.loc)+'"]');
		if (el){
			el.makeChart(chartJSON);
		}
	}
}

