$(function () {
    console.log("setting up namer interface");
    $('#goButton').on('click', doQuery);
    $('#colourpicker').farbtastic(function(e) { doQuery(e) }); 
    var $farb = $('.farbtastic')[0];
    $farb.style['margin-left'] = 'auto';
    $farb.style['margin-right'] = 'auto';
})
