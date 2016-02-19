# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SHIP_ANGLE_INC = 0.14
SHIP_FRICTION_CONSTANT = 0.015
VELOCITY_VECTOR_INC = 0.15
MISSILE_VELOCITY_CONSTANT = 3

score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas): 
        if not self.thrust:
            # if not thrusting, use 1st tiled image
            # image_center's x co-ord is assigned half of images x value   
            self.image_center[0] = int(ship_info.get_size()[0]) / 2             
        else:
            # if thrusting, use 2nd tiled image
            # add the x value of the ships size, to half of its own value
            self.image_center[0] = int(ship_info.get_size()[0]) / 2 + int(ship_info.get_size()[0])
            
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # position update
        self.pos[0] += self.vel[0]        
        self.pos[1] += self.vel[1]
        
        # angle update
        self.angle += self.angle_vel
        
        # friction update
        self.vel[0] *= (1 - SHIP_FRICTION_CONSTANT)
        self.vel[1] *= (1 - SHIP_FRICTION_CONSTANT)
                
        # compute forward vector
        self.forward = angle_to_vector(self.angle)
               
        # thrust update - acceleration in direction of forward vector
        if self.thrust:
            self.vel[0] += self.forward[0] * VELOCITY_VECTOR_INC
            self.vel[1] += self.forward[1] * VELOCITY_VECTOR_INC    

        # wrap ship around screen if its co-ord go off screen
        check_screen_wrap(self)            
        
    
    def keyup(self, key):
        if simplegui.KEY_MAP["left"] == key:
            self.angle_vel += SHIP_ANGLE_INC
        elif simplegui.KEY_MAP["right"] == key:
            self.angle_vel -= SHIP_ANGLE_INC
        elif simplegui.KEY_MAP["up"] == key:
            self.engage_thruster(False)
            
    def keydown(self, key):        
        if simplegui.KEY_MAP["left"] == key:
            self.angle_vel -= SHIP_ANGLE_INC
        elif simplegui.KEY_MAP["right"] == key:
            self.angle_vel += SHIP_ANGLE_INC
        elif simplegui.KEY_MAP["up"] == key:
            self.engage_thruster(True)
        elif simplegui.KEY_MAP["space"] == key:
            self.shoot()
            
    def engage_thruster(self, engage):        
        global ship_thrust_sound
        
        self.thrust = engage
                
        if engage:        
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
         
    def shoot(self): 
        global a_missile 
        
        # Missile's pos is the tip of your ship's "cannon".         
        missile_pos = [0, 0]
        missile_pos[0] = self.pos[0] + (self.radius * self.forward[0])
        missile_pos[1] = self.pos[1] + (self.radius * self.forward[1])
        
        # Missile velocity should be the sum of the ship's 
        # velocity and a multiple of the ship's forward vector.
        missile_velocity = [0, 0]        
        missile_velocity[0] = self.vel[0] + (self.forward[0] * MISSILE_VELOCITY_CONSTANT)
        missile_velocity[1] = self.vel[1] + (self.forward[1] * MISSILE_VELOCITY_CONSTANT)
        
        a_missile = Sprite(missile_pos, missile_velocity, 0, 0, missile_image, missile_info, missile_sound)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):        
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # position update
        self.pos[0] += self.vel[0]        
        self.pos[1] += self.vel[1]
        
        # angle update
        self.angle += self.angle_vel
        
        # wrap sprite around screen if its co-ord go off screen
        check_screen_wrap(self)            
        
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw lives and score
    canvas.draw_text("Remaining Lives: " + str(lives), (40, 30), 16, 'White', 'sans-serif')
    canvas.draw_text("Score: " + str(score), (660, 30), 16, 'White', 'sans-serif')

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    rock_x_pos = random.randrange(WIDTH)
    rock_y_pos = random.randrange(HEIGHT)
    vel_x_pos = random.randrange(-2, 3)
    vel_y_pos = random.randrange(-2, 3)
    
    lower = -0.1
    upper = 0.1
    range_width = upper - lower
    ang_vel = random.random() * range_width + lower
    
    a_rock = Sprite([rock_x_pos, rock_y_pos], [vel_x_pos, vel_y_pos], 0, ang_vel, asteroid_image, asteroid_info)

# key handlers
def keyup_handler(key):
    my_ship.keyup(key)
    
def keydown_handler(key):   
    my_ship.keydown(key)
    
def check_screen_wrap(object):
    # wrap object around screen if its co-ord go off screen                
    if object.pos[0] > WIDTH :
        object.pos[0] = object.pos[0] - WIDTH        
    elif object.pos[0] < 0 - (object.radius / 2):
        object.pos[0] = object.pos[0] + WIDTH 
            
    if object.pos[1] > HEIGHT:
        object.pos[1] = object.pos[1] - HEIGHT            
    elif object.pos[1] < 0 - (object.radius / 2):
        object.pos[1] = object.pos[1] + HEIGHT 

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.08, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()