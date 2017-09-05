const $header = document.querySelector('header');

document
    .querySelector('.hamburger')
    .addEventListener('click', () => $header.classList.toggle('revealed'));
