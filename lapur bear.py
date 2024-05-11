import arcade

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
SCREEN_TITLE="Flappy Bird"
BIRN_ANGLE=25

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

class Bird(Animation):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = SCREEN_WIDTH/4
        self.center_y = SCREEN_HEIGHT / 3

    def update(self):
        self.center_y += self.change_y
        window.isJump = False


class Game(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("bg.png")
        self.bird=Bird("bird — копия/bird1.png",1)
        for i in range(1,4):
            self.bird.append_texture(arcade.load_texture(f"bird — копия/bird{i}.png"))
        self.game = True
        self.isJump=False

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.bird.draw()


    def update(self, delta_time):
        if self.game:
            self.bird.update()
            if self.isJump!=True:
                self.bird.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.isJump!=True:
            self.bird.change_y = 5.5
            self.bird.angle = BIRN_ANGLE
            self.isJump = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.bird.change_y =-3.5
            self.bird.angle = -BIRN_ANGLE


window=Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
arcade.run()
