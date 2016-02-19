# template for "Stopwatch: The Game"

import simplegui
import time

# define global variables
user_score = 0
attempts = 0
current_time = 0
time_string = "0:00:0"
is_timer_running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):        
    # minutes
    a = t // 600   
        
    # tens-seconds       
    b = (t - a * 600) // 100    
               
    # calculate remainder       
    temp_holder = str( (t - (a * 600) + (b * 100)) % 100)
    
    # if seconds value is greater than 9
    if (int(temp_holder) > 9):
        c = temp_holder[0:1] 
        d = temp_holder[1:]       
    else:        
        c = 0  
        d = temp_holder[0:1]      
       
    return str(a) + ":" + str(b) + str(c) + ":" + str(d)
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():    
    global is_timer_running
    is_timer_running = True
    timer.start()
    
def stop_button():
    global user_score, attempts, is_timer_running
    
    if (is_timer_running):
        attempts += 1        
        if (int(time_string[-1]) == 0):
            user_score += 1            
    
    is_timer_running = False
    timer.stop()
    
    
    
def reset_button():
    global attempts, user_score, current_time, time_string    
    user_score = 0
    attempts = 0
    current_time = 0
    time_string = "0:00:0"
    timer.stop()

    
# define event handler for timer with 0.1 sec interval
def tick():
    global current_time, time_string
    current_time = current_time + 1
    time_string = format(current_time)

    
# define draw handler
def draw_handler(canvas):
    score = str(user_score) + "/" + str (attempts)    
    canvas.draw_text(score, (240, 30), 30, "Green")
    canvas.draw_text(str(time_string), (65, 150), 40, "White")
 
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 300)


# create timer
timer = simplegui.create_timer(100, tick)


# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_button)
frame.add_button("Stop", stop_button)
frame.add_button("Reset", reset_button)


# start frame
frame.start()

# Please remember to review the grading rubric
