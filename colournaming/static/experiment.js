/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 4);
/******/ })
/************************************************************************/
/******/ ({

/***/ 4:
/***/ (function(module, exports) {

let results = JSON.parse(localStorage.getItem('results'));

const updateResults = (delta) => {
    results = Object.assign({ }, results, delta);

    localStorage.setItem('results', JSON.stringify(results));
};
const $levels = document.getElementById('levels');

const submitForm = (data, location) => {
    const formData = new FormData();

    formData.append('csrf_token', document.getElementById('csrf_token').value);

    Object
        .keys(data)
        .forEach((key) => {
            formData.append(key, data[key]);
        });

    fetch(window.location, {
        body: formData,
        credentials: 'same-origin',
        method: 'POST'
    })
        .then(() => {
            if (typeof location === 'string') {
                window.location = location;
            }
        });
};

if ($levels !== null) {
    updateResults({ greyscaleRampSteps: undefined });

    $levels.addEventListener('change', () => {
        const value = $levels.value;

        if (value !== '-') {
            updateResults({ greyscaleRampSteps: parseInt(value, 10) });

            submitForm({
                levels: value,
                screen_colour_depth: screen.colorDepth,
                screen_height: screen.height,
                screen_width: screen.width
            }, 'name_colour.html');
        } else {
            updateResults({ greyscaleRampSteps: undefined });
        }
    });
}

const $colourCircle = document.getElementById('colour-circle');
const $colourId = document.getElementById('colour-id');
const $colourName = document.getElementById('colour-name');
const $colourNameForm = document.getElementById('colour-name-form');
const $colourNumber = document.getElementById('colour-number');
const $colourVisionTestPage = document.getElementById('colour-vision-test-page');
const $nextColour = document.getElementById('next-colour');
const $responseTime = document.getElementById('response-time');
const $startTime = document.getElementById('start-time');

if ($colourCircle !== null && $colourId !== null && $colourName !== null && $colourNameForm !== null && $colourNumber !== null && $colourVisionTestPage !== null && $nextColour !== null && $responseTime !== null && $startTime !== null) {
    updateResults({ colours: undefined });

    const updateColourCircle = () => {
        fetch(COLOUR_NAME_TARGET_URL)
            .then((response) => response.json())
            .then(({ b, g, id, r }) => {
                $colourCircle.style.backgroundColor = `rgb(${ r }, ${ g }, ${ b })`;
                $colourId.value = id;
                $startTime.value = performance.now();
            });
    };

    const updateColourResults = () => {
        const colour = {
            name: $colourName.value,
            value: $colourCircle.style.backgroundColor
        };
        const colours = (results.colours) ? [ ...results.colours, colour ] : [ colour ];

        updateResults({ colours });
    };

    updateColourCircle();

    $colourName.addEventListener('input', () => {
        if ($responseTime.value === '') {
            $responseTime.value = performance.now() - parseFloat($startTime.value);
        }
    });

    $colourNameForm.addEventListener('submit', (event) => {
        event.preventDefault();

        updateColourResults();
        submitForm({
            name: $colourName.value,
            response_time: parseFloat($responseTime.value),
            target_id: $colourId.value
        });
        updateColourCircle();

        $colourName.value = '';
        $colourNumber.textContent = `#${ (results.colours) ? results.colours.length + 1 : 0 }`;
        $responseTime.value = '';
        $colourName.focus();
    });

    $colourVisionTestPage.addEventListener('click', (event) => {
        event.preventDefault();

        if ($colourName.value !== '') {
            updateColourResults();
            submitForm({
                name: $colourName.value,
                response_time: performance.now() - parseFloat($startTime.value),
                target_id: $colourId.value
            }, 'colour_vision.html');
        } else {
            window.location = 'colour_vision.html';
        }
    });

    let dimesions = { height: window.innerHeight, width: window.innerWidth };

    window.addEventListener('resize', () => {
        const height = window.innerHeight;
        const scrollTop = document.scrollingElement.scrollTop;
        const width = window.innerWidth;

        if ($colourName === document.activeElement
                && height < dimesions.height
                && width === dimesions.width) {
            const { height: inputHeight, top } = $colourName.getBoundingClientRect();
            const desiredScrollTop = top + scrollTop - height + inputHeight + 10;

            document.scrollingElement.scrollTop = desiredScrollTop;

            let frames = 0;

            // Check the scroll position for the next couple of frames to ensure it will not be revoked by the browser.
            const forceScrollTop = () => {
                if (document.scrollingElement.scrollTop !== desiredScrollTop) {
                    document.scrollingElement.scrollTop = desiredScrollTop;
                }

                frames += 1;

                // Let's hope that 20 frames are enough to stabilize the scroll position.
                if (frames < 20) {
                    requestAnimationFrame(forceScrollTop);
                }
            };

            requestAnimationFrame(forceScrollTop);
        }

        dimesions = { height, width };
    });
}

const $appearance = document.getElementById('appearance');

if ($appearance !== null) {
    updateResults({ appearance: undefined });

    $appearance.addEventListener('change', () => {
        const value = $appearance.value;

        if (value !== '-') {
            updateResults({ appearance: value });

            submitForm({
                square_disappeared: value
            }, 'observer_information.html');
        } else {
            updateResults({ appearance: undefined });
        }
    });
}

const $age = document.getElementById('age');
const $gender = document.getElementById('gender');
const $experience = document.getElementById('colour_experience');
const $languageSkills = document.getElementById('language_experience');
const $educationalLevel = document.getElementById('education_level');
const $homeCountry = document.getElementById('country_raised');
const $residentCountry = document.getElementById('country_resident');
const $lightConditions = document.getElementById('ambient_light');
const $environment = document.getElementById('screen_light');
const $distance = document.getElementById('screen_distance');
const $thankYouPage = document.getElementById('thank-you-page');

if ($age !== null && $distance !== null && $educationalLevel !== null && $environment !== null && $experience !== null && $gender !== null && $homeCountry !== null && $languageSkills !== null && $lightConditions !== null && $residentCountry !== null && $thankYouPage !== null) {
    updateResults({ age: -1, distance: -1, educationalLevel: '', environment: '', experience: '', gender: '', homeCountry: '', languageSkills: '', lightConditions: '', residentCountry: '' });

    $age.addEventListener('change', () => {
        const value = $age.value;

        if (value !== '-') {
            updateResults({ age: parseInt(value, 10) });
        } else {
            updateResults({ age: undefined });
        }
    });

    $distance.addEventListener('change', () => {
        const value = $distance.value;

        if (value !== '-') {
            updateResults({ distance: value });
        } else {
            updateResults({ distance: undefined });
        }
    });

    $educationalLevel.addEventListener('change', () => {
        const value = $educationalLevel.value;

        if (value !== '-') {
            updateResults({ educationalLevel: value });
        } else {
            updateResults({ educationalLevel: undefined });
        }
    });

    $environment.addEventListener('change', () => {
        const value = $environment.value;

        if (value !== '-') {
            updateResults({ environment: value });
        } else {
            updateResults({ environment: undefined });
        }
    });

    $experience.addEventListener('change', () => {
        const value = $experience.value;

        if (value !== '-') {
            updateResults({ experience: value });
        } else {
            updateResults({ experience: undefined });
        }
    });

    $gender.addEventListener('change', () => {
        const value = $gender.value;

        if (value !== '-') {
            updateResults({ gender: value });
        } else {
            updateResults({ gender: undefined });
        }
    });

    $homeCountry.addEventListener('change', () => {
        const value = $homeCountry.value;

        if (value !== '-') {
            updateResults({ homeCountry: value });
        } else {
            updateResults({ homeCountry: undefined });
        }
    });

    $languageSkills.addEventListener('change', () => {
        const value = $languageSkills.value;

        if (value !== '-') {
            updateResults({ languageSkills: value });
        } else {
            updateResults({ languageSkills: undefined });
        }
    });

    $lightConditions.addEventListener('change', () => {
        const value = $lightConditions.value;

        if (value !== '-') {
            updateResults({ lightConditions: value });
        } else {
            updateResults({ lightConditions: undefined });
        }
    });

    $residentCountry.addEventListener('change', () => {
        const value = $residentCountry.value;

        if (value !== '-') {
            updateResults({ residentCountry: value });
        } else {
            updateResults({ residentCountry: undefined });
        }
    });

    $thankYouPage.addEventListener('click', (event) => {
        event.preventDefault();

        submitForm({
            age: results.age,
            ambient_light: results.lightConditions,
            colour_experience: results.experience,
            country_raised: results.homeCountry,
            country_resident: results.residentCountry,
            education_level: results.educationalLevel,
            gender: results.gender,
            language_experience: results.languageSkills,
            screen_distance: results.distance,
            screen_light: results.environment
        }, $thankYouPage.href);
    });

}

const $thankYouText = document.getElementById('thank-you-text');
const $results = document.getElementById('results');

if ($thankYouText !== null && $results !== null) {
    const { colours } = results;

    if (colours) {
        fetch(`/experiment/response_percentage?count=${ colours.length }`)
            .then((response) => response.json())
            .then((json) => {
                const roundedTopPercentage = Math.round(json.top_percentage);

                $thankYouText.textContent = `Thank you for participating. You are in the ${ roundedTopPercentage }% top colournamers. Feel free to share it with your friends.`;
            });

        Promise
            .all(Object
                .keys(colours)
                .map((key) => {
                    const { name, value } = colours[key];

                    const $div = document.createElement('div');
                    const $li = document.createElement('li');
                    const $whiteSpan = document.createElement('span');
                    const $blackSpan = document.createElement('span');

                    $div.style.backgroundColor = value;

                    $whiteSpan.className = 'white';
                    $whiteSpan.textContent = name;

                    const hexColorValue = value
                        .match(/rgb\(([0-9]+),\s([0-9]+),\s([0-9]+)\)/)
                        .slice(1)
                        .map((string) => parseInt(string, 10))
                        .map((number) => number.toString(16))
                        .join('');

                    $li.appendChild($div);
                    $li.appendChild($whiteSpan);
                    $li.appendChild($blackSpan);

                    $results.appendChild($li);

                    return fetch(`/namer/lang/en/name?colour=${ hexColorValue }`)
                        .then((response) => response.json())
                        .then((json) => {
                            $blackSpan.className = 'black';
                            $blackSpan.textContent = json.colours[0].name.replace('_', ' ');
                        });
                }));
    }
}


/***/ })

/******/ });