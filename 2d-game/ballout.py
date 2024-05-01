import pyglet as pg
from pyglet import shapes, window, clock
import os
from DIPPID import SensorUDP
import random
import time
from math import sqrt

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_HEIGHT=1000
WINDOW_WIDTH=1000
app_window = window.Window(WINDOW_HEIGHT,WINDOW_WIDTH)

# Background Image gets loaded and scaled to the window size
background = pg.image.load("background.png")
background.anchor_x = background.width // 2
background.anchor_y = background.height // 2
background = pg.sprite.Sprite(background, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2)
background.scale = max(WINDOW_WIDTH/background.width, WINDOW_HEIGHT/background.height)

class Player:

    def draw(self):
        self.sprite.draw()
        # Check if jump has ended by checking the time
        if self.invincible and time.time() - self.jump_start_time > 2:
            self.invincible = False
            self.sprite.scale /= 1.4
            self.jump_cooldown = time.time()

    # The Image loading was created using Github Copilot
    def __init__(self,x,y, img):
        self.img = pg.image.load(img)
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2
        self.sprite = pg.sprite.Sprite(self.img, x=x, y=y)
        self.sprite.scale = 0.21
        self.invincible = False
        self.jump_cooldown = 0

    def move(self,num):
        self.sprite.x += num
        # Check if player is out of bounds and move to other side
        if self.sprite.x < 0:
            self.sprite.x = WINDOW_WIDTH-2
        if self.sprite.x > WINDOW_WIDTH:
            self.sprite.x = 2

    def jump_start(self):
        if self.invincible or time.time() - self.jump_cooldown < 3:
            return
        self.invincible = True
        self.jump_start_time = time.time()
        self.sprite.scale *= 1.4
    
    def jump_end(self):
        self.invincible = False
    
    def check_collision(self,holes):
        for hole in holes.holes:
            distance = sqrt((self.sprite.x - hole.sprite.x)**2 + (self.sprite.y - hole.sprite.y)**2)
            if distance < self.sprite.width/2 + hole.sprite.width/4 and not self.invincible:
                self.die()
    
    # this could be expanded to show death screen or something and give player health
    def die(self):
        os._exit(0)


class Hole:
    holes = []

    def move_all():
        for hole in Hole.holes:
            hole.move()

    def draw_all():
        for hole in Hole.holes:
            hole.draw()

    def draw(self):
        self.sprite.draw()

    def __init__(self,x,y,speed):
        self.img = pg.image.load("hole.png")
        self.speed = speed
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2
        self.sprite = pg.sprite.Sprite(self.img, x=x, y=y)
        self.sprite.scale = 0.21 

    def move(self):
        self.sprite.y -= self.speed
        if self.sprite.y < -self.sprite.height:
            Hole.holes.remove(self)

    # Holes spawn in a row, most times there are gaps in the row of holes but this is random
    def draw_new(delta_time):
        num_of_holes = random.randint(0,10)
        speed=random.randint(3,6)
        list_of_poisitons = list(range(11))
        # The random.sample function is used to put the random number of holes created previously in random positions in a list
        list_of_holes = random.sample(list_of_poisitons, num_of_holes)
        for i in list_of_holes:
            Hole.holes.append(Hole(x = i*100, y=WINDOW_HEIGHT,speed=speed))


player = Player(100,100, "player.png")
start_time = time.time()

# Im leaving the keybindings for players who want to play with the keyboard
@app_window.event
def on_key_press(key, modifier):
    global player
    if key==window.key.Q:
        os._exit(0)
    if key==window.key.LEFT:
        player.move(-20)
    if key==window.key.RIGHT:
        player.move(20)
    if key==window.key.SPACE:
        player.jump_start()


@app_window.event
def on_draw():
    global player
    global sensor
    app_window.clear()
    background.draw()
    Hole.move_all()
    Hole.draw_all()
    player.draw()
    if(sensor.has_capability('accelerometer')):
        player.move(-5*float(sensor.get_value('accelerometer')['x']))
    if(sensor.has_capability('button_1')):
        if sensor.get_value('button_1') == 1:
            player.jump_start()
    player.check_collision(Hole)

    # Score simply counts the time the player is alive
    pg.text.Label("Score: ", x=10, y=WINDOW_HEIGHT-30, font_size=20).draw()
    pg.text.Label(str(int(time.time() - start_time)), x=90, y=WINDOW_HEIGHT-30, font_size=20).draw()

# Draws new holes every two seconds
clock.schedule_interval(Hole.draw_new, 2)
pg.app.run()
