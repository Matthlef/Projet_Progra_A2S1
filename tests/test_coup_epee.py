import arcade
import os
import random

# Constants
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.7
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard and Sword Arc Attack"

MOVEMENT_SPEED = 5
BULLET_SPEED = 5

class Player(arcade.Sprite):
    def update(self):
        """ Move the player """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class Sword(arcade.Sprite):
    def __init__(self, image, scaling):
        super().__init__(image, scaling)
        self.visible = False
        self.start_time = None
        self.direction = 0

    def start_swing(self, player):
        
        # Direction du joueur (on utilise la dernière direction connue si le joueur est immobile)
        if player.change_x > 0:
            self.direction = 0  # Droite
        elif player.change_x < 0:
            self.direction = 180  # Gauche
        elif player.change_y > 0:
            self.direction = 90  # Haut
        elif player.change_y < 0:
            self.direction = -90  # Bas

    def update_position(self, player):
        """Mise à jour de la position pour créer un mouvement d'arc."""
        if not self.visible:
            return

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_list = None
        self.player_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        arcade.set_background_color(arcade.color.AMAZON)
        
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.sword_sprite = Sword(":resources:gui_basic_assets/items/sword_gold.png", SPRITE_SCALING_LASER)
        self.player_list.append(self.sword_sprite)
        
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        self.player_list.update()
        if self.sword_active:
            self.sword_sprite.update_position(self.player_sprite)
            if not self.sword_sprite.visible:
                self.sword_active = False

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png", SPRITE_SCALING_LASER)

        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet.angle = 0

        # Give the bullet a speed
        bullet.change_y = BULLET_SPEED

        # Position the bullet
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.Q:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Z:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.Q:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
