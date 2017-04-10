var displayCentre;
var whiteTags;
var w;

function setup() {
    var $canv = $('#namerCanvas')
    w = $canv.width()
    console.log(w, h);
    var myCanvas = createCanvas(w, h);
    myCanvas.parent('namerCanvas');
    textAlign(CENTER);
    whiteTags = false;
    updateNames();
    $('#languageSelect').change(onLanguageSelectChange);
    $('#colourSelect').change(onColourSelectChange);
}

function onLanguageSelectChange(e) {
    updateNames();
}

function onColourSelectChange(e) {
    col = '#' + e.target.value;
    doQuery(col);
    ft = $.farbtastic('#colourpicker');
    ft.setColor(col);
}

function draw() {
}

function doQuery(hexcode, responseHandler) {
    hexcode = hexcode.substring(1)
    queryURL = url + '?colour=' + hexcode;
    loadJSON(queryURL, responseHandler);
}

function findCentre() {
    displayCentre = createVector(w / 2, h / 2);
    return displayCentre
}

function drawResponse(colour_matches) {
    background(128);
    displayCentre = findCentre();
    for (c of colour_matches.colours) {
        var pos = createVector(c.a, c.b);
        pos.mult(1.2);
        pos.x = -pos.x + 20; 
        pos.y = -pos.y;
        pos.add(displayCentre);
        if (c.d == 0.0) {
            if (whiteTags == false) {
                fill(c.red, c.green, c.blue, 255);
            }
            textSize(32);
        } else {
            if (whiteTags == false) {
                fill(c.red, c.green, c.blue, 200);
            }
            textSize(20);
        }
        text(c.name, pos.x, pos.y);
    }
}

function updateWithResponse(colour_matches) {
    console.log('in updateWithResponse()');
    c = colour_matches.colours[0]
    stroke(1)
    background(128);
    fill(c.red, c.green, c.blue);
    rect(w / 2 - 150, 0, 300, h - 2);
    console.log(colour_matches);
    $('#colourInfo').html(colour_matches.desc);
}

function updateNames() {
    var $languageSelect = $('#languageSelect')[0]
    $.get(coloursUrl + '?lang=' + $languageSelect.value, function (data) {
        $.each(data, function (i, x) {
            $('#colourSelect').append($('<option>', {value: x.hex, text: x.name}));
        })
    });
}
