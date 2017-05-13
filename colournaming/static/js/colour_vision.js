function setup() {
  var myCanvas = createCanvas(400, 400);
  myCanvas.parent('visionTestCanvas');
  noStroke();
}

function draw() {
  for (var i=0; i < 20; i++) {
    for (var j=0; j < 20; j++) {
      fill(random(100, 200));
      rect(j * 10, i * 10, 10, 10);
    }
  }
  targetLeft();
  targetRight();
}

function targetLeft() {
  target(2, 9);
}

function targetRight() {
  target(10, 17);
}

function target(xMin, xMax) {
  for (var i=6; i < 13; i++) {
    for (var j=xMin; j < xMax; j++) {
      var r = random(0, 100);
      fill(r, 150, r);
      rect(j * 10, i * 10, 10, 10);
    }
  }
}
