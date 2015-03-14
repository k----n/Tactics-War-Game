from powerup.base_power import BasePower
import powerup, helper
from tiles import Tile
import pygame

class Health_PUP(BasePower):
    """
    The basic health increasing power up.

    By default the health increase is set to 10.
    
    """
    sprite = pygame.image.load("assets/Health_PUP.png")

    def __init__(self, **keywords):
        #load the base class
        super().__init__(**keywords)

        #load the image for the base class.
        self.image = Health_PUP.sprite

        #set power up specific things.
        self.health = 10
        self.type = "Health +" + str(self.health)

    def use(self, unit):
        # take the min of the addition of health since we cannot go
        # over max health
        unit.health = min(unit.health + self.health, unit.max_health)

        # update the unit health indicator on its sprite
        unit._update_image()

powerup.power_types["Health-PUP"] = Health_PUP
