const image_top = document.getElementById('image-top');
const image_bottom = document.getElementById('image-bottom');

// add image click event to top image
document.querySelector('#image-top').addEventListener('click', (e) => {
    image_top.classList.add('selected');
        setTimeout(() => {
            image_top.classList.remove('selected');
            image_top.focus();
        }, 1000);
});

// add image click event to bottom image
document.querySelector('#image-bottom').addEventListener('click', (e) => {
    image_bottom.classList.add('selected');
        setTimeout(() => {
            image_bottom.classList.remove('selected');
            image_bottom.focus();
        }, 1000);
});