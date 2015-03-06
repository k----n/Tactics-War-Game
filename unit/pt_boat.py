import effects
import unit
import pygame


class PTBoat(unit.water_unit.WaterUnit):
    """
    The PT Boat is a more agile but more fragile water unit
    """
    sprite = pygame.image.load("assets/PT-boat.png")

    def __init__(self, **keywords):
        # load the image for the base class
        self._base_image = PTBoat.sprite

        # load the super class (water unit)
        super().__init__(**keywords)

        # sounds
        self.hit_sound = "ArilleryFire"

        # set unit specific things
        self.type = "PTBoat"
        self.speed = 12
        self.max_atk_range = 6
        self.damage = 4
        self.defense = 1
        self.hit_effect = effects.Explosion
        self.health = 6
        self.max_health = self.max_health
        self._update_image()

unit.unit_types["PTBoat"] = PTBoat
