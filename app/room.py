
def generateId():
    pass

class Room:
    def __init__(self,id=None, max_size=2):
        self.id = id if id is not None else generateId()
        self.max_size = max_size
        self.players = {}
        self.answers = 0

    def addPlayer(self, playerId):
        self.players[playerId] = 0
    
    def removePlayer(self, playerId):
        self.players.pop(playerId)

    def getId(self):
        return self.id
    
    def getMaxSize(self):
        return self.max_size
    
    def getPlayers(self):
        return self.players
    
    def addScore(self, playerId, score):
        self.players[playerId] += score