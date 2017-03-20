console.log(url)
var displayCentre;
var whiteTags;

function setup() {
    createCanvas(displayWidth, displayHeight);
    textAlign(CENTER);
    whiteTags = false;
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
        displayCentre = createVector(displayWidth / 2, displayHeight / 2);
    } else {
        displayCentre = createVector(windowWidth / 2, windowHeight / 2);
    }
    return displayCentre
}

function drawResponse(colour_matches) {
    background(128);
    console.log(colour_matches);
    displayCentre = findCentre();
    for (c of colour_matches) {
        var pos = createVector(c.a, c.b);
        pos.x = -pos.x; 
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
