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
    rooms[room_code].addPlayer(username)
    print('join_room_announcement', username + ' has joined the room.', room_code)
    join_room(room_code)
    emit('join_room_announcement', username + ' has joined the room.', room=room_code)
    emit('set-roomId', room_code)
    # check room is full
    if len(rooms[room_code].getPlayers()) == 3:#rooms[room_code].getMaxSize():
    # then start game
        print("room full")
        # hide waiting
        questions = [[((0,"name", 10),(1,"name2", 100)), 0, 0]]#getQuestions
        data = {}
        data['questions'] = questions
        emit('show-game', data, room=room_code)
        # get game info
            # get game products / companies
            # get image
        # un hide game halves

    # else return waiting
    
@socketio.on('answered-question')
def on_answer(data):
    username = data['username']
    roomId = int(data['room'])
    score = data['score']
    rooms[roomId].addScore(username, score)
    rooms[roomId].answers += 1
    if rooms[roomId].answers == len(rooms[roomId].getPlayers()):
        top3 = [str(key)+":"+str(value) for key, value in rooms[roomId].getPlayers().items()]
        top3 = sorted(top3, key=lambda x: x.split(':')[1], reverse=True)[:3]
        print(len(top3))
        emit('leaderboard', top3, room=roomId)
    
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print("removing ",username, " from room ",room)
    removePlayerFromRoom(room, username)
    leave_room(room)
