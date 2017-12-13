var context, sampleBuffers, audioAvailable;

function decodeComplete(sampleId, buffer) {
    sampleBuffers[sampleId] = buffer;
}

function onError() {
    alert('An error occurred');
}

function initAudio() {
    try {
        context = new (window.AudioContext || window.webkitAudioContext)();
        audioAvailable = true;
    } catch(e) {
        audioAvailable = false;
        return;
    }
    sampleBuffers = {};
    loadAudioSet('en');
}

function changeAudioSet(lang) {
    loadAudioSet(lang);
}

function loadAudioSet(lang) {
    if (lang) {
        var url = AUDIO_LIST_URL + "?lang=" + lang;
        $.getJSON(url, function(data) {
            if (data) {
                sampleBuffers = {};
                for (var i = 0, end = data.length; i < end; i++) {
                    var path = AUDIO_DIR + "/" + lang + "/" + data[i];
                    var colCode = data[i].split('.')[0];
                    loadSound(path, colCode);
                }
            }
        });
    }
}

function loadSound(url, sampleId) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';

    request.onload = function() {
        context.decodeAudioData(request.response, decodeComplete.bind(this, sampleId), onError);
    }
    request.send();
}

function playSound(hexcode) {
    var sampleId = hexcode.substr(1);
    var source = context.createBufferSource();

    if (sampleBuffers[sampleId] !== undefined) {
        source.buffer = sampleBuffers[sampleId];
        source.connect(context.destination);
        try {
            source.start(0)
        } catch(e) {
            source.noteOn(0);
        }
    }
}

export { initAudio };
