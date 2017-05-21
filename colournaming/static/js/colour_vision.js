var boxSide = 0;
var TEST_COUNT = 2;
var TGT_LEFT = 0;
var TGT_RIGHT = 1;
var testsComplete = 0;
var testsCorrect = 0;

function setup() {
  var myCanvas = createCanvas(400, 400);
  myCanvas.parent("visionTestCanvas");
  noStroke();
  $("#button-left").on("click", answerLeft);
  $("#button-right").on("click", answerRight);
  nextTarget();
}

function draw() {
  for (var i=0; i < 20; i++) {
    for (var j=0; j < 20; j++) {
      fill(random(100, 200));
      rect(j * 10, i * 10, 10, 10);
    }
  }
  drawTarget();
}

function answerLeft(e) {
  checkAnswerShowNext(TGT_LEFT);
  e.preventDefault()
}

function answerRight(e) {
  checkAnswerShowNext(TGT_RIGHT);
  e.preventDefault()
}

function checkAnswerShowNext(side) {
  if (side === boxSide) {
    testsCorrect += 1;
  }
  testsComplete += 1;
  if (testsComplete === TEST_COUNT) {
    var results = {
      csrf_token: $('#csrf_token')[0].value,
      tests_correct: testsCorrect,
      tests_complete: testsComplete
    };
    $.post(
      COLOUR_VISION_SUBMIT_URL, 
      results,
      function(data) {
        console.log(data);
        window.location.replace(data.url);
      }
    );
  }
  nextTarget();
}


function nextTarget() {
  boxSide = random([TGT_LEFT, TGT_RIGHT]);
}

function drawTarget() {
  if (boxSide === TGT_LEFT) {
    targetLeft();
  } else if (boxSide === TGT_RIGHT) {
    targetRight();
  }
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
