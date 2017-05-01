$(function () {
    $('#goButton').on('click', doQuery);
    $('#colourpicker').farbtastic(function(e) { doQuery(e, updateWithResponse) }); 
    var $farb = $('.farbtastic')[0];
    $farb.style['margin-left'] = 'auto';
    $farb.style['margin-right'] = 'auto';
})
