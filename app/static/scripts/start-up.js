// get elements
input_username = document.getElementById("input-username");

const GAMEMODES = ["Classic", "Elimniation", "Stanley"] 

let game_index = 0; 

var socket = io.connect("http://127.0.0.1:5000/");

socket.on('change_webpage', function (data){
    window.location.href = data
});


// name validation
document.querySelector('#btn-play').addEventListener('click', () => {
    // if name too short show error
    if (input_username.value.length <= 3) {
        input_username.classList.add('input-err');
        setTimeout(() => {
            input_username.classList.remove('input-err');
            input_username.focus();
        }, 500);
    }
    //else start game
    else {
        data = {'username':$('#input-username').val(),
                'gamemode':document.getElementById("gamemode").innerHTML}

        socket.emit('start_game', data, callback=function (data){
            console.log(data)
            document.cookie = "username="+data['cookie']+";max-age=31536000"
            window.location.href = data['redirect']
        });


    }
});

// add button event
document.querySelector('#gamemode').addEventListener('click', (e) => {
    game_index = game_index + 1 > GAMEMODES.length - 1 ? 0 : game_index + 1;
    e.target.innerHTML = GAMEMODES[game_index];
});
