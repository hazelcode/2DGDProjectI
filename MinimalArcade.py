import arcade
import pathlib
from enum import auto, Enum

RESOURCE_DIRECTORY = pathlib.Path.cwd() / 'Assets'

class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class GameClassTypes(Enum):
    # all the different types of classes the game is going to manage
    PLAYER = auto()
    BULLET = auto()


class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed:int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window
        self.change_x = 0
        self.change_y = 0
        self.class_type = GameClassTypes.PLAYER

    def move(self):
        # check to see if we are not trying to go out of bounds
        if (self.center_y + self.change_y < self.game.room_height) and\
                (self.change_y + self.center_y > 0):
            self.center_y += self.change_y
        if (self.center_x + self.change_x < self.game.room_width) and\
                (self.change_x + self.center_x > 0):
            self.center_x += self.change_x
        else:
            pass

    def shoot(self):
        # arcade.play_sound(self.gun_sound)

        bullet = arcade.Sprite(RESOURCE_DIRECTORY / 'laserRed01.png', 1)
        bullet.class_type = GameClassTypes.BULLET
        bullet.angle = 0
        bullet.change_x = 20
        bullet.center_x = self.center_x + 24
        bullet.center_y = self.center_y

        self.game.pictlist.append(bullet)


class MimimalArcade(arcade.Window):

    def __init__(self, room_width:int, room_height:int):
        super().__init__(room_width, room_height)
        self.image_path = RESOURCE_DIRECTORY/ "PlayerShip.png"
        self.player = None
        self.direction = MoveEnum.NONE
        self.pictlist = None
        self.room_width = room_width
        self.room_height = room_height
        self.background = None
        arcade.set_background_color(arcade.color.PURPLE)
        self.step = 0
        self.background_step = 0

    def setup(self):
        self.player = MinimalSprite(str(self.image_path), speed=3, game_window=self)
        self.player.center_x = self.room_width/2
        self.player.center_y = self.room_height/2
        self.pictlist = arcade.SpriteList()
        self.pictlist.append(self.player)
        # load background texture
        self.background = arcade.load_texture(RESOURCE_DIRECTORY / 'background.png')

    def on_update(self, delta_time: float):
        #to get really smooth movement we would use the delta time to
        #adjust the movement, but for this simple version I'll forgo that.
        for entity in self.pictlist:
            if entity.class_type == GameClassTypes.PLAYER:
                entity.move()
            if entity.class_type == GameClassTypes.BULLET:
                entity.center_x += entity.change_x

    def on_draw(self):
        """ Render the screen. """
        self.step += 1
        self.background_step -= 2 # there's probably a better way to do this

        if (self.background_step<-self.room_width):
            self.background_step = 0
        arcade.start_render()

        # Draw the background twice so it can appear looping
        arcade.draw_lrwh_rectangle_textured(self.background_step, 0,
                                            self.room_width+2, self.room_height,
                                            self.background)
        arcade.draw_lrwh_rectangle_textured(self.background_step+self.room_width, 0,
                                            self.room_width+2, self.room_height,
                                            self.background)
        # Draw entities
        self.pictlist.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.player.speed
        elif key == arcade.key.SPACE:
            self.player.shoot()

    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = 0
        if (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = 0
        if (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = 0
        if (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = 0

def main():
    """ Main method """
    window = MimimalArcade(800, 600)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()


