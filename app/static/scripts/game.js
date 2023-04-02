const image_top = document.getElementById('image-top');
const image_bottom = document.getElementById('image-bottom');
const podium = document.getElementById('podium')
const podFirst = document.getElementById('podium-text1')
const podSec = document.getElementById('podium-text2')
const podThird = document.getElementById('podium-text3')

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

function sendQuestionAnswer(score) {
    socket.emit('answered-question', { username: username, room: roomId, score:score})
}

$(document).ready(function() {
    var socket = io.connect("http://127.0.0.1:5000/");
    //var roomId = document.getElementById("room-id").getAttribute('data-value')
    var username = document.cookie.split('=')[1];

    socket.on('connect', function() {
        socket.emit('join', { username: username});});

    socket.on('set-roomId', function(data) {
        console.log(data)
        window.roomId = data
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

        question = data['questions'][0]
        if (question[1] == 0) {
            console.log("higher")
        } else {
            console.log("not higher")
        }
        if (question[2] == 0){
            image_top.addEventListener('click', function () {
                socket.emit('answered-question', { username: username, room: window.roomId, score:100})
                loading_screen.classList.remove('hidden');
                top_half.classList.add('hidden');
                bottom_half.classList.add('hidden');
                loading_screen.focus();
                top_half.focus();
                bottom_half.focus();
            });
            image_bottom.addEventListener('click', function() {
                socket.emit('answered-question', { username: username, room: window.roomId, score:0})
                loading_screen.classList.remove('hidden');
                top_half.classList.add('hidden');
                bottom_half.classList.add('hidden');
                loading_screen.focus();
                top_half.focus();
                bottom_half.focus();
            });
        } else {
            image_top.addEventListener('click', function () {
                socket.emit('answered-question', { username: username, room: window.roomId, score:0})
                loading_screen.classList.remove('hidden');
                top_half.classList.add('hidden');
                bottom_half.classList.add('hidden');
                loading_screen.focus();
                top_half.focus();
                bottom_half.focus();
            });
            image_bottom.addEventListener('click', function() {
                socket.emit('answered-question', { username: username, room: window.roomId, score:100})
                loading_screen.classList.remove('hidden');
                top_half.classList.add('hidden');
                bottom_half.classList.add('hidden');
                loading_screen.focus();
                top_half.focus();
                bottom_half.focus();
            });
        }



    });

    socket.on('leaderboard', function(data) {
        podium.classList.remove('hidden')
        loading_screen.classList.add('hidden')
        podium.focus()
        loading_screen.focus()
        podFirst.innerHTML = "1. "+data[0]
        podSec.innerHTML = "2. "+data[1]
        podThird.innerHTML = "3. "+data[2]
        setTimeout(function(){
            window.location.href = '/'
            //socket.emit('next-question')
        }, 5000)
    })

});