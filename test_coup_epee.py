import arcade
import time
import math

# Constants
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_SWORD = 0.7
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard and Sword Arc Attack"

MOVEMENT_SPEED = 5
SWORD_DURATION = 0.1  # Durée de l'attaque en secondes
ARC_RADIUS = 60  # Rayon de l'arc d'attaque
ATTACK_COOLDOWN = 0.5  # Cooldown de l'attaque en secondes

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
        """Commence l'attaque avec un mouvement en arc de cercle."""
        self.visible = True
        self.start_time = time.time()

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

        # Calcul du temps écoulé depuis le début de l'attaque
        elapsed_time = time.time() - self.start_time
        if elapsed_time > SWORD_DURATION:
            # Fin de l'attaque
            self.visible = False
            return

        # Calculer l'angle actuel de l'arc de cercle (de -45° à +45°)
        arc_progress = (elapsed_time / SWORD_DURATION)  # Proportion du mouvement terminé
        angle_offset = -45 + 90 * arc_progress  # Mouvement de -45° à +45°
        current_angle = self.direction + angle_offset

        # Calculer la position x, y en fonction du rayon et de l'angle actuel
        radians = math.radians(current_angle)
        self.center_x = player.center_x + ARC_RADIUS * math.cos(radians)
        self.center_y = player.center_y + ARC_RADIUS * math.sin(radians)
        self.angle = current_angle  # Tourner l'épée pour suivre le mouvement

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_list = None
        self.player_sprite = None
        self.sword_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.sword_active = False
        self.last_attack_time = 0  # Temps du dernier lancement d'attaque
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.sword_sprite = Sword(":resources:gui_basic_assets/items/sword_gold.png", SPRITE_SCALING_SWORD)
        self.player_list.append(self.sword_sprite)

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
        current_time = time.time()
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Vérifie si l'attaque est en cooldown
            if not self.sword_active and (current_time - self.last_attack_time) >= ATTACK_COOLDOWN:
                self.sword_sprite.start_swing(self.player_sprite)
                self.sword_active = True
                self.last_attack_time = current_time  # Enregistre le temps de l'attaque

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
