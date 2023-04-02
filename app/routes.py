from flask import Blueprint, render_template, request, make_response
from .room import Room
from flask_socketio import emit

main = Blueprint('main', __name__)
rooms = []

#room_code = 'AAAA'
#rooms.append(Room(id=room_code))

def getRoomCode():
    displayRooms()
    for room in rooms:
        if len(room.getPlayers()) < room.getMaxSize():
            return room.getId()
    newId = len(rooms)
    rooms.append(Room(id=newId, max_size=4))
    return  newId

def removePlayerFromRoom(roomId, playerName):
    for room in rooms:
        if room.getId() == int(roomId):
            room.removePlayer(playerName)
            return
    print("player not in room")    
    
def displayRooms():
    for r in rooms:
        print(r.getId())
    for r in rooms:
        print(r.getPlayers())

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/talk')
def talk():
    username = request.cookies.get('username')
    response = make_response(render_template('talk.html', username=username))
    #response.headers.add('Room-Code', room_code)
    return response

@main.route('/game')
def game():
    username = request.cookies.get('username')

    response = make_response(render_template('game.html', username=username))
    return response

@main.route('/test')
def test():
    return render_template('test.html')
