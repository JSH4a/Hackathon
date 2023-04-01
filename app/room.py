
def generateId():
    pass

class Room:
    def __init__(self,id=None, max_size=2):
        self.id = id if id is not None else generateId()
        self.max_size = max_size
        self.players = {}

    def addPlayer(self, playerId, playerName):
        self.players[playerId] = playerName
    
    def removePlayer(self, playerId):
        self.players.pop(playerId)

    def getId(self):
        return self.id
    
    def getMaxSize(self):
        return self.max_size
    
    def getPlayers(self):
        return self.players