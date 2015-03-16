import pygame, powerup, helper, bmpfont, effects
from pygame.sprite import Sprite

SIZE = 20

class BasePower(Sprite):
    """
    The basic representation of a power from which all other power up types
    extend.
    
    Note: self.image MUST be set in subclasses! This is the tilesheet
    from which the unit renders its actual image.
    """
    active_powers = pygame.sprite.LayeredUpdates()
    
    def __init__(self,
                 tile_x = None,
                 tile_y = None,
                 activate = False,
                 **keywords):

        Sprite.__init__(self)
        
        #Take the keywords off
        self.tile_x = tile_x
        self.tile_y = tile_y

        #Some default values so that nothing complains when trying to
        #assign later
        self._active = False
        
        #Default unit stats
        self.type = "Power Up"
        
        #set required pygame things.
        self.image = None
        self.rect = pygame.Rect(0, 0, SIZE, SIZE)
        
        if activate:
            self.activate()

    @staticmethod
    def get_power_at_pos(pos):
        """
        Returns the active unit at the given tile position, or None if no unit
        is present.
        """
        for p in BasePower.active_powers:
            if (p.tile_x, p.tile_y) == pos:
                return p

        return None
            
    @property
    def tile_pos(self):
        """
        Returns the unit's tile position.
        """
        return (self.tile_x, self.tile_y)
        
    def activate(self):
        """
        Adds this unit to the active roster.
        """
        if not self._active:
            self._active = True
            BasePower.active_powers.add(self)
    
    def deactivate(self, unit):
        """
        Removes this power from the active roster and deactivate unit.
        """
        unit._moving = False

        if self._active:
            self._active = False
            BasePower.active_powers.remove(self)
        
