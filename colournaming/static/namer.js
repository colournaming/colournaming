console.log(url)

function setup() {
    loadJSON(url, drawResponse);
}

function draw() {
}

function drawResponse(colour_matches) {
    c = colour_matches[0];
    fill(c.red, c.green, c.blue);
    ellipse(50, 50, 80, 80);
}
