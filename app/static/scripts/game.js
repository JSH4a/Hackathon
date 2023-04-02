const image_top = document.getElementById('image-top');
const image_bottom = document.getElementById('image-bottom');

const loading_screen = document.getElementById('loading-screen');
const top_half = document.getElementById('top');
const bottom_half = document.getElementById('bottom');

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

// socket stuff

$(document).ready(function() {
    var socket = io.connect("http://127.0.0.1:5000/");
    var roomId = document.getElementById("room-id").getAttribute('data-value')
    var username = document.cookie.split('=')[1];

    socket.on('connect', function() {
        socket.emit('join', { username: username});});

    socket.on('set-roomId', function(data) {
        var roomId = data
    })

    window.addEventListener('beforeunload', function(event) {
        // Emit a leave message to the server
        console.log('leaving')
        socket.emit('leave', { username: username, room: roomId });
        
        // Cancel the event so that the browser doesn't show a confirmation dialog
        event.preventDefault();
        event.returnValue = '';
    });

    socket.on('show-game', function(data) {
        loading_screen.classList.add('hidden');
        top_half.classList.remove('hidden');
        bottom_half.classList.remove('hidden');
        loading_screen.focus();
        top_half.focus();
        bottom_half.focus();
        alert("Room full - starting game")
    });
});