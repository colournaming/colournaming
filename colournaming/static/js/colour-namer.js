$(function () {
    var $languageSelect = $('select#language');
    var $nameSelect = $('select#name');
    var $statsBoxRGBDisplay = $('#stats-box-rgb-display');
    var $statsBoxHeader = $('#stats-box-header');
    var $statsBoxColourNameDisplay = $('#stats-box-colour-name-display');
    var $statsBoxSynonymsDisplayList = $('#stats-box-synonyms-display ul');

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

        $statsBoxRGBDisplay.text(rgb.join(' '));
        $statsBoxHeader.css('background-color', hexcode);

        $.get(COLOUR_NAMER_URL + '?colour=' + hexcodeValues, function (data) {
            var colourName = data.colours.shift().name;
            var $synonyms = data.colours
                .map(function (colour) {
                    return $('<li>').text(colour.name);
                })
                .reduce(function ($ul, $li) {
                    return $ul.append($li);
                }, $('<ul>'));

            $statsBoxColourNameDisplay.text(colourName);
            $statsBoxSynonymsDisplayList.replaceWith($synonyms);
        });
    }

    function resetSelectName (hexCode) {
        if (hexCode === undefined || hexCode.slice(1) !== $nameSelect.val()) {
            $nameSelect
                .blur()
                .val('-')
                .children(':first-child')
                .attr('selected', 'selected');
        }
    }

    function updateNames () {
        $.get(COLOUR_NAMER_COLOURS_URL + '?lang=' + $languageSelect.val(), function (data) {
            $nameSelect.children(':not(:first-child)').remove();

            resetSelectName();

            $.each(data, function (_, colour) {
                $nameSelect.append($('<option/>')
                    .attr('value', colour.hex)
                    .text(colour.name));
            });
        });
    }

    function updateLanguages () {
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

    $.farbtastic('#colour-picker', function (hexCode) {
        resetSelectName(hexCode);
        doQuery(hexCode);
    }).setColor('#FF0000');

    $languageSelect.change(onLanguageSelectChange);
    $nameSelect.change(onColourSelectChange);

    updateLanguages();
    updateNames();
})
