from powerup.base_power import BasePower
import powerup, helper
from tiles import Tile
import pygame

class Speed_PUP(BasePower):
    """
    The basic speed increasing power up.

    By default speed increase is set to 2.
    
    """
    sprite = pygame.image.load("assets/Speed_PUP.png")

    def __init__(self, **keywords):
        #load the base class
        super().__init__(**keywords)

        #load the image for the base class.
        self.image = Speed_PUP.sprite

        #set power up specific things.
        self.speed = 2
        self.type = "Speed +" + str(self.speed)

    def use(self, unit):
        unit.speed += self.speed
        
powerup.power_types["Speed-PUP"] = Speed_PUP
