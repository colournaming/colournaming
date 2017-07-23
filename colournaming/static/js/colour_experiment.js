function setup() {
  var myCanvas = createCanvas(400, 400);
  myCanvas.parent("colourNameCanvas");
  noStroke();
}

function draw() {
  fill(255, 0, 0);
  rect(10, 10, 100, 100);
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
