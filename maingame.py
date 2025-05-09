import numpy as np
import random as rand
from Classes import Player, PlayedCard
# import Classes 

#values (dictionary)
def create_deck():
    suits = {"Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣",
            "Spades": "♠"
    }


    ranks = {"2": 2,
            "3": 3,                          
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
    }

    deck = []

    for suit_name, suit_symbol in suits.items():
        for rank, value in ranks.items():
            card = {
                    
                    "symbol": suit_symbol,
                    "rank": rank,
            }
            deck.append(card)
    return deck

# for card in deck[:]:
#     print(f"{card['symbol']}{card['rank']}") #prints all cards with suit and rank

#Player creation


p1 = Player("blue", True, "Player 1")
p2 = Player("red", False, "Player 2") 
p3 = Player("green", False, "Player 3")
p4 = Player("yellow", False, "Player 4")


# print(p2.color)
# print(p2.turnindex)

#choose a random card from the deck
def dealcard(deck):
    index = rand.randrange(len(deck))
    randcard = deck[index]
    #print(randcard)

    #delete that card from the deck
    del deck[index]
    return randcard

# card = dealcard(deck)
# print(f"{card['symbol']}{card['rank']}")

# for card in deck[:]:
#     print(f"{card['symbol']}{card['rank']}") #prints all cards with suit and rank


deck = create_deck()

#create hands at the start  of the round with randomly selected cards from deck
def shuffle(deck):
    hands = [[], [], [], []]


    for x in range(52): #this right here gives everyone a full deck
        c = dealcard(deck)
        hands[0].append(c)
        hands[1].append(c)
        hands[2].append(c)
        hands[3].append(c)
        #hands[x%4].append(dealcard(deck)) #this is the right one
    return hands
    # for card in hands [0]:
    #     print(f"{card['symbol']}{card['rank']}")
hands = shuffle(deck)


#sort hands based on suits order above and then based on rank
suit_order = {'♥':0, '♦':1, '♣':2, '♠':3}
rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def sort_hands(hands):
    for i in range(4):
        hands[i] = sorted(hands[i], key = lambda card: (suit_order[card['symbol']], -rank_order[card['rank']]))
    
    
# for i, hand in enumerate(hands):
#     print(f"Player {i + 1}'s hand:")
#     for card in hand:
#         print(f"{card['symbol']}{card['rank']}")
#     print()  # empty line between player


#rotate a list (for determining starting player of the round)
playerorder = [p1, p2, p3, p4] #standard player order
def rotate_list(playerorder):
    start_index = next((i for i, player in enumerate(playerorder) if player.turnindex == True), 0)
    rotated = playerorder[start_index:] + playerorder[:start_index]
    # for i in range(4):
    #     print(f"new list: {rotated[i].name}")
    return rotated


gameisactive = None
print('Would you like to start a new Game? (y/n) ')
startinput = input()
if (startinput == 'y'):
    gameisactive = True
while (gameisactive == True):
    
    # print("this should not print")
    roundisactive = True
    while (roundisactive):
        
        deck = create_deck()
        hands = shuffle(deck)
        sort_hands(hands)
        print("Hands have been dealt")
        #set bets

        for x in range(4):
            while True:
                try:
                    print(f"How many points do you wager this round, {playerorder[x].name}? ")
                    wager = int(input())
                    if wager < 2 or wager > 13:
                        print("Invalid bet! Please enter a number between 2 and 13.")
                        continue  # Ask again
                    break  # Valid input, exit the loop
                except ValueError:
                    print("Invalid input! Please enter a whole number between 2 and 13.")

            if wager >= 5:
                wager *= 2

            playerorder[x].bet = wager
            print(f"Player {x + 1} wagers {wager} points this round.")

        #check if total of 12 points is achieved to start the round
        sum = 0
        for i in range(4):
            sum += playerorder[i].bet
        if (sum < 12):
            print(f"Too few points wagered. There needs to be at least 12 points wagered, but only {sum} were wagered")
            continue
       
        table = []
        while len(hands[3]) > 49: #should be while len() != 0
            #round starts
            for d in range(4):
                while True:
                    try: 
                        print(f"Player {playerorder[d].name} Choose your card to play")
                        playedcard = input().strip()

                        assert (playedcard != "break")

                        symbol = playedcard[0]
                        rank = playedcard[1:]

                        card_to_play = None
                        for card in hands[d]:
                            if card['symbol'] == symbol and card['rank'] == rank:
                                card_to_play = card
                                break

                        if card_to_play:
                            hands[d].remove(card_to_play)
                            table.append(PlayedCard(symbol, rank, playerorder[d]))
                            if d == 0:
                                first_suit = symbol
                            print(f"{playerorder[d].name} played {symbol}{rank}")
                            break

                        else:
                            print(f"This card is not in your hand.")

                    except ValueError:
                        print(f"Invalid input. Choose another card")

            # for card in table:
            #     print(f"{card['symbol']}{card['rank']}")
                
            #determine winner
            heartcards = [card for card in table if card.isHeart]

            #check for hearts
            for card in table:
            #     print(card.rank)
            #     print(card.suit)
            #     print(card.player.name)
            #     print(card.value)

                #if len(heartcards) == 1:
                #round_winner = heartcards[0].player
                    
                p1.turnindex = False #just because player 1 starts with turnindex True so that someone can start the game
                # round_winner.turnindex = False #set turnindex to False from previous round_winner to ensure only the new winner has turnindex == True
                p2.turnindex = False
                p3.turnindex = False
                p4.turnindex = False

                if len(heartcards) >= 1:
                    final_list = heartcards

                else:
                    final_list = [card for card in table if card.suit == first_suit]

                biggest = 0
                for niki in final_list:
                    if niki.value > biggest:
                        biggest = niki.value
                        round_winner = niki.player

            round_winner.score += 1
            round_winner.turnindex = True
            print(f"{round_winner.name} wins this round! {round_winner.name}'s score is now {round_winner.score} ")
            playerorder = rotate_list(playerorder)
            
            
            # for i in range(4):
            #     print(f"{playerorder[i].name} with {playerorder[i].turnindex}")

        #set ended, check if players achieved their bet 
        for x in range(4):
            if(playerorder[x].score >= 5):
                playerorder[x].score *= 2
            if playerorder[x].bet > playerorder[x].score:
                playerorder[x].big_score -= playerorder[x].bet
                print(f"{playerorder[x].name} wagered {playerorder[x].bet} but only got {playerorder[x].score}. {playerorder[x].name} loses {playerorder[x].bet} points! Better luck next time!")
            else: 
                playerorder[x].big_score += playerorder[x].bet
                print(f"{playerorder[x].name} wagered {playerorder[x].bet} and got {playerorder[x].score}. {playerorder[x].name} gets {playerorder[x].bet} points! Good job! ")

        #check if someone won the entire game

        
        winner_list = []
        goat = None
        for i in range(4):
            if playerorder[i].big_score >= 2:
                winner_list.append(playerorder[i])
        
        if len(winner_list) > 0:
            if len(winner_list) == 1:
                winner_list[0].iswinner = True
                goat = winner_list[0]
            
            else:
                big_score_tracker = 0
                for x in range(len(winner_list)-1):
                    if winner_list[x].big_score > big_score_tracker:
                        big_score_tracker = winner_list[x].big_score
                        goat = winner_list[x]

        print(f"{goat.name} wins the game! Congratulations")
        for i in range(4):
            print(f"Scoresheet: {playerorder[i].name}: {playerorder[i].big_score}")
        

        #include some function that sorts the scoresheet in decreasing order
        #print scoresheet after every round where big_points get awarded
        #actually end the game when someone wins and give option to restart a new game

        

        # print(hands[0])



        