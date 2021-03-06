class chartdnChart extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
	var _this = this;
    const shadowRoot = this.attachShadow({mode: 'open'});
  	shadowRoot.innerHTML = `<div class="chart-container" style="position: relative;">
		<canvas id="myChart" style="display: none;"></canvas>
	</div>`;
	if (this.getAttribute('data-style') != 'chartJS'){
		this.chgType(this.getAttribute('data-style'));
	}
	
	googleEl = shadowRoot.querySelector('#googleChart');
	
  }
  
  makeChartjs(chartJSON) {
  	
  	this.shadowRoot.querySelector('#myChart').style.display = 'block';
  	var ctx = this.shadowRoot.querySelector('#myChart').getContext('2d');
	var myLineChart = new Chart(ctx, chartJSON);
  }
  makeXkcd(chartJSON) {
  	this.shadowRoot.querySelector('#xkcdSvg').style.display = 'block';
	const lineChart = new chartXkcd.Line(this.shadowRoot.querySelector('#xkcdSvg'), chartJSON);
  }
  makeGoogle(chartJSON) {
  	googleArray = chartJSON.retArray;
  	googleOptions = chartJSON.options;
    var el = this.shadowRoot.querySelector('#googleChart');
  	el.style.display = 'block';
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawChart);
  }
  makePlotly(chartJSON){
  	this.shadowRoot.querySelector('#plotlyDiv').style.display = 'block';

	Plotly.newPlot(this.shadowRoot.querySelector('#plotlyDiv'), chartJSON.data, chartJSON.options);
  }
  
  
  makeChart(chartJSON){
  	if (this.getAttribute('data-style') == 'XKCD'){
  		this.makeXkcd(chartJSON);
  	}
  	else if (this.getAttribute('data-style') == 'google'){
  		this.makeGoogle(chartJSON);
  	}
  	else if (this.getAttribute('data-style') == 'plotly'){
  		this.makePlotly(chartJSON);
  	}
  	else {
  		this.makeChartjs(chartJSON);
  	}
  }
  chgType(style) {
  	if (style == 'XKCD'){
  		this.shadowRoot.innerHTML = `<div class="chart-container" style="position: relative;">
					<svg id="xkcdSvg" style="display: none;"></svg>
				</div>`;
  	}
  	else if (style == 'google') {
  		this.shadowRoot.innerHTML = `<div class="chart-container" style="position: relative;">
					<div id="googleChart" style="display: none;"></div>
				</div>`;
  	}
  	else if (style == 'plotly') {
  		this.shadowRoot.innerHTML = `<style>.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
    font-family:'Open Sans', verdana, arial, sans-serif;
    margin:0;
    padding:0;
}

.js-plotly-plot .plotly input, .js-plotly-plot .plotly button {
    font-family:'Open Sans', verdana, arial, sans-serif;
}

.js-plotly-plot .plotly input:focus,.js-plotly-plot .plotly button:focus {
    outline:none;
}

.js-plotly-plot .plotly a {
    text-decoration:none;
}

.js-plotly-plot .plotly a:hover {
    text-decoration:none;
}

.js-plotly-plot .plotly .crisp {
    shape-rendering:crispEdges;
}

.js-plotly-plot .plotly .user-select-none {
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    -o-user-select:none;
    user-select:none;
}

.js-plotly-plot .plotly svg {
    overflow:hidden;
}

.js-plotly-plot .plotly svg a {
    fill:#447adb;
}

.js-plotly-plot .plotly svg a:hover {
    fill:#3c6dc5;
}

.js-plotly-plot .plotly .main-svg {
    position:absolute;
    top:0;
    left:0;
    pointer-events:none;
}

.js-plotly-plot .plotly .main-svg .draglayer {
    pointer-events:all;
}

.js-plotly-plot .plotly .cursor-default {
    cursor:default;
}

.js-plotly-plot .plotly .cursor-pointer {
    cursor:pointer;
}

.js-plotly-plot .plotly .cursor-crosshair {
    cursor:crosshair;
}

.js-plotly-plot .plotly .cursor-move {
    cursor:move;
}

.js-plotly-plot .plotly .cursor-col-resize {
    cursor:col-resize;
}

.js-plotly-plot .plotly .cursor-row-resize {
    cursor:row-resize;
}

.js-plotly-plot .plotly .cursor-ns-resize {
    cursor:ns-resize;
}

.js-plotly-plot .plotly .cursor-ew-resize {
    cursor:ew-resize;
}

.js-plotly-plot .plotly .cursor-sw-resize {
    cursor:sw-resize;
}

.js-plotly-plot .plotly .cursor-s-resize {
    cursor:s-resize;
}

.js-plotly-plot .plotly .cursor-se-resize {
    cursor:se-resize;
}

.js-plotly-plot .plotly .cursor-w-resize {
    cursor:w-resize;
}

.js-plotly-plot .plotly .cursor-e-resize {
    cursor:e-resize;
}

.js-plotly-plot .plotly .cursor-nw-resize {
    cursor:nw-resize;
}

.js-plotly-plot .plotly .cursor-n-resize {
    cursor:n-resize;
}

.js-plotly-plot .plotly .cursor-ne-resize {
    cursor:ne-resize;
}

.js-plotly-plot .plotly .modebar {
    position:absolute;
    top:2px;
    right:2px;
    z-index:1001;
    background:rgba(255,255,255,0.7);
}

.js-plotly-plot .plotly .modebar--hover {
    opacity:0;
    -webkit-transition:opacity 0.3s ease 0s;
    -moz-transition:opacity 0.3s ease 0s;
    -ms-transition:opacity 0.3s ease 0s;
    -o-transition:opacity 0.3s ease 0s;
    transition:opacity 0.3s ease 0s;
}

.js-plotly-plot .plotly:hover .modebar--hover {
    opacity:1;
}

.js-plotly-plot .plotly .modebar-group {
    float:left;
    display:inline-block;
    box-sizing:border-box;
    margin-left:8px;
    position:relative;
    vertical-align:middle;
    white-space:nowrap;
}

.js-plotly-plot .plotly .modebar-group:first-child {
    margin-left:0px;
}

.js-plotly-plot .plotly .modebar-btn {
    position:relative;
    font-size:16px;
    padding:3px 4px;
    cursor:pointer;
    line-height:normal;
    box-sizing:border-box;
}

.js-plotly-plot .plotly .modebar-btn svg {
    position:relative;
    top:2px;
}

.js-plotly-plot .plotly .modebar-btn path {
    fill:rgba(0,31,95,0.3);
}

.js-plotly-plot .plotly .modebar-btn.active path,.js-plotly-plot .plotly .modebar-btn:hover path {
    fill:rgba(0,22,72,0.5);
}

.js-plotly-plot .plotly .modebar-btn.modebar-btn--logo {
    padding:3px 1px;
}

.js-plotly-plot .plotly .modebar-btn.modebar-btn--logo path {
    fill:#447adb !important;
}

.js-plotly-plot .plotly [data-title]:before,.js-plotly-plot .plotly [data-title]:after {
    position:absolute;
    -webkit-transform:translate3d(0, 0, 0);
    -moz-transform:translate3d(0, 0, 0);
    -ms-transform:translate3d(0, 0, 0);
    -o-transform:translate3d(0, 0, 0);
    transform:translate3d(0, 0, 0);
    display:none;
    opacity:0;
    z-index:1001;
    pointer-events:none;
    top:110%;
    right:50%;
}

.js-plotly-plot .plotly [data-title]:hover:before,.js-plotly-plot .plotly [data-title]:hover:after {
    display:block;
    opacity:1;
}

.js-plotly-plot .plotly [data-title]:before {
    content:'';
    position:absolute;
    background:transparent;
    border:6px solid transparent;
    z-index:1002;
    margin-top:-12px;
    border-bottom-color:#69738a;
    margin-right:-6px;
}

.js-plotly-plot .plotly [data-title]:after {
    content:attr(data-title);
    background:#69738a;
    color:white;
    padding:8px 10px;
    font-size:12px;
    line-height:12px;
    white-space:nowrap;
    margin-right:-18px;
    border-radius:2px;
}

.js-plotly-plot .plotly .select-outline {
    fill:none;
    stroke-width:1;
    shape-rendering:crispEdges;
}

.js-plotly-plot .plotly .select-outline-1 {
    stroke:white;
}

.js-plotly-plot .plotly .select-outline-2 {
    stroke:black;
    stroke-dasharray:2px 2px;
}

.plotly-notifier {
    font-family:'Open Sans';
    position:fixed;
    top:50px;
    right:20px;
    z-index:10000;
    font-size:10pt;
    max-width:180px;
}

.plotly-notifier p {
    margin:0;
}

.plotly-notifier .notifier-note {
    min-width:180px;
    max-width:250px;
    border:1px solid #fff;
    z-index:3000;
    margin:0;
    background-color:#8c97af;
    background-color:rgba(140,151,175,0.9);
    color:#fff;
    padding:10px;
}

.plotly-notifier .notifier-close {
    color:#fff;
    opacity:0.8;
    float:right;
    padding:0 5px;
    background:none;
    border:none;
    font-size:20px;
    font-weight:bold;
    line-height:20px;
}

.plotly-notifier .notifier-close:hover {
    color:#444;
    text-decoration:none;
    cursor:pointer;
}</style><div class="chart-container" style="position: relative;">
					<div id="plotlyDiv" style="display: none;"></div>
				</div>`;
  	}
  	else if (style == 'chartJS') {
  		this.shadowRoot.innerHTML = `<div class="chart-container" style="position: relative;">
			<canvas id="myChart" style="display: none;"></canvas>
		</div>`;
  	}
  	
  	
  }
}
var googleEl;
var googleArray;
var googleOptions;
function drawChart() {
  	var data = google.visualization.arrayToDataTable(googleArray);
	var chart = new google.visualization.LineChart(googleEl);
	chart.draw(data, googleOptions);
}
customElements.define('chartdn-chart', chartdnChart);
