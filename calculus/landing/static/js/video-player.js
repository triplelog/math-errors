(function () {
	'use strict';
	// Does the browser actually support the video element?
	var supportsVideo = !!document.createElement('video').canPlayType;

	if (supportsVideo) {
		// Obtain handles to main elements
		var videoContainer = document.getElementById('videoContainer');
		var video = document.getElementById('video');
		var videoControls = document.getElementById('video-controls');

		// Hide the default controls
		video.controls = false;

		// Display the user defined video controls
		videoControls.setAttribute('data-state', 'visible');

		// Obtain handles to buttons and other elements
		var backone = document.getElementById('backone');
		var playpause = document.getElementById('playpause');
		var forwardone = document.getElementById('forwardone');
		var mute = document.getElementById('mute');
		var volinc = document.getElementById('volinc');
		var voldec = document.getElementById('voldec');
		var progress = document.getElementById('progress');
		var progressOver = document.getElementById('progressOver');
		var progressBar = document.getElementById('progress-bar');
		var fullscreen = document.getElementById('fs');
		var figcaption = document.getElementById('figcaption');


		progress.setAttribute('data-state', 'fake');
		var itv = setInterval(function() {
			if(video.readyState > 0) {
				for (var i=0;i<steps.length;i++) {
					var node = document.createElement("span");
					node.classList.add("progressProduct");
					node.classList.add("progressType");
					node.style.width = steps[i].time*100.0/video.duration+"%";
					node.style.backgroundColor = steps[i].type;
					node.addEventListener("mouseover", chgFigCaption.bind(null,i), false);
					progressOver.appendChild(node);
					
				}
				for (var i = 0; i < video.textTracks.length; i++) {
				   video.textTracks[i].mode = 'hidden';
				}

				// (Put the minutes and seconds in the display)

				clearInterval(itv);
			}
		}, 200);
		
		function chgFigCaption(i) {
			figcaption.innerHTML = steps[i].text;
			katex.render(steps[i].text, figcaption, {throwOnError: false});
		}

		// Check if the browser supports the Fullscreen API
		var fullScreenEnabled = !!(document.fullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled || document.webkitSupportsFullscreen || document.webkitFullscreenEnabled || document.createElement('video').webkitRequestFullScreen);
		// If the browser doesn't support the Fulscreen API then hide the fullscreen button
		if (!fullScreenEnabled) {
			fullscreen.style.display = 'none';
		}

		// Check the volume
		var checkVolume = function(dir) {
			if (dir) {
				var currentVolume = Math.floor(video.volume * 10) / 10;
				if (dir === '+') {
					if (currentVolume < 1) video.volume += 0.1;
				}
				else if (dir === '-') {
					if (currentVolume > 0) video.volume -= 0.1;
				}
				// If the volume has been turned off, also set it as muted
				// Note: can only do this with the custom control set as when the 'volumechange' event is raised, there is no way to know if it was via a volume or a mute change
				if (currentVolume <= 0) video.muted = true;
				else video.muted = false;
			}
			changeButtonState('mute');
		}

		// Change the volume
		var alterVolume = function(dir) {
			checkVolume(dir);
		}

		// Set the video container's fullscreen state
		var setFullscreenData = function(state) {
			videoContainer.setAttribute('data-fullscreen', !!state);
			// Set the fullscreen button's 'data-state' which allows the correct button image to be set via CSS
			fullscreen.setAttribute('data-state', !!state ? 'cancel-fullscreen' : 'go-fullscreen');
		}

		// Checks if the document is currently in fullscreen mode
		var isFullScreen = function() {
			return !!(document.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || document.fullscreenElement);
		}

		// Fullscreen
		var handleFullscreen = function() {
			// If fullscreen mode is active...	
			if (isFullScreen()) {
					// ...exit fullscreen mode
					// (Note: this can only be called on document)
					if (document.exitFullscreen) document.exitFullscreen();
					else if (document.mozCancelFullScreen) document.mozCancelFullScreen();
					else if (document.webkitCancelFullScreen) document.webkitCancelFullScreen();
					else if (document.msExitFullscreen) document.msExitFullscreen();
					setFullscreenData(false);
				}
				else {
					// ...otherwise enter fullscreen mode
					// (Note: can be called on document, but here the specific element is used as it will also ensure that the element's children, e.g. the custom controls, go fullscreen also)
					if (videoContainer.requestFullscreen) videoContainer.requestFullscreen();
					else if (videoContainer.mozRequestFullScreen) videoContainer.mozRequestFullScreen();
					else if (videoContainer.webkitRequestFullScreen) {
						// Safari 5.1 only allows proper fullscreen on the video element. This also works fine on other WebKit browsers as the following CSS (set in styles.css) hides the default controls that appear again, and 
						// ensures that our custom controls are visible:
						// figure[data-fullscreen=true] video::-webkit-media-controls { display:none !important; }
						// figure[data-fullscreen=true] .controls { z-index:2147483647; }
						video.webkitRequestFullScreen();
					}
					else if (videoContainer.msRequestFullscreen) videoContainer.msRequestFullscreen();
					setFullscreenData(true);
				}
			}
		
		// Only add the events if addEventListener is supported (IE8 and less don't support it, but that will use Flash anyway)
		if (document.addEventListener) {
			// Wait for the video's meta data to be loaded, then set the progress bar's max value to the duration of the video
			video.addEventListener('loadedmetadata', function() {
				progress.setAttribute('max', video.duration);
			});

			// Changes the button state of certain button's so the correct visuals can be displayed with CSS
			var changeButtonState = function(type) {
				// Play/Pause button
				if (type == 'playpause') {
					if (video.paused || video.ended) {
						playpause.setAttribute('data-state', 'play');
					}
					else {
						playpause.setAttribute('data-state', 'pause');
					}
				}
				// Mute button
				else if (type == 'mute') {
					mute.setAttribute('data-state', video.muted ? 'unmute' : 'mute');
				}
			}

			// Add event listeners for video specific events
			video.addEventListener('play', function() {

				changeButtonState('playpause');
			}, false);
			video.addEventListener('pause', function() {
				changeButtonState('playpause');
			}, false);
			video.addEventListener('volumechange', function() {
				checkVolume();
			}, false);

			// Add events for all buttons			
			playpause.addEventListener('click', function(e) {
				if (video.paused || video.ended) video.play();
				else video.pause();
			});			

			// Go to next step
			forwardone.addEventListener('click', function(e) {
				var totalTime = 0
				for (var i=0;i<steps.length;i++) {
					totalTime += steps[i].time;
					if (video.currentTime < totalTime) {
						video.currentTime = totalTime;
						progress.value = totalTime;
						break;
					}
				}
				
			});
			backone.addEventListener('click', function(e) {
				var totalTime = 0
				for (var i=0;i<steps.length;i++) {
					totalTime += steps[i].time;
					if (video.currentTime < totalTime + 1) {
						if (i>0){
							video.currentTime = totalTime - steps[i].time;
							progress.value = totalTime - steps[i].time;
							break;
						}
						else {
							video.currentTime = 0;
							progress.value = 0;
							break;
						}
					}
				}
			});
			mute.addEventListener('click', function(e) {
				if (video.muted) {
					for (var i = 0; i < video.textTracks.length; i++) {
					   video.textTracks[i].mode = 'hidden';
					}
				}
				else{
					for (var i = 0; i < video.textTracks.length; i++) {
					   video.textTracks[i].mode = 'showing';
					}
				}

				video.muted = !video.muted;
				changeButtonState('mute');
			});
			volinc.addEventListener('click', function(e) {
				alterVolume('+');
			});
			voldec.addEventListener('click', function(e) {
				alterVolume('-');
			});
			fs.addEventListener('click', function(e) {
				handleFullscreen();
			});

			// As the video is playing, update the progress bar
			video.addEventListener('timeupdate', function() {
				// For mobile browsers, ensure that the progress element's max attribute is set
				if (!progress.getAttribute('max')) progress.setAttribute('max', video.duration);
				progress.value = video.currentTime;
				progressBar.style.width = Math.floor((video.currentTime / video.duration) * 100) + '%';
			});

			// React to the user clicking within the progress bar
			progressOver.addEventListener('click', function(e) {
				//var pos = (e.pageX  - this.offsetLeft) / this.offsetWidth; // Also need to take the parent into account here as .controls now has position:relative
				var pos = (e.pageX  - (this.offsetLeft + this.offsetParent.offsetLeft)) / this.offsetWidth;
				video.currentTime = pos * video.duration;
			});

			// Listen for fullscreen change events (from other controls, e.g. right clicking on the video itself)
			document.addEventListener('fullscreenchange', function(e) {
				setFullscreenData(!!(document.fullScreen || document.fullscreenElement));
			});
			document.addEventListener('webkitfullscreenchange', function() {
				setFullscreenData(!!document.webkitIsFullScreen);
			});
			document.addEventListener('mozfullscreenchange', function() {
				setFullscreenData(!!document.mozFullScreen);
			});
			document.addEventListener('msfullscreenchange', function() {
				setFullscreenData(!!document.msFullscreenElement);
			});
		}
	 }

 })();