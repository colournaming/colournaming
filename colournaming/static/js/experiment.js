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
const $distance = document.getElementById('distance');
const $educationalLevel = document.getElementById('educational-level');
const $environment = document.getElementById('environment');
const $experience = document.getElementById('experience');
const $gender = document.getElementById('gender');
const $homeCountry = document.getElementById('home-country');
const $languageSkills = document.getElementById('language-skills');
const $lightConditions = document.getElementById('light-conditions');
const $residentCountry = document.getElementById('resident-country');
const $thankYouPage = document.getElementById('thank-you-page');

if ($age !== null && $distance !== null && $educationalLevel !== null && $environment !== null && $experience !== null && $gender !== null && $homeCountry !== null && $languageSkills !== null && $lightConditions !== null && $residentCountry !== null && $thankYouPage !== null) {
    updateResults({ age: undefined, distance: undefined, educationalLevel: undefined, environment: undefined, experience: undefined, gender: undefined, homeCountry: undefined, languageSkills: undefined, lightConditions: undefined, residentCountry: undefined });

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

const $results = document.getElementById('results');

if ($results !== null) {
    const { colours } = results;

    if (colours) {
        for (const { name, value } of colours) {
            const $div = document.createElement('div');
            const $li = document.createElement('li');
            const $whiteSpan = document.createElement('span');
            const $blackSpan = document.createElement('span');

            $div.style.backgroundColor = value;

            $whiteSpan.className = 'white';
            $whiteSpan.textContent = name;

            $blackSpan.className = 'black';
            $blackSpan.textContent = 'likely name';

            $li.appendChild($div);
            $li.appendChild($whiteSpan);
            $li.appendChild($blackSpan);

            $results.appendChild($li);
        }
    }
}
