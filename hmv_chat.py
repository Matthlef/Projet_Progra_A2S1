import math
from typing import Tuple
import arcade
import os

from arcade.resources import (
    image_female_person_idle,
    image_laser_blue01,
    image_zombie_idle,
)

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.5
SPRITE_SCALING_BULLET = 1
INDICATOR_BAR_OFFSET = 32
ENEMY_ATTACK_COOLDOWN = 1
BULLET_SPEED = 150
BULLET_DAMAGE = 1
PLAYER_HEALTH = 5
SPRITE_SCALING_LASER = 0.7

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Assemblage mob joueur"

LASER_SPEED = 7
MOVEMENT_SPEED = 5


def sprite_off_screen(
    sprite: arcade.Sprite,
    screen_height: int = SCREEN_HEIGHT,
    screen_width: int = SCREEN_WIDTH,
) -> bool:
    """Checks if a sprite is off-screen or not."""
    return (
        sprite.top < 0
        or sprite.bottom > screen_height
        or sprite.right < 0
        or sprite.left > screen_width
    )


class Player(arcade.Sprite):
    def __init__(self, bar_list: arcade.SpriteList) -> None:
        super().__init__(filename=image_female_person_idle, scale=SPRITE_SCALING_PLAYER)
        self.indicator_bar = IndicatorBar(self, bar_list)
        self.health = PLAYER_HEALTH


class MOB(arcade.Sprite):
    def __init__(self, bar_list: arcade.SpriteList) -> None:
        super().__init__(filename=image_zombie_idle, scale=SPRITE_SCALING_ENEMY)
        self.indicator_bar = IndicatorBar(self, bar_list)
        self.health = PLAYER_HEALTH


class Bullet(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__(filename=image_laser_blue01, scale=SPRITE_SCALING_BULLET)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates the bullet's position."""
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time


class IndicatorBar:
    """Represents a bar to display sprite health."""

    def __init__(
        self,
        owner: arcade.Sprite,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color=arcade.color.GREEN,
        background_color=arcade.color.BLACK,
        width=100,
        height=4,
        border_size=4,
    ):
        self.owner = owner
        self.sprite_list = sprite_list

        self._box_width = width
        self._box_height = height
        self._half_box_width = self._box_width // 2

        # Initialize coordinates before fullness
        self._center_x, self._center_y = position

        # Create bar components
        self._background_box = arcade.SpriteSolidColor(
            self._box_width + border_size, self._box_height + border_size, background_color
        )
        self._full_box = arcade.SpriteSolidColor(
            self._box_width, self._box_height, full_color
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set initial position
        self.position = position

        # Initialize fullness after setting position
        self.fullness = 1.0

    @property
    def fullness(self):
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness):
        self._fullness = max(0.0, min(1.0, new_fullness))
        self._full_box.width = self._box_width * self._fullness
        self._full_box.left = self._center_x - (self._box_width // 2)
        self._full_box.visible = self._fullness > 0

    @property
    def position(self):
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position):
        self._center_x, self._center_y = new_position
        self._background_box.position = new_position
        self._full_box.position = new_position

class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.bullet_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()

        self.player_sprite = Player(self.bar_list)
        self.enemy_sprite = MOB(self.bar_list)

        self.enemy_timer = 0
        self.player_direction = (0, 1)

        self.set_mouse_visible(True)

        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 4

        self.enemy_sprite.center_x = SCREEN_WIDTH // 2
        self.enemy_sprite.center_y = SCREEN_HEIGHT // 2

        self.background_color = arcade.color.AMAZON

    def on_draw(self):
        self.clear()
        self.bullet_list.draw()
        self.player_sprite.draw()
        self.enemy_sprite.draw()
        self.bar_list.draw()

    def update_player_speed(self):
        self.player_sprite.change_x = self.player_direction[0] * MOVEMENT_SPEED
        self.player_sprite.change_y = self.player_direction[1] * MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z:
            self.player_direction = (0, 1)
        elif key == arcade.key.S:
            self.player_direction = (0, -1)
        elif key == arcade.key.Q:
            self.player_direction = (-1, 0)
        elif key == arcade.key.D:
            self.player_direction = (1, 0)
        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.Z, arcade.key.S, arcade.key.Q, arcade.key.D):
            self.player_direction = (0, 0)
        self.update_player_speed()

    def on_mouse_press(self, x, y, button, modifiers):
        arcade.play_sound(self.gun_sound)
        bullet = Bullet()
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y

        if self.player_direction == (0, 1):  # Shooting upward
            bullet.change_y = LASER_SPEED
        elif self.player_direction == (0, -1):  # Shooting downward
            bullet.change_y = -LASER_SPEED
        elif self.player_direction == (1, 0):  # Shooting right
            bullet.change_x = LASER_SPEED
        elif self.player_direction == (-1, 0):  # Shooting left
            bullet.change_x = -LASER_SPEED

        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        self.bullet_list.update()

        if self.player_sprite.health <= 0 or self.enemy_sprite.health <= 0:
            arcade.exit()

        self.player_sprite.indicator_bar.position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y + INDICATOR_BAR_OFFSET,
        )
        self.enemy_sprite.indicator_bar.position = (
            self.enemy_sprite.center_x,
            self.enemy_sprite.center_y + INDICATOR_BAR_OFFSET,
        )

        for bullet in self.bullet_list:
            if sprite_off_screen(bullet):
                bullet.remove_from_sprite_lists()

            if arcade.check_for_collision(bullet, self.enemy_sprite):
                self.enemy_sprite.health -= BULLET_DAMAGE
                bullet.remove_from_sprite_lists()
                arcade.play_sound(self.hit_sound)
                self.enemy_sprite.indicator_bar.fullness = (
                    self.enemy_sprite.health / PLAYER_HEALTH
                )

            if arcade.check_for_collision(bullet, self.player_sprite):
                self.player_sprite.health -= BULLET_DAMAGE
                bullet.remove_from_sprite_lists()
                self.player_sprite.indicator_bar.fullness = (
                    self.player_sprite.health / PLAYER_HEALTH
                )


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
