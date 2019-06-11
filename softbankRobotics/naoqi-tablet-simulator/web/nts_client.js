
/**
 * In this file, the word "tablet" will refer to the simulated tablet,
 * more precisely, to the div #tablet-main.
 * 
 * 
 */

// *** VARIABLES AND SETTINGS INITIALIZATION

var tablet = $("#tablet-main");
var image = $("#tablet-image");
var video = $("#tablet-video");
var webview = $("#tablet-webview-iframe");
webview.attr("src", "about:blank");

// make image not draggable
// because otherwise, when dragging image, 'mouseup' signal is not fired !
image.attr("draggable", false);

var connectionStatusDiv = $("#connection-status");

// tablet width & height are subject to change depending on Pepper model
//  for the first tablet it was 1708*1067
var width = 1280;
var height = 800;

var verbose = true;

var idle_screen_path = "idle_screen.png";
var screen_off_path = "screen_off.png";

var default_host = "127.0.0.1";
var default_port = "31415";

var host = default_host;
var port = default_port;

var wsStates = ['CONNECTING', 'OPEN', 'CLOSING', 'CLOSED'];
// websocket, connected later
var ws = null;


var returnValuesSent = [];

function debug(msg) {
  if (verbose) {
    console.log(msg);
  }
}

$("#host").val(host);
$("#port").val(port);

$("#connect").on("click", function() {
  console.log("connecting");
  ws.close();
  connectWebsocket();
});

$("#default-connection-settings").on("click", function() {
  $("#host").val(default_host);
  $("#port").val(default_port);
});

$("#select-screen-size").on("change", function() {
  debug(this.value);
  
  // screen size parameter was changed
  if (this.value == "1280") {
    width = 1280;
    height = 800;
  } else if (this.value == "1708") {
    width = 1708;
    height = 1067;
  }
  tablet.width(width);
  tablet.height(height);
});

$("#cb-debug").on("click", function() {
  if (this.checked) {
    verbose = true;
  } else {
    verbose = false;
  }
});

// *** WEBSOCKET SETUP

connectWebsocket = function() {
  
  ws = new WebSocket("ws://" + host + ":" + port + "/signal");

  ws.onmessage = function (evt) {
  var data = evt.data;
  debug("Received message : " + data);
  
  // here data is supposed to be JSON 

  var obj = jQuery.parseJSON(data);

  method = obj.method;
  args = obj.args;
  call_id = obj.call_id;

  if ( !tabletMethods.hasOwnProperty(method) ) {
    throw "No such method : " + method;
  }

  //TODO : protect if method already called (identical call_id), don't call the method twice

  // call the method with its arguments
  methodToCall = tabletMethods[method][0];
  requiredArgs = tabletMethods[method][1];
  checkArgsNumber(args, requiredArgs, methodToCall);

  var returnValue = null;


  // we add the call_id to the arguments
  // because some methods like showImage() need it
  if (args == null) {
    args = [call_id];
  } else {
    args.push(call_id);
  }

  returnValue = methodToCall(...args);

  // for some methods, we already returned the value
  // for the others, we have to send it now
  sendReturnValue(call_id, returnValue);
};

ws.onclose = function() {
  debug("WebSocket is closed.");
  
  connectionStatusDiv.html("WebSocket is closed (readyState = " + wsStates[ws.readyState] + ")");
  connectionStatusDiv.removeClass();
  connectionStatusDiv.addClass("red");
};

ws.onopen = function() {
    if(verbose) {
      console.log("connected");
    }
    connectionStatusDiv.html("Connected");
    connectionStatusDiv.removeClass();
    connectionStatusDiv.addClass("green");
  };

};


function sendReturnValue(call_id, value) {
  if (call_id == undefined) return;

  if (returnValuesSent.includes(call_id)) {
    // this method might be called multiple times
    //  for the same method call.
    // So we ensure to return a value at most once for each method call !
    debug("return value already sent for call_id " + call_id);
    return;
  }

  debug("sending return value for " + call_id + " : " + value);

  var data = JSON.stringify({
    "type":"return",
    "call_id":call_id,
    "value":value
  });
  ws.send(data);

  returnValuesSent.push(call_id);
}

// *** METHODS CALLED BY THE CLIENT

/**
 * Generic method equivalent to a signal sent by the tablet to the service
 * 
 */
function sendSignal(signal, args) {

  var data = JSON.stringify({
    "type":"signal",
    "signal":signal,
    "args":args
  });

  debug("sending : " + data);
  
  ws.send(data);
}

// click on the tablet <=> physical tablet touchDown
tablet.on("mousedown", function(event) {
  debug(event.offsetX + ", " + event.offsetY);
  
  var x = event.offsetX;
  var y = event.offsetY;

  sendSignal("onTouchDown", [
    x,
    y
  ]);

});

tablet.on("mouseup", function(event) {
  debug(event.offsetX + ", " + event.offsetY);
  
  var x = event.offsetX;
  var y = event.offsetY;

  sendSignal("onTouchUp", [
    x,
    y
  ]);

});

function checkArgsNumber(argsArray, requiredNumber, method) {
  if (argsArray == null && requiredNumber == 0) {
    return true;
  } else if (argsArray.length != requiredNumber) {
    throw "Invalid number of arguments for method " + method + "() - the method will not be called";
    return false;
  }
  return true;
}



// *** Equivalent of ALTabletService functions

function hideEverything() {
  image.attr("hidden", true);
  video.attr("hidden", true);
  webview.css("display", "none");
  tablet.css("background-color", "#ffffff");
}

hideEverything();

// Webview 

function cleanWebview() {
  debug("cleanWebview()");
  
  hideEverything();
  webview.attr("src", "about:blank");
  showIdleScreenImage();
  // no return value for cleanWebView(), according to the documentation
  //  (but in fact, the return value will actually be sent by the showImage() in the showIdleScreenImage() method... )
}

function executeJS() {
  debug("executeJS()");
  
  throw 'Not implemented yet';
}

function hideWebview() {
  debug("hideWebview()");
  
  hideEverything();
  showIdleScreenImage();
  return true;
}

function loadUrl(url) {
  debug("loadUrl(" + url + ")");
  
  hideEverything();
  //url = "http://" + host + ":" + port + "/webview/" + url;
  webview.attr("src", url);

  // TODO cases in which to return false !
  return true;
}

function showWebview() {
  debug("showWebview()");
  
  hideEverything();
  webview.css("display", "block");
  return true;
}

// Image

function setBackgroundColor(color) {
  debug("setBackgroundColor(" + color + ")");
  
  hideEverything();
  // parameter color shoud be an hexa color code
  tablet.css("background-color", color);
}

function showImage(path, call_id) {
  debug("showImage(" + path + ")");
  
  hideEverything();

  // these events will be triggered AFTER the end of the method call (after the image loading)
  // so the value return must be done inside these events
  //  because before that, we don't know the image has loaded or not
  image.on("load", function() {
    console.log("image is loaded - call_id = " + call_id);
    
    image.removeAttr("hidden");
    image.on("load", null);
    image.on("error", null);
    sendReturnValue(call_id, true);
  });
  
  image.on("error", function() {
    console.log("image error - call_id = " + call_id);
    image.attr("about:blank", path);
    image.on("load", null);
    image.on("error", null);
    sendReturnValue(call_id, false);
  });

  image.attr("src", path);
  // the return value will be sent by the events above, not here
  //return true;
}

function hideImage(call_id) {
  debug("hideImage()");
  
  image.attr("hidden", true);
  sendReturnValue(call_id, true);
  return true;
}

// Video

function isVideoPlaying() {
  // thanks to https://stackoverflow.com/questions/6877403/how-to-tell-if-a-video-element-is-currently-playing
  var playing = (video[0].currentTime > 0 && !video[0].paused && !video[0].ended && video[0].readyState > 2);
  return playing;
}

function getVideoLength() {
  debug("getVideoLength()");
  
  return video[0].duration*1000;
}

function getVideoPosition() {
  debug("getVideoPosition()");
  
  return video[0].currentTime*1000;
}

function playVideo(url) {
  debug("playVideo(" + url + ")");
  
  hideEverything();
  tablet.prepend(video);
  video.removeAttr("hidden");
  video.attr("src", url);
  video.attr("autoplay", true);
  
  //return isVideoPlaying();
  //  here it seems that although "autoplay" property has been set on the video,
  //  the video itself will not start until we exit this method 
  //    (thus, simply calling isVideoPlaying() here will return false)
  // TODO return value according to the doc (True if video is playing, false otherwise)
  // perhaps do it with events as we did for showImage() ?
  // or maybe call video.trigger("play") instead of "autoplay" ?
  return true;
}

function pauseVideo() {
  debug("pauseVideo()");
  
  video.trigger("pause");
  return isVideoPlaying();
}

function resumeVideo() {
  debug("resumeVideo()");
  
  video.trigger("play");
  return isVideoPlaying();
}

function stopVideo() {
  debug("stopVideo()");
  
  video.trigger("pause");
  video.removeAttr("src");
  video.attr("hidden", true);
  //TODO return value according to doc (True if video player is open, false otherwise.)
  return false;
}


// gather all the tablet methods, along with their number of required arguments
tabletMethods = {
  "cleanWebview": [ cleanWebview, 0 ],
  "hideWebview": [ hideWebview, 0 ],
  "loadUrl": [ loadUrl, 1 ],
  "showWebview": [ showWebview, 0 ],
  "setBackgroundColor": [ setBackgroundColor, 1 ],
  "showImage": [ showImage, 1 ],
  "hideImage": [ hideImage, 0 ],
  "playVideo": [ playVideo, 1 ],
  "pauseVideo": [ pauseVideo, 0 ],
  "resumeVideo": [ resumeVideo, 0 ],
  "stopVideo": [ stopVideo, 0 ],
  "getVideoLength": [ getVideoLength, 0 ],
  "getVideoPosition": [ getVideoPosition, 0 ],
};





function showIdleScreenImage() {
  showImage(idle_screen_path);
}

function showScreenOffImage() {
  showImage(screen_off_path);
}

// when the page loads

showIdleScreenImage();

connectWebsocket();
