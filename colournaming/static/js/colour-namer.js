$(function () {
    function hexToRGB (hexcode) {
        return [
            parseInt(hexcode.substring(0, 2), 16),
            parseInt(hexcode.substring(2, 4), 16),
            parseInt(hexcode.substring(4, 6), 16)
        ];
    }

    function doQuery (hexcode, responseHandler) {
        var hexcodeValues = hexcode.substring(1);
        var rgb = hexToRGB(hexcodeValues);
        var hexString = 'Hex: ' + hexcodeValues.toUpperCase();
        var rgbString = 'RGB: ' + rgb.join(', ');

        $('#stats-box-rgb-display').text(rgb.join(' '));
        $('#stats-box-header').css('background-color', hexcode);

        $.getJSON(COLOUR_NAMER_URL + '?colour=' + hexcodeValues, function (data) {
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

    function updateNames () {
        var $nameSelect = $('select#name');
        var $languageSelect = $('select#language');

        $.get(COLOUR_NAMER_COLOURS_URL + '?lang=' + $languageSelect.val(), function (data) {
            $nameSelect.empty();

            $.each(data, function (_, colour) {
                $nameSelect.append($('<option/>')
                    .attr('value', colour.hex)
                    .text(colour.name));
            });
        });
    }

    function updateLanguages () {
        var $languageSelect = $('select#language');

        $.get(COLOUR_NAMER_LANGUAGES_URL, function (data) {
            $languageSelect.empty();

            $.each(data, function (_, language) {
                $languageSelect.append($('<option/>')
                    .attr('value', language.code)
                    .text(language.name));
            });
        });
    }

    function onLanguageSelectChange () {
        updateNames();
    }

    function onColourSelectChange (event) {
        $.farbtastic('#colour-picker').setColor('#' + event.target.value);
    }

    $.farbtastic('#colour-picker', function (colour) {
        doQuery(colour);
    }).setColor('#FF0000');

    $('select#language').change(onLanguageSelectChange);
    $('select#name').change(onColourSelectChange);

    updateLanguages();
    updateNames();
})
