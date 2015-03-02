from unit.ground_unit import GroundUnit
import unit, helper, effects
from tiles import Tile
import pygame
from queue import deque

class Transport(GroundUnit):
    """
    A troop transport. Heavy armour, no weapons, and can travel far distances on ground.
    Additionally, it can be loaded with other ground units up to some capacity.
    """
    sprite = pygame.image.load("assets/transport.png")
    
    def __init__(self, **keywords):
        #load the image for the base class.
        self._base_image = Transport.sprite

        #load the base class
        super().__init__(**keywords)

        #sounds
        self.move_sound = "TankMove"
        self.hit_sound = "TankFire"

        #set unit specific things.
        self.type = "Transport"
        self.speed = 8
        self.max_atk_range = 0
        self.damage = 6
        self.defense = 4
        self.hit_effect = effects.Explosion

        self.health = 20   
        self.max_health = self.health     
        self.capacity = 100

        self.carrying = deque()
        
        #the unit cannot attack, so set the attack state to false
        self.turn_state = [False, True]

        self._update_image()

    def add_unit(self, load_unit):
        """
        Add the unit to the transport. Ideally, this is called
        at the end of the movement along a path for load_unit
        in their update() method.
        """

        if not self.can_load(load_unit):
            raise ValueError("cannot load unit")

        self.capacity -= load_unit.unit_size
        self.carrying.append(load_unit)
        load_unit.deactivate()


    def is_passable(self, tile, pos):
        """
        Returns whether or not this unit can move over a certain tile.
        """
        #Check superclass to see if it's passable first
        if not super().is_passable(tile, pos):
            return False

        #This unit can't pass these specific terrains
        if (tile.type == 'mountain' or
            tile.type == 'forest'):
            return False
        
        #The tile is passable
        return True
                                     
    def can_hit(self, target_unit):
        """
        Determines whether a unit can hit another unit.
        
        Overrides because transports cannot hit anything.
        """

        return False

    def turn_ended(self):
        """
        Called when the turn for the team has ended.

        Overrides because the transport can never attack.
        """

        self.turn_state = [False, True]
        return True

    def can_load(self, load_unit):
        """
        Determine if load_unit can be loaded into the transport.
        """

        if load_unit.team != self.team or \
           not isinstance(load_unit, unit.ground_unit.GroundUnit) or \
           load_unit.type == "Transport" or \
           load_unit.unit_size > self.capacity:
            return False
        return True

    def pop_front_unit(self, tile, pos):
        """
        Determine if the unit at the front of the deque
        (i.e. the one that has been loaded the longest)
        can be extracted and placed at position pos.

        If so, then do it.
        """
        if not self.carrying:
            raise IndexError("pop from an empty transport")
        
        top_u = self.carrying[0]
        if top_u.is_stoppable(tile, pos):
            top_u.activate()
            top_u.tile_x, top_u.tile = self.tile_x, self.tile_y
            top_u.in_transport = None
            top_u.set_path([(self.tile_x, self.tile_y), pos])
            self.capacity += top_u.unit_size
            self.carrying.popleft()
            return True

        return False

    def update(self):
        """
        In addition to the usual update from the super class,
        make sure very unit that is being carried also hase
        the same position.
        """

        super().update()
        for u in self.carrying:
            u.tile_x, u.tile_y = self.tile_x, self.tile_y
        
    
unit.unit_types["Transport"] = Transport
