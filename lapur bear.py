import arcade

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
SCREEN_TITLE="Flappy Bird"

class Game(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width, height, title)



window=Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
arcade.run()