import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys, random

### Our list of images ##

# Wall
# Block
# GrassBlock
# StoneBlock
# ShortTree
# TallTree
# Rock
# Chest
# DoorClosed
# DoorOpen
# BlueGem
# GreenGem
# OrangeGem
# Heart
# Key
# Boy
# Cat
# Horns
# Girl
# Princess


#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 5

#### Put class definitions here ####

class BadGuy(GameElement):
    IMAGE = "Cat"
    direction = 1

    def update(self, dt):
        if random.random() < .2:
            next_y = self.y + self.direction

            if next_y < 0 or next_y >= self.board.height:
                self.direction *= -1
                next_y = self.y

            self.board.del_el(self.x, self.y)
            self.board.set_el(self.x, next_y, self)

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    can_open_door = True
    DO = False

    def interact(self, character):
        character.inventory.append(self)
        GAME_BOARD.draw_msg("Nice find! This can open doors! You have %d items!" % (len(character.inventory)))



class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    DO = False


    def interact(self, character):
        new_friend = Character()
        new_friend.change_image("Princess")
        GAME_BOARD.draw_msg("This gem made you a new friend! Go visit her! Your inventory has %s items" % (len(character.inventory)))
        GAME_BOARD.register(new_friend)
        GAME_BOARD.set_el(6, 1, new_friend)


class Reset_stone(GameElement):
    IMAGE = "GreenGem"
    SOLID = True
    DO = False

    def interact(self, character):
        #hackbrighter moves to starting point
        self.board.del_el(self.x, self.y)
        character.board.del_el(character.x, character.y)
        character.board.set_el(2, 2, character) #might have to make this dynamic later

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
    DO = False

class Door(GameElement):

    IMAGE = "DoorClosed"
    SOLID = True

    DO = False


    def __init__(self,xcoordinate=0,ycoordinate=0):
        GameElement.__init__(self)
        GAME_BOARD.set_el(xcoordinate,ycoordinate,self)
        xcoordinate = xcoordinate
        ycoordinate = ycoordinate


    def can_be_opened(self, inventory):
        for i in inventory:
            if getattr(i, 'can_open_door', False):
                return True
        return False

    def interact(self, character):
        character.hover = self
        if self.IMAGE == "DoorClosed" and self.can_be_opened(character.inventory):
            self.change_image("DoorOpen")
            self.SOLID = False
            
        
class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    DO = False

    def interact(self):
        GAME_BOARD.draw_msg("Now you have a heart!") # add to inventory
     #   heart = Heart()
      #  GAME_BOARD.register(heart)
      #  heartx =  character.x + 1
       # hearty = character.y
      #  GAME_BOARD.set_el(heartx, hearty, heart)

class Character(GameElement):
    IMAGE = "Horns"
    SOLID = True
    SPEAK = True
    DO = True

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.hover = None

    def do_thing(self):
        GAME_BOARD.draw_msg("You had me at hello!")
    #     heart = Heart("hackbrighter")
        heart = Heart()
        GAME_BOARD.register(heart)
        GAME_BOARD.set_el(7,1, heart)

 

class Main_Character(Character):
    DO = False


    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"

        self.board.draw_msg("%s moves %s" % (self.IMAGE, direction))

        hover = self.hover

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if next_x > GAME_WIDTH-1 or next_x < 0 or next_y > GAME_HEIGHT-1 or next_y < 0:
                    self.board.draw_msg("That's the edge of the world! You can't go past that!")
                else:

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    if existing_el and existing_el.SOLID:
                        if existing_el.DO:
                            existing_el.do_thing()
                        else:
                            self.board.draw_msg("There's something in my way!")                         
                    elif existing_el is None or not existing_el.SOLID:
                            self.board.del_el(self.x, self.y)
                            if hover:
                                hover.board.set_el(self.x, self.y, hover)
                                self.hover = None

                            self.board.set_el(next_x, next_y, self)

####   End class definitions    ####

# gem_you_want = None

def initialize():
    """Put game initialization code here"""
    # global gem_you_want

    # registering and setting our rocks in the initialize function
    
    rock_positions = [
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 4), 
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

   # rocks[-1].SOLID = False

    bad_dude = BadGuy()
    GAME_BOARD.register(bad_dude)
    GAME_BOARD.set_el(5,4, bad_dude)

    

    doorA = Door(4,3) #pass in coordinates
    GAME_BOARD.register(doorA)

    # registering and setting our hackbrighter in the initialize function

    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(1,1, key1)    

    hackbrighter = Main_Character()
    GAME_BOARD.register(hackbrighter)
    GAME_BOARD.set_el(2, 2, hackbrighter)

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # registering and setting our gem in the initialize function
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    # registering and setting the reset gem in the initialize function
    reset_stone = Reset_stone()
    GAME_BOARD.register(reset_stone)
    GAME_BOARD.set_el(0, 4, reset_stone)




