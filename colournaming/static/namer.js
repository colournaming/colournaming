var displayCentre;
var whiteTags;

function setup() {
    createCanvas(displayWidth, displayHeight);
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

function doQuery(hexcode) {
    hexcode = hexcode.substring(1)
    queryURL = url + '?colour=' + hexcode;
    loadJSON(queryURL, drawResponse);
}

function findCentre() {
    if (windowWidth * windowHeight >= displayWidth * displayHeight) {
        x = displayWidth / 2;
        y = displayHeight / 2;
    } else {
        x = windowWidth / 2;
        y = windowHeight / 2;
    }
    if (displayHeight < 500) {
        yOffset = 175;
    } else if (displayHeight >= 500) {
        yOffset = 225;
    } else {
        yOffset = 300;
    }
    displayCentre = createVector(x, y - yOffset);
    return displayCentre
}

function drawResponse(colour_matches) {
    background(128);
    displayCentre = findCentre();
    for (c of colour_matches) {
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

function updateNames() {
    var $languageSelect = $('#languageSelect')[0]
    $.get(coloursUrl + '?lang=' + $languageSelect.value, function (data) {
        $.each(data, function (i, x) {
            $('#colourSelect').append($('<option>', {value: x.hex, text: x.name}));
        })
    });
}
