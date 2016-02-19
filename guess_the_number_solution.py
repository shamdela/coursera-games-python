# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math

# initialize global variables used in your code
secret_number = 0
number_range = 100
no_of_guesses = 7


# helper function to calculate no of allowed guesses
def calculate_allowed_guesses(high):
    """ Formula : 2 ** n >= high - low + 1 """
    log = math.log(high, 2)
    return int(math.ceil(log))
    
    
# helper function to start and restart the game
def new_game():
    
    global secret_number, number_range, no_of_guesses
    
    # generate secret number
    secret_number = random.randrange(0, number_range)
    
    # Reset number of guesses
    no_of_guesses = calculate_allowed_guesses(number_range)

    # print two blank lines to separate consecutive games
    print
    print
    
    print "New Game. Numbers in the range [0-" + str(number_range) + "]"
    print "Guesses remaining: " + str(no_of_guesses)  

    
# define event handlers for control panel
def range100():
    """ button that changes range to range [0,100) and restarts """
    
    global number_range
        
    number_range = 100
    new_game()
    
    
def range1000():
    """ button that changes range to range [0,1000) and restarts """
    
    global number_range
   
    number_range = 1000
    new_game()
    
    
def input_guess(guess):
    """ main game logic goes here """
    
    global no_of_guesses
    
    # print a blank line to separate guesses
    print
    
    if (int(guess) == secret_number):
        print "Congratulations, You guessed correctly. Number was " + str(secret_number)
        new_game()
    elif (secret_number > int(guess)):
        print "Higher!  Your Guess: " + str(guess)
        no_of_guesses -= 1
        print "Guesses remaining: " + str(no_of_guesses) 
    elif (secret_number < int(guess)):
        print "Lower!  Your Guess: " + str(guess)
        no_of_guesses -= 1
        print "Guesses remaining: " + str(no_of_guesses) 
               
    if (no_of_guesses <= 0):
        print "No guesses remaining - You lose!"  
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the Number" , 200, 200)


# register event handlers for control elements
frame.add_button("Range [0-100]", range100, 200)
frame.add_button("Range [0-1000]", range1000, 200)
frame.add_input("Enter your Guess", input_guess, 200 )


# call new_game and start frame
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
