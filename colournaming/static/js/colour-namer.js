$(function () {
    function hexToRGB (hexcode) {
        return [
            parseInt(hexcode.substring(0, 2), 16),
            parseInt(hexcode.substring(2, 4), 16),
            parseInt(hexcode.substring(4, 6), 16)
        ];
    }

    function doQuery (hexcode, responseHandler) {
        hexcode = hexcode.substring(1);

        var rgb = hexToRGB(hexcode);
        var hexString = 'Hex: ' + hexcode.toUpperCase();
        var rgbString = 'RGB: ' + rgb.join(', ');

        $('#stats-box-rgb-display').text(rgb.join(' '));
        $('#stats-box-header').css('background-color', hexcode);

        $.getJSON(COLOUR_NAMER_URL + '?colour=' + hexcode, function (data) {
            var colourName = data.colours.shift().name;
            var $synonyms = data.colours
                .map(function (colour) {
                    return $('<li>').text(colour.name);
                })
                .reduce(function ($ul, $li) {
                    return $ul.append($li);
                }, $('<ul>'));

            $('#stats-box-colour-name-display').text(colourName);
            $('#stats-box-synonyms-display ul').replaceWith($synonyms);
        });
    }

    $.farbtastic('#colour-picker', function (colour) {
        doQuery(colour);
    }).setColor('#FF0000');
})
