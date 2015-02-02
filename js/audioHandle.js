var preloadCount = 0;

function playAudio(pan, start) { // pan : -1(left) ~ 1(right)
    var splitter = context.createChannelSplitter(2);
    var merger = context.createChannelMerger(2);
    var gainL = context.createGain();
    var gainR = context.createGain();

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

    // connection 
    splitter.connect(gainL, 0);
    splitter.connect(gainR, 1);

    gainL.connect(merger, 0, 0);
    gainR.connect(merger, 0, 1);

    merger.connect(context.destination);
 
   
//    getData(url);
 
    source.connect(splitter);
 
    source.start(0);
}


function stopAudio() {
    source.stop(0);
}


function preload(url) {
  source = context.createBufferSource();
  request = new XMLHttpRequest();

  request.open('GET', url, true);

  request.responseType = 'arraybuffer';

  request.onload = function() {
      preloadCount++;
      console.log("preloadCount : " + preloadCount);

      var loadProgress = document.getElementById("progress");
      loadProgress.innerHTML = preloadCount + "/" + numOfSound;      
      
      if(preloadCount == numOfSound){
          console.log("All files loaded.");
          $(".host").hide(1);
          buttonActivated = 1;
          console.log("buttonActivated: " + buttonActivated);
      }
  }


  request.send();
}


function getData(url) {
  source = context.createBufferSource();
  request = new XMLHttpRequest();

  request.open('GET', url, true);

  request.responseType = 'arraybuffer';

  request.onload = function() {
    var audioData = request.response;

    context.decodeAudioData(audioData, function(buffer) {
        source.buffer = buffer;
        console.log("Data loaded.");
      },

      function(e){"Error with decoding audio data" + e.err});
  }

  request.send();
}


function prePlay(){

    var loadProgressComment = document.getElementById("comment");
    var loadProgress = document.getElementById("progress");
    var loadProgressKind = document.getElementById("progressKind");
    loadProgressComment.innerHTML = "sound preloading...";      
    loadProgress.innerHTML = j + "/" + numOfVoice;      
    loadProgressKind.innerHTML = i + "/" + numOfKind; 
    
    var src = "./audio/t2/" + i + "/" + j + ".mp3";
    $('#audioplay').attr('src', src);
    audio.play();
}


function preloadAudio() {
    var body = document.getElementById("body_t1");
    if (body){
    
    for (i = 1; i < (numOfSound + 1); i++) {
        var src = "./audio/t1/" + i + ".mp3";
        preload(src);
    }
    console.log("T1_Preload audio files finished.");
    }

    /*
    var body2 = document.getElementById("body_t2");
    if (body2){
        i = 1;
        j = 1;
        prePlay();

        $("#audioplay").bind('ended', function(){
            j++;
//            console.log("j :" + j);
            if (j == 7){
                i++;
//                console.log("i :" + i);
                j = 1;
            }

            if (i < 21) {
                prePlay();
            }else if (i == 21){
                $(".host").hide(1);
                console.log("T2_Preload audio files finished.");
            }
        });
    }
*/

}



window.addEventListener('load', preloadAudio );
