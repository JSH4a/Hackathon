from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import redirect
from . import socketio
from .routes import removePlayerFromRoom, getRoomCode, rooms

@socketio.on('message')
def handle_message(data):
    message = data['message']
    room = data['room']
    print(message, room)
    emit('message', message, room=room)


@socketio.on('start_game')
def start_game(data):
    username = data['username']
    gamemode = data['gamemode']
    ret_value = {'redirect':'/game',
                'cookie': username}
    return ret_value

@socketio.on('join')
def on_join(data):
    username = data['username']
    room_code = getRoomCode()
    rooms[room_code].addPlayer(username, username)
    print('join_room_announcement', username + ' has joined the room.', room_code)
    join_room(room_code)
    emit('join_room_announcement', username + ' has joined the room.', room=room_code)
    emit('set-roomId', room_code)
    # check room is full
    if len(rooms[room_code].getPlayers()) == 2:#rooms[room_code].getMaxSize():
    # then start game
        print("room full")
        # hide waiting
        emit('show-game', 'true', room=room_code)
        # get game info
            # get game products / companies
            # get image
        # un hide game halves

    # else return waiting
   
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print("removing ",username, " from room ",room)
    removePlayerFromRoom(room, username)
    leave_room(room)
