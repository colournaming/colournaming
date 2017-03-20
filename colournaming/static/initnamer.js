$(function () {
    console.log("setting up namer interface");
    $('#goButton').on('click', doQuery);
    $('#colourpicker').farbtastic(function(e) { doQuery(e) }); 
})