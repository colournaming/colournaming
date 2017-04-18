$(function () {
    console.log("setting up namer interface");
    $('#goButton').on('click', doQuery);
    var farb = $.farbtastic('#colourpicker', function(e) { doQuery(e, drawResponse) }); 
    var $farbdiv = $('.farbtastic')[0];
    $farbdiv.style['margin-left'] = 'auto';
    $farbdiv.style['margin-right'] = 'auto';
    $farbdiv.style['margin-top'] = '100px';
    farb.setColor('#ff0000');
})
