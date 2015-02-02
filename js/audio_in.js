window.AudioContext = window.AudioContext ||
                      window.webkitAudioContext;

var context = new AudioContext();

function getInput(pan) { // pan output: -1(left) ~ 1(right)
    
    // audio input connect
    audioInput.connect(inputPoint);

    //console.log("maxChannelCount: " + context.destination.maxChannelCount);
    //console.log("numberOfInputs: " + context.destination.numberOfInputs);
    //console.log("numberOfOutputs: " + context.destination.numberOfOutputs);
    
    var splitter = context.createChannelSplitter(2);
    var merger = context.createChannelMerger(2);
    var gainL = context.createGain();
    var gainR = context.createGain();

    audioInput.connect(splitter);

    if (pan == 1) {
    gainL.gain.value = 1.0;
    gainR.gain.value = 0.0;
    }

    else if (pan == -1) {
    gainL.gain.value = 0.0;
    gainR.gain.value = 1.0;
    }

    else {
    gainL.gain.value = 1.0;
    gainR.gain.value = 1.0;
    }

    splitter.connect(gainL, 0);
    splitter.connect(gainR, 1);

    gainL.connect(merger, 0, 0);
    gainR.connect(merger, 0, 1);


    merger.connect(context.destination);
    //inputPoint.connect(context.destination);
    setupAnalyser(inputPoint);
}


function initAudio() {
        if (!navigator.getUserMedia)
            navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

    navigator.getUserMedia(
        {
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            },
        }, gotStream, errorCallback);
}

function gotStream(stream) {
    inputPoint = context.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = context.createMediaStreamSource(stream);
    audioInput = realAudioInput;

    setupAnalyser(inputPoint);
//    audioInput.connect(inputPoint);
//    inputPoint.connect(context.destination);
}


function setupAnalyser(audioSource) {

    javascriptNode = context.createScriptProcessor(2048, 1, 1);
    javascriptNode.connect(context.destination);

    javascriptNode.onaudioprocess = function() {
        var array = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(array);
        var average = getAverageVolume(array);

        var c = document.getElementById("audioDisplay"); 
        var ctx = c.getContext("2d");
        var graphSens = 8;
        var lineWidth = 1; 

       // var my_gradient = ctx.createLinearGradient(0, 0, 150, 0);
       // my_gradient.addColorStop(0, "black");
       // my_gradient.addColorStop(1, "white");
       // ctx.fillStyle = my_gradient;
        
//        console.log("average: " + average);         
        ctx.clearRect(0, 0, 400, 10);
        ctx.fillRect( (average*graphSens) - 400, lineWidth, 400, lineWidth);
    }


    analyser = context.createAnalyser();
    analyser.smoothingTimeConstant = 0.3;
    analyser.fftSize = 1024;

    // audio source -> analyser
    audioSource.connect(analyser);

    analyser.connect(javascriptNode);


    
}

function getAverageVolume(array) {
    var values = 0;
    var average;

    var length = array.length;

    for (var i = 0; i < length; i++) {
        values += array[i];
    }

    average = values / length;
    return average;
}



function errorCallback (e) {
    alert('Error getting audio');
    console.log(e);
    };

window.addEventListener('load', initAudio );


