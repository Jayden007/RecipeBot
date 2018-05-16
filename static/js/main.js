$(function () {
  if (typeof webkitSpeechRecognition != 'function') {
    alert('크롬에서만 동작 합니다.');
    return false;
  }

  var recognition = new webkitSpeechRecognition();
  var isRecognizing = false;
  var ignoreOnend = false;
  var finalTranscript = '';
  var audio = document.getElementById('audio');
  var $btnMic = $('#btn-mic');
  var $result = $('#result');
  var $iconMusic = $('#icon-music');
  var $messages = $('.messages-content'),
    d, h, m, i = 0;
  recognition.continuous = true;
  recognition.interimResults = false;

  $(window).load(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
      //fakeMessage();
    }, 100);
  });

  recognition.onstart = function () {
    console.log('onstart', arguments);
    isRecognizing = true;

    $btnMic.attr('class', 'message-submit-on');
  };

  recognition.onend = function () {
    console.log('onend', arguments);
    isRecognizing = false;

    if (ignoreOnend) {
      return false;
    }

    // DO end process
    $btnMic.attr('class', 'message-submit');
    if (!finalTranscript) {
      console.log('empty finalTranscript');
      return false;
    }

    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    }

  };

  function interact(message) {
    // loading message
    $('<div class="message loading new"><figure class="avatar"><img src="static/res/bananas.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    // make a POST request [ajax call]
    $.post('/message', {
      msg: message,
    }).done(function(reply) {
      // Message Received
      // 	remove loading meassage
      $('.message.loading').remove();
      // Add message to chatbox
      $('<div class="message new"><figure class="avatar"><img src="static/res/bananas.png" /></figure>' + reply['text'] + '</div>').appendTo($('.mCSB_container')).addClass('new');
      textToSpeech(reply['text']);
      setDate();
      updateScrollbar();
  
    
  
      /*
      var audio = document.getElementById('player');
  
      audio.setAttribute('preload', "none");
      audio.setAttribute('src', 'tts_out/' + reply['text']);
      audio.play();
      */
      }).fail(function() {
          alert('error calling function');
          });
  }

  recognition.onresult = function (event) {
    console.log('onresult', event);

    var interimTranscript = '';
    if (typeof (event.results) == 'undefined') {
      recognition.onend = null;
      recognition.stop();
      return;
    }
    //console.log('1111', event.results.length-1);
    
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript = event.results[i][0].transcript;
      } else {
        interimTranscript = event.results[i][0].transcript;
      }
    }

    finalTranscript = capitalize(finalTranscript);

    if ($.trim(finalTranscript) == '') {
      return false;
    }
    $('<div class="message message-personal">' + finalTranscript + '</div>').appendTo($('.mCSB_container')).addClass('new');
    console.log('finalTranscript1=', finalTranscript);
    setDate();
    console.log('finalTranscript2=', finalTranscript);
    interact(finalTranscript);
    updateScrollbar();
    setTimeout(function () {
      //fakeMessage();
    }, 1000 + (Math.random() * 20) * 100);
    /* messages_span.innerHTML = linebreak(finalTranscript);

    /*
    console.log('finalTranscript', finalTranscript);
    console.log('interimTranscript', interimTranscript);
    */
    fireCommand(interimTranscript);
  };

  function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
      scrollInertia: 10,
      timeout: 0
    });
  }

  function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
      m = d.getMinutes();
      $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
  }

  

  /**
   * changeColor
   *
   */
  /*
	  .red 		{ background: red; }
		.blue 	{ background: blue; }
		.green 	{ background: green; }
		.yellow { background: yellow; }
		.orange { background: orange; }
		.grey 	{ background: grey; }
		.gold   { background: gold; }
		.white 	{ background: white; }
		.black  { background: black; }
 	*/
  function fireCommand(string) {
    if (string.endsWith('레드')) {
      $result.attr('class', 'red');
    } else if (string.endsWith('블루')) {
      $result.attr('class', 'blue');
    } else if (string.endsWith('그린')) {
      $result.attr('class', 'green');
    } else if (string.endsWith('옐로우')) {
      $result.attr('class', 'yellow');
    } else if (string.endsWith('오렌지')) {
      $result.attr('class', 'orange');
    } else if (string.endsWith('그레이')) {
      $result.attr('class', 'grey');
    } else if (string.endsWith('골드')) {
      $result.attr('class', 'gold');
    } else if (string.endsWith('화이트')) {
      $result.attr('class', 'white');
    } else if (string.endsWith('블랙')) {
      $result.attr('class', 'black');
    } else if (string.endsWith('알람') || string.endsWith('알 람')) {
      alert('알람');
    } else if (string.endsWith('노래 켜') || string.endsWith('음악 켜')) {
      audio.play();
      $iconMusic.addClass('visible');
    } else if (string.endsWith('노래 꺼') || string.endsWith('음악 꺼')) {
      audio.pause();
      $iconMusic.removeClass('visible');
    } else if (string.endsWith('볼륨 업') || string.endsWith('볼륨업')) {
      audio.volume += 0.2;
    } else if (string.endsWith('볼륨 다운') || string.endsWith('볼륨다운')) {
      audio.volume -= 0.2;
    } else if (string.endsWith('스피치') || string.endsWith('말해줘') || string.endsWith('말 해 줘')) {
      textToSpeech($('#messages_span').text() || '전 음성 인식된 글자를 읽습니다.');
    }
  }

  recognition.onerror = function (event) {
    console.log('onerror', event);

    if (event.error == 'no-speech') {
      ignoreOnend = true;
    } else if (event.error == 'audio-capture') {
      ignoreOnend = true;
    } else if (event.error == 'not-allowed') {
      ignoreOnend = true;
    }

    $btnMic.attr('class', 'message-submit');
  };

  var two_line = /\n\n/g;
  var one_line = /\n/g;
  var first_char = /\S/;

  function linebreak(s) {
    return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
  }

  function capitalize(s) {
    return s.replace(first_char, function (m) {
      return m.toUpperCase();
    });
  }

  function start(event) {
    if (isRecognizing) {
      recognition.stop();
      return;
    }
    recognition.lang = 'ko-KR';
    recognition.start();
    ignoreOnend = false;

    finalTranscript = '';
  }

  /**
   * textToSpeech
   * 지원: 크롬, 사파리, 오페라, 엣지
   */
  function textToSpeech(text) {
    console.log('textToSpeech', arguments);

    /*
    var u = new SpeechSynthesisUtterance();
    u.text = 'Hello world';
    u.lang = 'en-US';
    u.rate = 1.2;
    u.onend = function(event) {
      log('Finished in ' + event.elapsedTime + ' seconds.');
    };
    speechSynthesis.speak(u);
    */

    // simple version
    speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  }

  /**
   * requestServer
   * key - AIzaSyDiMqfg8frtoZflA_2LPqfGdpjmgTMgWhg
   */
  function requestServer() {
    $.ajax({
      method: 'post',
      url: 'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyDiMqfg8frtoZflA_2LPqfGdpjmgTMgWhg',
      data: '/examples/speech-recognition/hello.wav',
      contentType: 'audio/l16; rate=16000;', // 'audio/x-flac; rate=44100;',
      success: function (data) {

      },
      error: function (xhr) {

      }
    });
  }

  /**
   * init
   */
  $btnMic.click(start);
  $('#btn-tts').click(function () {
    textToSpeech($('#messages_span').text() || '전 음성 인식된 글자를 읽습니다.');
  });
});