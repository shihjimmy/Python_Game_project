import random

"""
create a uno deck 
including: 108 cards with four different colors
"""
def create_deck():
    deck=[]
    colors=["red","yellow","green","blue"]
    values=[0,1,2,3,4,5,6,7,8,9,"skip","reverse","draw two cards"]
    for color in colors:
        for value in values:
            card="{} {}".format(color,value)
            deck.append(card)
            if value!=0:
                deck.append(card)
    wild=["wild","draw four cards"]
    for i in range(4):
        deck.append(wild[0])
        deck.append(wild[1])
    #print(deck)
    return deck

"""
shuffle a deck
"""
def shuffle(deck):
    for cardpos in range(0,107):
        randpos=random.randint(0,107)
        deck[cardpos],deck[randpos] = deck[randpos],deck[cardpos]
    #print(deck)
    return deck

"""
draw a deck
"""
def draw_cards(number,uno_deck):
    deck=[]
    for i in range(number):
        deck.append(uno_deck.pop(0))
    return deck

"""
players settings
"""
def players_setting(uno_deck):
    players=[]
    number=int(input("how many players: "))
    while number<2 or number>4:
        print("invalid!")
        number=int(input("how many players: "))
    for i in range(number):
        players.append(draw_cards(5,uno_deck))
    return players,number

"""
print your cards
"""
def print_cards(playerturn,players_deck):
    print()
    print("Player {}".format(playerturn+1))
    print("your card: ")
    print("------------------")
    y=0
    for card in players_deck:
        print("{}) {}".format(y,card))
        y+=1
    print("------------------")
    return

"""
check if the card chosen is able to be placed
"""
def can_play(color,value,card):
    splitcard = card.split(' ',1)    
    if splitcard[0]=="wild" or splitcard[0]=="draw":
        return True
    if color==splitcard[0] or value==splitcard[1]:
        return True
    return False

"""
check if the player can place a card or not
"""
def can_place_cards(discards_piles,players_deck):
    current = discards_piles[-1]
    current_card = current.split(' ',1)
    if current_card[0]=="wild" or current_card[0]=="draw":
        return True
    for card in players_deck:
        splitcard = card.split(' ',1)
        if current_card[0]==splitcard[0] or current_card[1]==splitcard[1]:
            return True
    return False

"""
playing the game
"""
def play_uno():
    running = True
    uno_deck = create_deck()
    uno_deck = shuffle(uno_deck)
    players,num_of_players = players_setting(uno_deck)
    playing_direction = 1
    #1 : clockwise
    #-1 : counter clockwise
    playersturn=0  
    discards_pile=[]
    while running:        
        if len(discards_pile)==0:
            print_cards(playersturn,players[playersturn])
            print("put first card on the table!")
            choice=int(input("which card do you want to discard: "))
            while choice<0 or choice>=len(players[playersturn]):
                print("invalid number!")
                choice=int(input("which card do you want to discard: "))
            discards_pile.append(players[playersturn].pop(choice))
            
        else:
            print("the top of the discards: {}".format(discards_pile[-1]))
            splitcard = discards_pile[-1].split(' ',1)
            
            """
            some game condition judgement
            ex: draw cards
            """
            if splitcard[1]=="reverse":
                playing_direction*=-1
                playersturn=(playersturn-2*playing_direction) % num_of_players
            
            if splitcard[0]=="draw":
                for i in range(4):
                    players[playersturn].append(uno_deck.pop(0))
                    
            if splitcard[1]=="draw two cards":
                for i in range(2):
                    players[playersturn].append(uno_deck.pop(0))
            
            if splitcard[1]=="skip":
                playersturn=(playersturn+playing_direction) % num_of_players
           
            print_cards(playersturn,players[playersturn])

            if can_place_cards(discards_pile,players[playersturn]) is False:
                print("you cannot place a card")
                print("you must draw a card")
                players[playersturn].append(uno_deck.pop(0))    
                continue
            
            choice=int(input("which card do you want to discard: "))
            while choice<0 or choice>=len(players[playersturn]):
                print("invalid number!")
                choice=int(input("which card do you want to discard: "))
            
            if splitcard[0]!="wild" and splitcard[0]!="draw":
                current_color = splitcard[0]
                current_value = splitcard[1]
                while can_play(current_color,current_value,players[playersturn][choice]) is False:
                    print("invalid number to place your card!")
                    print("please enter another number")
                    choice=int(input("which card do you want to discard: "))    
            discards_pile.append(players[playersturn].pop(choice))

        """
        do final check if someone win or not
        """
        if len(players[playersturn])==0:
            print("Player {} win this game! Congratulations!".format(playersturn+1))
            running=False
        else:
            playersturn=(playersturn+playing_direction) % num_of_players
        
play_uno()       