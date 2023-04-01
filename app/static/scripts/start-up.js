// get elements
input_username = document.getElementById("input-username");

const GAMEMODES = ["Classic", "Elimniation", "Stanley"] 

let game_index = 0; 


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

    }
});

// add button event
document.querySelector('#gamemode').addEventListener('click', (e) => {
    game_index = game_index + 1 > GAMEMODES.length - 1 ? 0 : game_index + 1;
    e.target.innerHTML = GAMEMODES[game_index];
});