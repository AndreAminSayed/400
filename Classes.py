#Player creation

class Player:
    def __init__(self, color, turnindex, name):
        self.color = color
        self.turnindex = turnindex
        self.name = name
        self.score = 0
        self.bet = 0
        self.big_score = 0
        self.iswinner = False


#Played cards

class PlayedCard:
    def __init__(self, suit, rank, player):
        self.suit = suit
        self.rank = rank
        self.player = player
        self.value = self.getValue()
        self.isHeart = False
        if self.suit == "♥":
            self.isHeart = True
    
    def getValue(self):
        if self.rank == "A":
            return 14
        if self.rank == "K":
            return 13
        if self.rank == "Q":
            return 12
        if self.rank == "J":
            return 11
        else:
            return int(self.rank)