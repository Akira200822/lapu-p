import random

import arcade

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
SCREEN_TITLE="Flappy Bird"
BIRN_ANGLE=25
PIPE_SPEED=4
PIPE_DISTANCE=150


class Animation(arcade.Sprite):
    frame_index = 0
    time = 0

    def update_animation(self, delta_time):
        self.time += delta_time
        if self.time > 0.1:
            self.time = 0
            if self.frame_index == len(self.textures) - 1:
                self.frame_index = 0
            else:
                self.frame_index += 1
            self.set_texture(self.frame_index)
class Pipe(arcade.Sprite):
    def __init__(self,flip):
        super().__init__("pipe.png",0.2,flipped_vertically=flip)
        self.connect = False
        self.flip = flip
        if self.flip:
            self.center_y=random.randint(SCREEN_HEIGHT-SCREEN_HEIGHT/8,SCREEN_HEIGHT)
        else:
            self.center_y=random.randint(0,SCREEN_HEIGHT/8)


        #self.center_x = SCREEN_WIDTH

    def update(self):
        self.center_x -=self.change_x
        if self.right<0:
            self.left=SCREEN_WIDTH
            self.connect = False
            if self.flip:
                self.center_y = random.randint(SCREEN_HEIGHT - SCREEN_HEIGHT / 8, SCREEN_HEIGHT)
            else:
                self.center_y = random.randint(0, SCREEN_HEIGHT / 8)
        if self.right <  SCREEN_WIDTH/4 and self.connect == False:
            window.score += 0.5
            arcade.play_sound(window.point_sound, 0.1)
            self.connect = True



class Bird(Animation):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = SCREEN_WIDTH/4
        self.center_y = SCREEN_HEIGHT / 3

    def update(self):
        self.center_y += self.change_y
        window.isJump = False
        if self.bottom<0:
            self.bottom=0
        if self.top>SCREEN_HEIGHT :
            self.top=SCREEN_HEIGHT

class Game(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("bg.png")
        self.bird=Bird("bird — копия/bird1.png",1)
        self.gameover=arcade.load_texture("gameover.png")
        for i in range(1,4):
            self.bird.append_texture(arcade.load_texture(f"bird — копия/bird{i}.png"))
        self.game = False
        self.isJump=False
        self.start=False
        self.pipelist=arcade.SpriteList()
        self.hit_sound=arcade.load_sound("audio/hit.wav")
        self.wing_sound=arcade.load_sound("audio/wing.wav")
        self.point_sound=arcade.load_sound("audio/point.wav")
        self.score=0

    def setup(self):
        for i in range(6):
            pipe_bottom=Pipe(flip=False)
            pipe_bottom.change_x=PIPE_SPEED
            #pipe_bottom.center_y=0
            pipe_bottom.center_x=PIPE_DISTANCE*i+SCREEN_WIDTH
            self.pipelist.append(pipe_bottom)
            pipe_top=Pipe(flip=True)
            pipe_top.change_x=PIPE_SPEED
            #pipe_top.center_y=SCREEN_HEIGHT
            pipe_top.center_x=PIPE_DISTANCE*i+SCREEN_WIDTH
            self.pipelist.append(pipe_top)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.bird.draw()
        self.pipelist.draw()
        if self.game==False and self.start==True:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                          SCREEN_HEIGHT / 2,
                                          self.gameover.width * 1.5,
                                          self.gameover.height * 1.5,
                                          self.gameover)
        arcade.draw_text(f"Счет:{int(self.score)}", SCREEN_WIDTH/2-20, SCREEN_HEIGHT-20, (0, 0, 0), 20)

    def update(self, delta_time):
        if self.game:
            self.bird.update()
            self.pipelist.update()
            hit_list=arcade.check_for_collision_with_list(self.bird,self.pipelist)
            if len(hit_list)>0:
                self.game=False
                arcade.play_sound(self.hit_sound,0.1)
            if self.isJump!=True:
                self.bird.update_animation(delta_time)



    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.isJump!=True:
            self.bird.change_y = 5.5
            self.bird.angle = BIRN_ANGLE
            self.isJump = True
            self.game=True
            self.start=True
            arcade.play_sound(self.wing_sound, 0.2)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.bird.change_y =-3.5
            self.bird.angle = -BIRN_ANGLE


window=Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
window.setup()
arcade.run()
