import sys
import pygame
from pygame.locals import *
import all_names
from random import choice

"""

All game entities

"""

class Entity(object):
     """

     All game entities

     """
     def __init__(self, pos):        
        self.pos = pos
        self.name = Entity.random_name()

     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)

    
