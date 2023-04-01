from flask import Blueprint, render_template, request, make_response
from .room import Room

main = Blueprint('main', __name__)
rooms = []
#room_code = 'AAAA'
#rooms.append(Room(id=room_code))

def getRoomCode():
    displayRooms()
    for room in rooms:
        print(len(room.getPlayers()))
        if len(room.getPlayers()) < room.getMaxSize():
            return room.getId()
    newId = len(rooms)
    rooms.append(Room(id=newId, max_size=2))
    return  newId

def removePlayerFromRoom(roomId, playerName):
    #displayRooms()
    #rooms[roomId].removePlayer(playerName)
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
    room_code = getRoomCode()
    username = request.cookies.get('username')
    rooms[room_code].addPlayer(username, username)
    response = make_response(render_template('talk.html', username=username, roomId=room_code))
    #response.headers.add('Room-Code', room_code)
    return response
