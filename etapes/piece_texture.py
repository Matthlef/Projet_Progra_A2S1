"""
Sprite move between different rooms.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_rooms
"""

import arcade
import os

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10
SCREEN_TITLE = "Sprite Rooms Example"

MOVEMENT_SPEED = 20


class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None

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



def setup_room_2():
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

    return room

def setup_room_P1():
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
    return room

def setup_room_3():
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
    
def setup_room_4():
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

def setup_room_5():
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
    return room

def setup_room_P2():
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

    return room

def setup_room_6():
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

    return room

def setup_room_7():
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

    return room

def setup_room_Boss():
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

        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_sprite = arcade.Sprite(os.path.join(os.path.dirname(__file__), "doom_slayer.png"), SPRITE_SCALING*0.80)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        room = setup_room_P1()
        self.rooms.append(room)

        room = setup_room_3()
        self.rooms.append(room)

        room = setup_room_B1()
        self.rooms.append(room)
        
        room = setup_room_4()
        self.rooms.append(room)

        room = setup_room_B2()
        self.rooms.append(room)

        room = setup_room_5()
        self.rooms.append(room)

        room = setup_room_P2()
        self.rooms.append(room)

        room = setup_room_6()
        self.rooms.append(room)

        room = setup_room_7()
        self.rooms.append(room)

        room = setup_room_Boss()
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
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # If you have coins or monsters, then copy and modify the line
        # above for each list.

        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

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


if __name__ == "__main__":
    main()