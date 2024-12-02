"""
Sprite Bullets

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:zq
python -m arcade.examples.sprite_bullets
"""
import random
import arcade
import os

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.7
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Bullets Example"

BULLET_SPEED = 7
MOVEMENT_SPEED = 5

Dir_bullet_droite = False
Dir_bullet_gauche = False
Dir_bullet_haut = False
Dir_bullet_bas = False

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

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        """ Initializer """
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

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
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
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    def update_player_speed(self):
        # Calculate speed based on the keys pressed

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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png", SPRITE_SCALING_LASER)

        #Coup en haut
        if Dir_bullet_gauche == False and Dir_bullet_droite == False and Dir_bullet_bas == True and Dir_bullet_haut == False :
            bullet.angle = 180
            bullet.change_y = -BULLET_SPEED
            bullet.center_x = self.player_sprite.center_x
            bullet.top = self.player_sprite.bottom

        #Coup en bas
        elif Dir_bullet_gauche == False and Dir_bullet_droite == False and Dir_bullet_bas == False and Dir_bullet_haut == True :
            bullet.angle = 0
            bullet.change_y = BULLET_SPEED
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

        #Coup à droite
        elif Dir_bullet_gauche == False and Dir_bullet_droite == True and Dir_bullet_bas == False and Dir_bullet_haut == False :
            bullet.angle = -90
            bullet.change_x = BULLET_SPEED
            bullet.center_y = self.player_sprite.center_y
            bullet.left = self.player_sprite.right

        #Coup à gauche
        elif Dir_bullet_gauche == True and Dir_bullet_droite == False and Dir_bullet_bas == False and Dir_bullet_haut == False :
            bullet.angle = 90
            bullet.change_x = -BULLET_SPEED
            bullet.center_y = self.player_sprite.center_y
            bullet.right = self.player_sprite.left
                
        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on bullet sprites
        self.bullet_list.update()
        self.player_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            if len(self.bullet_list) > 1 or (abs(bullet.center_x - self.player_sprite.center_x) > 50) or (abs(bullet.center_y - self.player_sprite.center_y) > 50):
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        global Dir_bullet_droite, Dir_bullet_gauche, Dir_bullet_haut, Dir_bullet_bas

        if key == arcade.key.Z :
            self.up_pressed = True
            self.update_player_speed()
            Dir_bullet_droite = False
            Dir_bullet_gauche = False
            Dir_bullet_haut = True
            Dir_bullet_bas = False

        elif key == arcade.key.S :
            self.down_pressed = True
            self.update_player_speed()
            Dir_bullet_droite = False
            Dir_bullet_gauche = False
            Dir_bullet_haut = False
            Dir_bullet_bas = True

        elif key == arcade.key.Q :
            self.left_pressed = True
            self.update_player_speed()
            Dir_bullet_droite = False
            Dir_bullet_gauche = True
            Dir_bullet_haut = False
            Dir_bullet_bas = False

        elif key == arcade.key.D :
            self.right_pressed = True
            self.update_player_speed()
            Dir_bullet_droite = True
            Dir_bullet_gauche = False
            Dir_bullet_haut = False
            Dir_bullet_bas = False

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z :
            self.up_pressed = False
            self.update_player_speed()

        elif key == arcade.key.S :
            self.down_pressed = False
            self.update_player_speed()

        elif key == arcade.key.Q :
            self.left_pressed = False
            self.update_player_speed()

        elif key == arcade.key.D :
            self.right_pressed = False
            self.update_player_speed()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()