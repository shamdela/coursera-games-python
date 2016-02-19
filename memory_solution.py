# implementation of card game - Memory

import simplegui
import random

# global constants
CARD_RANGE = 8
CARD_WIDTH = 50
CARD_HEIGHT = 100

# helper function to initialize globals
def new_game():
    global memory_deck, exposed, turns, state
    
    memory_deck = range(CARD_RANGE)
    memory_deck = memory_deck * 2 # concatenate list
    random.shuffle(memory_deck)   # shuffle deck 
    
    # Create list of booleans and initialise to False
    exposed = [False] * len(memory_deck)
    
    # initialise turns to zero
    turns = 0
    state = 0
     
        
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global turns, state, prev_card1, prev_card2
    card_clicked = pos[0] // CARD_WIDTH
    
    if state == 0:
        # first turn: increment turns and change state
        prev_card1 = card_clicked
        exposed[card_clicked] = True  # Expose clicked card           
        state = 1;
        turns += 1
    
    elif state == 1:        
        prev_card2 = card_clicked    
        if exposed[card_clicked] == False :
            exposed[card_clicked] = True        
            state = 2
    else:                                
        if exposed[card_clicked] == False :
            exposed[card_clicked] = True   
            state = 1                               
            turns += 1
            
            # if previous 2 choices dont match,
            # hide both cards
            if memory_deck[prev_card1] != memory_deck[prev_card2]:
                exposed[prev_card1] = False    
                exposed[prev_card2] = False
            
            # set previous clicked card
            prev_card1 = card_clicked                    
   
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    number_position = [15, 60]
    x1, x2 = 0, CARD_WIDTH
    counter = 0
    
    for card in memory_deck:
        if exposed[counter] == True:
            canvas.draw_text(str(card), number_position, 40, "White")
        else:
            canvas.draw_polygon([(x1, 0), (x2, 0), (x2, CARD_HEIGHT), (x1, CARD_HEIGHT)], 6, 'Black', 'Green' )
        
        # increment x co-ord for number by the CARD_WIDTH
        number_position[0] += CARD_WIDTH
        counter += 1
        x1 += CARD_WIDTH
        x2 += CARD_WIDTH
    
    label.set_text(turns) # update turns label


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric 