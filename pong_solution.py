# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize locals
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    horizontal_velo = random.randrange(120, 240) // 60
    vertical_velo = random.randrange(60, 180) // 60
    
    if direction == LEFT:
        ball_vel = [-horizontal_velo, -vertical_velo]    
    else:
        ball_vel = [horizontal_velo, -vertical_velo]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0 
    score2 = 0
    
    paddle1_pos = (HEIGHT / 2) - HALF_PAD_HEIGHT
    paddle2_pos = (HEIGHT / 2) - HALF_PAD_HEIGHT
    
    direction = LEFT   
    spawn_ball(direction)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # check if ball collides with walls and reflect
    # Left Wall
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:        
        # check if ball hits left paddle and reflect
        # else spawn new ball if it hits gutter.
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]            
            ball_vel[0] += ball_vel[0] * .10  # increase velocity by 10%            
        else:
            spawn_ball(RIGHT)
            score1 += 1
    
    # Right Wall    
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:        
        # check if ball hits right paddle and reflect
        # else spawn new ball if it hits gutter
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]             
            ball_vel[0] += ball_vel[0] * .10  # increase velocity by 10%
        else :
            spawn_ball(LEFT)
            score2 += 1
     
    # Bottom Wall
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:        
        ball_vel[1] = -ball_vel[1]    
    
    # Top Wall
    elif ball_pos[1] <= BALL_RADIUS:             
        ball_vel[1] = -ball_vel[1]        
         
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= 0 and (paddle1_pos + paddle1_vel) <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel) >= 0 and (paddle2_pos + paddle2_vel) <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel 
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH, PAD_HEIGHT + paddle1_pos], [0, paddle1_pos + PAD_HEIGHT]], 10, 'White')
    canvas.draw_polygon([[WIDTH, paddle2_pos], [WIDTH - HALF_PAD_WIDTH, paddle2_pos], [WIDTH - HALF_PAD_WIDTH, PAD_HEIGHT + paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT]], 10, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), [170, 100], 80, 'White')
    canvas.draw_text(str(score2), [400, 100], 80, 'White')
                
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += 3
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 3
    elif key == simplegui.KEY_MAP['down']: 
        paddle2_vel += 3
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']: 
        paddle2_vel = 0
               
# Reset button handler        
def button_handler():        
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset = frame.add_button("Reset", button_handler, 100)

# start frame
new_game()
frame.start()
