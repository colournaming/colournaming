var target = {r: 0, g: 0, b: 0};

function setup() {
  var myCanvas = createCanvas(400, 400);
  myCanvas.parent("colourNameCanvas");
  nextTarget();
  noStroke();
}

function draw() {
  fill(target.r, target.g, target.b);
  rect(10, 10, 100, 100);
}

function recordAnswerShowNext(e) {
  var response = {
    csrf_token: $('#csrf_token')[0].value,
    name: $('#name')[0].value,
    target_id: target.id
  };
  $.post(
    COLOUR_NAME_RESPONSE_URL,
    response,
    function(data) {
      nextTarget();
      $('#name')[0].value = '';
    }
  );
  e.preventDefault()
}

function nextTarget() {
  $.get(
    COLOUR_NAME_TARGET_URL,
    success=function(data) {
      target = data;
    }
  )
}