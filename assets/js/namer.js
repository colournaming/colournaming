import jquery from 'jquery';
window.jQuery = jquery;
window.$ = jquery;
require('./farbtastic')
import { initAudio, playSound, loadAudioSet, resumeAudio } from './audio'

function hexToRGB (hexcode) {
  return [
    parseInt(hexcode.substring(0, 2), 16),
    parseInt(hexcode.substring(2, 4), 16),
    parseInt(hexcode.substring(4, 6), 16)
  ];
}

function rgbToHex(r, g, b) {return '#' + r.toString(16) + g.toString(16) + b.toString(16)};

function doQuery (hexcode, responseHandler) {
  const $languageSelect = $('select#language');
  const $statsBoxRGBDisplay = $('#stats-box-rgb-display');
  const $statsBoxHeader = $('#stats-box-header');
  const $statsBoxColourNameDisplay = $('#stats-box-colour-name-display');
  const $statsBoxSynonymsDisplayList = $('#stats-box-synonyms-display ul');

  var hexcodeValues = hexcode.substring(1);
  var rgb = hexToRGB(hexcodeValues);
  var hexString = 'Hex: ' + hexcodeValues.toUpperCase();
  var rgbString = 'RGB: ' + rgb.join(', ');

  $statsBoxRGBDisplay.text(rgb.join(' '));
  $statsBoxHeader.css('background-color', hexcode);

  $.get(COLOUR_NAMER_URL + $languageSelect.val() + '/name?colour=' + hexcodeValues, function (data) {
    var topMatch = data.colours.shift()
    var colourName = topMatch.name.replace('_', ' ');
    var topHex = rgbToHex(topMatch.red, topMatch.green, topMatch.blue);
    playSound(topHex);
    var $synonyms = $('<ul/>');
    $.each(data.colours, function(i, colour) {
      var $li = $('<li/>')
        .text(colour.name.replace('_', ' '))
      $synonyms.append($li);
    });
    $statsBoxColourNameDisplay.text(colourName);
    $statsBoxSynonymsDisplayList.replaceWith($synonyms);
    resetAgreement(); 
  });
}

function resetSelectName (hexCode) {
  const $nameSelect = $('select#name'); 
  if (hexCode === undefined || hexCode.slice(1) !== $nameSelect.val()) {
    $nameSelect
      .blur()
      .val('-')
      .children(':first-child')
      .attr('selected', 'selected');
  }
}

function resetAgreement () {
  const $agreementSelect = $('select#agreement :first-child')[0]; 
  $agreementSelect.selected = true;
}

function updateNames () {
  const $nameSelect = $('select#name'); 
  const $languageSelect = $('select#language');
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
  const $languageSelect = $('select#language');
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
  const $languageSelect = $('select#language');
  updateNames();
  loadAudioSet($languageSelect.val());
}

function onColourSelectChange (event) {
  $.farbtastic('#colour-picker').setColor('#' + event.target.value);
}

function onInterfaceLanguageSelectChange (event) {
  const $interfaceLanguageSelect = $('select#interface-language');
  var url = INTERFACE_LANGUAGE_SELECT_URL + '?lang=' + $interfaceLanguageSelect.val();
  console.log(url);
  window.location.replace(url);
}

function onAgreementSelectChange (event) {
  var agreement_level = $('#name_agreement_form #agreement')[0].value;
  if (agreement_level == "") {
    return;
  }
  var rgb_selected = hexToRGB($.farbtastic('#colour-picker').color.substring(1));
  console.log(rgb_selected);
  $.post(COLOUR_NAMER_AGREEMENT_URL, {
    csrf_token: $('#name_agreement_form #csrf_token')[0].value,
    language_code: $('select#language')[0].value,
    agreement: $('#name_agreement_form #agreement')[0].value,
    red: rgb_selected[0],
    green: rgb_selected[1],
    blue: rgb_selected[2],
  }).done(function() {
    resetAgreement();
  });
}

$(function () {
  var $interfaceLanguageSelect = $('select#interface-language');
  var $languageSelect = $('select#language');
  var $nameSelect = $('select#name');
  var $agreementSelect = $('select#agreement');
  var $statsBoxRGBDisplay = $('#stats-box-rgb-display');
  var $statsBoxHeader = $('#stats-box-header');
  var $statsBoxColourNameDisplay = $('#stats-box-colour-name-display');


  $.farbtastic('#colour-picker', function (hexCode) {
    resetSelectName(hexCode);
    doQuery(hexCode);
  }).setColor('#FF0000');

  $(document).on('touchstart', resumeAudio);
  $languageSelect.change(onLanguageSelectChange);
  $nameSelect.change(onColourSelectChange);
  $agreementSelect.change(onAgreementSelectChange);
  $interfaceLanguageSelect.change(onInterfaceLanguageSelectChange);

  $('#hamburger').on('click', function () {
    $('header').toggleClass('revealed');
  });

  updateNames();
  initAudio();
})
