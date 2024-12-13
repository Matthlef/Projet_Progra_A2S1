import arcade
import os
import math
from typing import Tuple
import random
import arcade.gui

from arcade.resources import (
    image_female_person_idle,
    image_laser_blue01,
    image_zombie_idle,
)

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SPRITE_SCALING_PLAYER = 0.3
SPRITE_SCALING_ENEMY = 0.5
MOVEMENT_SPEED = 4

SPRITE_SCALING_BULLET = 1
BULLET_SPEED = 150
SPRITE_SCALING_EPEE = 0.7
EPEE_SPEED = 8
BULLET_DAMAGE = 1
ENEMY_ATTACK_COOLDOWN = 1

INDICATOR_BAR_OFFSET = 32
PLAYER_HEALTH = 10
ENEMY_HEALTH = 3

SCREEN_WIDTH = SPRITE_SIZE * 16
SCREEN_HEIGHT = SPRITE_SIZE * 12
SCREEN_TITLE = "Galactic strikeforce 2"

Dir_bullet_droite = False
Dir_bullet_gauche = False
Dir_bullet_haut = False
Dir_bullet_bas = False

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
        super().__init__(
            filename=os.path.join(os.path.dirname(__file__), "doom_slayer.png"),
            scale=SPRITE_SCALING_PLAYER,
        )
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.health: int = PLAYER_HEALTH

    def update(self):
        """ Move the player """
        self.center_x += self.change_x
        self.center_y += self.change_y

class MOB(arcade.Sprite):
    def __init__(self, bar_list: arcade.SpriteList) -> None:
        super().__init__(
            filename=image_zombie_idle,
            scale= SPRITE_SCALING_ENEMY
        )
        self.indicator_bar: IndicatorBarMob = IndicatorBarMob(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.health: int = ENEMY_HEALTH

class Bullet(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__(
            filename=image_laser_blue01,
            scale=SPRITE_SCALING_BULLET,
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates the bullet's position."""
        self.position = (
            self.center_x + self.change_x * delta_time,
            self.center_y + self.change_y * delta_time,
        )

class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.

    :param Player owner: The owner of this indicator bar.
    :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
    bar components.
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        owner: Player,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)

class IndicatorBarMob:
    """
    Represents a bar which can display information about a sprite.

    :param Player owner: The owner of this indicator bar.
    :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
    bar components.
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        owner: MOB,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: MOB = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None
        self.mob = None
        self.mob_list = arcade.SpriteList()

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None

def setup_room_1():
    """
    Create and return room 1.
    """
    room = Room()

    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    y = SCREEN_HEIGHT - SPRITE_SIZE
    for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
        if (x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7) or y == 0:
            wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall5.png"), SPRITE_SCALING/4)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    y = 0
    for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
        wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
        wall.left = x
        wall.bottom = y
        room.wall_list.append(wall)

    # Create left and right column of boxes
    x=0
    for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
        wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
        wall.left = x
        wall.bottom = y
        room.wall_list.append(wall)

    x = SCREEN_WIDTH - SPRITE_SIZE
    for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
        wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall4.png"), SPRITE_SCALING/4)
        wall.left = x
        wall.bottom = y
        room.wall_list.append(wall)

    # Set the background image for this room
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))
    
    return room

def setup_room_2(self):
    """
    Create and return room 2.
    """
    room = Room()


    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7): 
                # Skip making a block 6 and 7 blocks up and down
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x==0:
                # Skip making a block 4 and 5 blocks on the right side
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)
            

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall.jpg"), SPRITE_SCALING/4)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 4 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))

    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_P1(self):
    """
    Create and return room P1.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 6 and x!= SPRITE_SIZE * 7) or y != 0:
                # Skip making a block 6 and 7 blocks dawn
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)


    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor_trap.jpg"))
    for i in range(4): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_3(self):
    """
    Create and return room 3.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
                if (x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7):
                    # Skip making a block 6 and 7 blocks up and down
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5):
                # Skip making a block 4 and 5 blocks up on the right and left side
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)
            

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))
    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_B1():
    """
    Create and return room B1.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 6 and x!= SPRITE_SIZE * 7)or y==0:
                # Skip making a block 6 and 7 blocks up
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                 wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                 wall.left = x
                 wall.bottom = y
                 room.wall_list.append(wall)


    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor_bonus.jpg"))

    return room
    
def setup_room_4(self):
    """
    Create and return room 4.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 2 and x!= SPRITE_SIZE * 3) or y==0:
                # Skip making a block 2 and 3 blocks up
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 4 and y!= SPRITE_SIZE * 5) :
                    # Skip making a block 4 and 5 blocks on the right and left side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 7 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))
    
    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_B2():
    """
    Create and return room B2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 4 and y!= SPRITE_SIZE * 5)or x !=0:
                    # Skip making a block 4 and 5 blocks on the left side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor_bonus.jpg"))

    return room

def setup_room_5(self):
    """
    Create and return room 5.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 2 and x!= SPRITE_SIZE * 3):
                # Skip making a block 2 and 3 blocks up and down
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 6 and y!= SPRITE_SIZE * 7)or x!=0:
                    # Skip making a block 6 and 7 blocks on the left side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))

    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_P2(self):
    """
    Create and return room P2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 6 and x!= SPRITE_SIZE * 7)or y!=0:
                # Skip making a block 6 and 7 blocks down
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 6 and y!= SPRITE_SIZE * 7)or x==0:
                    # Skip making a block 6 and 7 blocks on the right side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor_trap.jpg"))
    
    for i in range(4): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_6(self):
    """
    Create and return room 6.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 2 and x!= SPRITE_SIZE * 3)or y!=0:
                # Skip making a block 2 and 3 blocks down
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 4 and y!= SPRITE_SIZE * 5)or x!=0:
                    # Skip making a block 4 and 5 blocks on the left side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall.jpg"), SPRITE_SCALING/3)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))
    
    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_7(self):
    """
    Create and return room 7.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 6 and x!= SPRITE_SIZE * 7) or y==0:
                # Skip making a block 6 and 7 blocks up
                wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall3.jpg"), SPRITE_SCALING/4)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 4 and y!= SPRITE_SIZE * 5):
                    # Skip making a block 4 and 5 blocks on the left and right side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall6.png"), SPRITE_SCALING/4)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "space_station_wall2.jpg"), SPRITE_SCALING/3)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "space_station_floor.jpg"))
    
    for i in range(2): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

def setup_room_Boss(self):
    """
    Create and return room Boss.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "Boss_wall.png"), SPRITE_SCALING/6)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if (y != SPRITE_SIZE * 4 and y!= SPRITE_SIZE * 5)or x==0:
                    # Skip making a block 4 and 5 blocks on the right side
                    wall = arcade.Sprite(os.path.join(os.path.dirname(__file__), "Boss_wall.png"), SPRITE_SCALING/6)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    room.background = arcade.load_texture(os.path.join(os.path.dirname(__file__), "Boss_floor.png"))
    
    for i in range(6): 
        enemy = MOB(self.bar_list)
        enemy.center_x = random.randrange(SCREEN_WIDTH)
        enemy.center_y = random.randrange(SCREEN_HEIGHT)
        room.mob_list.append(enemy)

    return room

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #player part
        self.epee_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        
        self.player_list =  arcade.SpriteList()
        
        self.bar_list = arcade.SpriteList()
        self.player_sprite = Player(self.bar_list)
        self.enemy_timer = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        #show the mouse cursor
        self.set_mouse_visible(True)
        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")



        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
                # Setup player and enemy positions
        self.player_sprite.position = self.width // 2, self.height // 4
        self.player_list.append(self.player_sprite)

        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2(self)
        self.rooms.append(room)

        room = setup_room_P1(self)
        self.rooms.append(room)

        room = setup_room_3(self)
        self.rooms.append(room)

        room = setup_room_B1()
        self.rooms.append(room)
        
        room = setup_room_4(self)
        self.rooms.append(room)

        room = setup_room_B2()
        self.rooms.append(room)

        room = setup_room_5(self)
        self.rooms.append(room)

        room = setup_room_P2(self)
        self.rooms.append(room)

        room = setup_room_6(self)
        self.rooms.append(room)

        room = setup_room_7(self)
        self.rooms.append(room)

        room = setup_room_Boss(self)
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()
        self.rooms[self.current_room].mob_list.draw()

        # Draw all the sprites
        self.player_sprite.draw()
        self.epee_list.draw()

        self.bullet_list.draw()

        self.bar_list.draw()
        self.player_list.draw()

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
        epee = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png", SPRITE_SCALING_EPEE)

        #Coup en haut
        if Dir_bullet_gauche == False and Dir_bullet_droite == False and Dir_bullet_bas == True and Dir_bullet_haut == False :
            epee.angle = 180
            epee.change_y = -EPEE_SPEED
            epee.center_x = self.player_sprite.center_x
            epee.top = self.player_sprite.bottom

        #Coup en bas
        elif Dir_bullet_gauche == False and Dir_bullet_droite == False and Dir_bullet_bas == False and Dir_bullet_haut == True :
            epee.angle = 0
            epee.change_y = EPEE_SPEED
            epee.center_x = self.player_sprite.center_x
            epee.bottom = self.player_sprite.top

        #Coup à droite
        elif Dir_bullet_gauche == False and Dir_bullet_droite == True and Dir_bullet_bas == False and Dir_bullet_haut == False :
            epee.angle = -90
            epee.change_x = EPEE_SPEED
            epee.center_y = self.player_sprite.center_y
            epee.left = self.player_sprite.right

        #Coup à gauche
        elif Dir_bullet_gauche == True and Dir_bullet_droite == False and Dir_bullet_bas == False and Dir_bullet_haut == False :
            epee.angle = 90
            epee.change_x = -EPEE_SPEED
            epee.center_y = self.player_sprite.center_y
            epee.right = self.player_sprite.left
                
        # Add the bullet to the appropriate lists
        self.epee_list.append(epee)


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
    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Check if the player is dead. If so, exit the game
        if self.player_sprite.health <= 0:
            arcade.exit()
        
        for i in self.rooms[self.current_room].mob_list:
            if i.health <= 0 :
                i.remove_from_sprite_lists()
                i.indicator_bar.position = -500,-500

        # Increase the enemy's timer
        self.enemy_timer += delta_time

        # Update the player's indicator bar position
        self.player_sprite.indicator_bar.position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y + INDICATOR_BAR_OFFSET,
        )

        for i in self.rooms[self.current_room].mob_list:
            i.indicator_bar.position = (i.center_x, i.center_y + INDICATOR_BAR_OFFSET)

        # Call updates on bullet sprites
        self.bullet_list.on_update(delta_time)

        # Check if the enemy can attack. If so, shoot a bullet from the
        # enemy towards the player
        if self.enemy_timer >= ENEMY_ATTACK_COOLDOWN:
            self.enemy_timer = 0

            # Create the bullet
            bullet = Bullet()
            for i in self.rooms[self.current_room].mob_list:
                bullet = Bullet()
            # Set the bullet's position
                bullet.position = i.position

            # Set the bullet's angle to face the player
                diff_x = self.player_sprite.center_x - i.center_x
                diff_y = self.player_sprite.center_y - i.center_y
                angle = math.atan2(diff_y, diff_x)
                angle_deg = math.degrees(angle)
                if angle_deg < 0:
                    angle_deg += 360
                bullet.angle = angle_deg

            # Give the bullet a velocity towards the player
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the bullet list
                self.bullet_list.append(bullet)

        # Loop through each bullet 
            for existing_bullet in self.bullet_list:
            # Check if the bullet has gone off-screen. If so, delete the bullet
                if sprite_off_screen(existing_bullet):
                    existing_bullet.remove_from_sprite_lists()
                    continue

            # Check if the bullet has hit the player
                if arcade.check_for_collision(existing_bullet, self.player_sprite):
                # Damage the player and remove the bullet
                    self.player_sprite.health -= BULLET_DAMAGE
                    existing_bullet.remove_from_sprite_lists()

                # Set the player's indicator bar fullness
                    self.player_sprite.indicator_bar.fullness = (
                        self.player_sprite.health / PLAYER_HEALTH
                    )

        self.epee_list.update()
        self.player_list.update()

        # Loop through each bullet
        for epee in self.epee_list:
            for i in self.rooms[self.current_room].mob_list:
                if arcade.check_for_collision(epee, i):
                # Damage the enemy and remove the epee
                    i.health -= BULLET_DAMAGE
                    epee.remove_from_sprite_lists()

                # Set the player's indicator bar fullness
                    i.indicator_bar.fullness = (
                        i.health / ENEMY_HEALTH
                    )

                # Hit Sound
                    arcade.play_sound(self.hit_sound)

            if len(self.epee_list) > 1 or (abs(epee.center_x - self.player_sprite.center_x) > 50) or (abs(epee.center_y - self.player_sprite.center_y) > 50):
                epee.remove_from_sprite_lists()

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0
        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 1:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0
        
        elif self.player_sprite.center_y < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT
        elif self.player_sprite.center_y < 0 and self.current_room == 2:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT
        
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 1:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 3:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_y < 0 and self.current_room == 3:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT
        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 4:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 3:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 5:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 5:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 6:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 5:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0
        elif self.player_sprite.center_y < 0 and self.current_room == 7:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT

        elif self.player_sprite.center_x < 0 and self.current_room == 7:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 8:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 3:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0
        elif self.player_sprite.center_y < 0 and self.current_room == 8:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT

        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 7:
            self.current_room = 9
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0
        elif self.player_sprite.center_y < 0 and self.current_room == 9:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT

        elif self.player_sprite.center_x < 0 and self.current_room == 9:
            self.current_room = 10
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 10:
            self.current_room = 9
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 10:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT/2

        elif self.player_sprite.center_x < 0 and self.current_room == 10:
            self.current_room = 11
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 11:
            self.current_room = 10
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

class MyView(arcade.View):
    def __init__(self, my_window: arcade.Window):
        super().__init__(my_window)

        self.media_player = None
        self.paused = True
        self.songs = [":resources:music/funkyrobot.mp3",
                      ":resources:music/1918.mp3"]
        self.cur_song_index = 0

        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])

        # This creates a "manager" for all our UI elements
        self.ui_manager = arcade.gui.UIManager(self.window)

        box = arcade.gui.UIBoxLayout(vertical=False)

        # --- Start button
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/"
                                             "sound_off.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "sound_off.png")
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "sound_off.png")

        # Create our button
        self.start_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        # Map that button's on_click method to this view's on_button_click method.
        self.start_button.on_click = self.start_button_clicked  # type: ignore

        # Add in our element.
        box.add(self.start_button)

        # --- Down button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/down.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/down.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/down.png")

        # Create our button
        self.down_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        # Map that button's on_click method to this view's on_button_click method.
        self.down_button.on_click = self.volume_down  # type: ignore
        self.down_button.scale(0.5)

        # Add in our element.
        box.add(self.down_button)

        # --- Up button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/up.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")

        # Create our button
        self.up_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        # Map that button's on_click method to this view's on_button_click method.
        self.up_button.on_click = self.volume_up  # type: ignore
        self.up_button.scale(0.5)

        # Add in our element.
        box.add(self.up_button)

        # --- Right button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/right.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/right.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/right.png")

        # Create our button
        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        # Map that button's on_click method to this view's on_button_click method.
        self.right_button.on_click = self.forward  # type: ignore
        self.right_button.scale(0.5)

        # Add in our element.
        box.add(self.right_button)

        # Place buttons in the center of the screen using an UIAnchorWidget with default values
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box))

    def music_over(self):
        self.media_player.pop_handlers()
        self.media_player = None
        self.sound_button_off()
        self.cur_song_index += 1
        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        self.media_player = self.my_music.play()
        self.media_player.push_handlers(on_eos=self.music_over)

    def volume_down(self, *_):
        if self.media_player and self.media_player.volume > 0.2:
            self.media_player.volume -= 0.2

    def volume_up(self, *_):
        if self.media_player and self.media_player.volume < 1.0:
            self.media_player.volume += 0.2

    def forward(self, *_):
        skip_time = 10

        if self.media_player and self.media_player.time < self.my_music.get_length() - skip_time:
            self.media_player.seek(self.media_player.time + 10)

    def sound_button_on(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")

    def sound_button_off(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_off.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")

    def start_button_clicked(self, *_):
        self.paused = False
        if not self.media_player:
            # Play button has been hit, and we need to start playing from the beginning.
            self.media_player = self.my_music.play()
            self.media_player.push_handlers(on_eos=self.music_over)
            self.sound_button_on()
        elif not self.media_player.playing:
            # Play button hit, and we need to un-pause our playing.
            self.media_player.play()
            self.sound_button_on()
        elif self.media_player.playing:
            # We are playing music, so pause.
            self.media_player.pause()
            self.sound_button_off()

    def on_draw(self):
        self.clear()

        # This draws our UI elements
        self.ui_manager.draw()
        arcade.draw_text("Galactic Strikeforce 2",
                         start_x=0, start_y=self.window.height - 55,
                         width=self.window.width,
                         font_size=40,
                         align="center",
                         color=arcade.color.BLACK)

        if self.media_player:
            seconds = self.media_player.time
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            arcade.draw_text(f"Time: {minutes}:{seconds:02}",
                             start_x=10, start_y=10, color=arcade.color.BLACK, font_size=24)
            volume = self.media_player.volume
            arcade.draw_text(f"Volume: {volume:3.1f}",
                             start_x=10, start_y=50, color=arcade.color.BLACK, font_size=24)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)

        # Registers handlers for GUI button clicks, etc.
        # We don't really use them in this example.
        self.ui_manager.enable()

    def on_hide_view(self):
        # This unregisters the manager's UI handlers,
        # Handlers respond to GUI button clicks, etc.
        self.ui_manager.disable()


if __name__ == "__main__":
    window = arcade.Window(title="Arcade Music Control Demo")
    window.show_view(MyView(window))
    arcade.run()

if __name__ == "__main__":
    main()