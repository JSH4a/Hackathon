$(document).ready(function() {
    var socket = io.connect("http://138.38.198.157:5000/");
    var roomId = document.getElementById("room-id").getAttribute('data-value')

    socket.on('connect', function() {
        socket.emit('join', { username: $('#username').val(), room: roomId });
    })

    $('#sendBtn').on('click', function() {
        socket.emit('message',{message:$('#username').val() + ': ' + $('#message').val(), room:roomId});
        console.log($('#username').val() + ': ' + $('#message').val(), roomId)
        $('#message').val('');
    });

    socket.on('message', function(data) {
        $('#messages').prepend($('<p>').text(data));
    });

    $('#homeBtn').on('click', function() {
        console.log('leaving')
        socket.emit('leave', { username: $('#username').val(), room: roomId });
        window.location.href = '/'
    });


    window.addEventListener('beforeunload', function(event) {
        // Emit a leave message to the server
        console.log('leaving')
        socket.emit('leave', { username: $('#username').val(), room: roomId });
        
        // Cancel the event so that the browser doesn't show a confirmation dialog
        event.preventDefault();
        event.returnValue = '';
    });
});