from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import redirect
from . import socketio
from .routes import removePlayerFromRoom

@socketio.on('message')
def handle_message(data):
    message = data['message']
    room = data['room']
    print(message, room)
    emit('message', message, room=room)


@socketio.on('start_game')
def start_game(data):
    print(data)
    print(type(data))
    username= data['username']
    gamemode= data['gamemode']
    print("user",username,"joined gamemode",gamemode)
    #emit('change_webpage', '/talk')
    ret_value = {'redirect':'/talk',
                'cookie': username}
    return ret_value

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    print('join_room_announcement', username + ' has joined the room.', room)
    join_room(room)
    emit('join_room_announcement', username + ' has joined the room.', room=room)
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print("removing ",username, " from room ",room)
    removePlayerFromRoom(room, username)
    leave_room(room)
