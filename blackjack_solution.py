# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user31_J8jUoTmqYd_0.py

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
instruction = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
     
    def draw_back(self, canvas, pos):        
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []

    def __str__(self):
        # return a string representation of a hand
        self.hand_string = ""        
        for card in self.hand_list:	
            self.hand_string += str(card) + " "
        return "Hand contains " + self.hand_string       
    
    def add_card(self, card):
        self.hand_list.append(card) # add a card object to a hand

    def get_value(self):
        # compute the value of the hand
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        ace_exists = False
        
        for card in self.hand_list:
            hand_value += VALUES.get(card.get_rank())
            if card.get_rank() == 'A':
                ace_exists = True
        
        if ace_exists:               
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        else:
            return hand_value
        
   
    def draw(self, canvas, pos, hide_hole_card):        
        # draw a hand on the canvas, use the draw method for cards
        index = 0
        for card in self.hand_list:
            if in_play and hide_hole_card and index == 0:
                card.draw_back(canvas, pos)	
            else:
                card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20
            index += 1
 
        
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.full_deck = []
        
        for s in SUITS:
            for r in RANKS:
                card = Card(s, r)
                self.full_deck.append(card)
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.full_deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.full_deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        self.deck_string = ""        
        for card in self.full_deck:	
            self.deck_string += str(card) + " "
        return "Deck contains " + self.deck_string    



#define event handlers for buttons
def deal():
    global outcome, in_play, instruction, score
    global deck, player_hand, dealer_hand
    
    if in_play == True:
        score -= 1
        outcome = "You lose last round"
    else:
        outcome = ""
        
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
     
    in_play = True
    instruction = "Hit or Stand?"
    
    
def hit():
    global deck, player_hand, score
    global in_play, outcome, instruction
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card()) 
        outcome = ""
        
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You Bust, Dealer wins"
            in_play = False
            instruction = "New Deal?"
            score -= 1        
        
def stand():
    global deck, dealer_hand, in_play, outcome, instruction, score
    
    if in_play:
        if player_hand.get_value() > 21:
            outcome = "You Bust, Dealer wins"
            
        else:
            # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            if in_play:
                while dealer_hand.get_value() < 17:
                    dealer_hand.add_card(deck.deal_card())          
                                
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
             outcome = "Dealer Busts, You win"
             score += 1
        elif dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value():
            outcome = "You lose"
            score -= 1
        else: 
            outcome = "You win"
            score += 1
            
        instruction = "New Deal?"
        in_play = False    
        
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text("Blackjack", (140, 100), 34, "Cyan", "sans-serif")
    canvas.draw_text("Score: " + str(score), (410, 100), 26, "Black", "sans-serif")
    
    canvas.draw_text("Dealer", (90, 180), 26, "Black", "sans-serif")
    dealer_hand.draw(canvas, [90, 220], True)
              
    canvas.draw_text("Player", (90, 400), 26, "Black", "sans-serif")
    player_hand.draw(canvas, [90, 430], False)
    
    canvas.draw_text(outcome, (270, 180), 24, "Black", "sans-serif")    
    canvas.draw_text(instruction, (270, 400), 24, "Black", "sans-serif")    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric