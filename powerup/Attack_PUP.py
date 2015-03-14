from powerup.base_power import BasePower
import powerup, helper
from tiles import Tile
import pygame

class Attack_PUP(BasePower):
    """
    The basic attack increasing power up.
   
    By default the attack damage is set to 2.

    Note: This power up will not increase the Transport
          units attack.
    
    """
    sprite = pygame.image.load("assets/Damage_PUP.png")

    def __init__(self, **keywords):
        #load the base class
        super().__init__(**keywords)

        #load the image for the base class.
        self.image = Attack_PUP.sprite

        #set power up specific things.
        self.damage = 2
        self.type = "Attack +" + str(self.damage)

    def use(self, unit):
        if unit.type != "Transport":
            unit.damage += self.damage
        
powerup.power_types["Attack-PUP"] = Attack_PUP
