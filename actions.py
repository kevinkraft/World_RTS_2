import sys
import pygame
from pygame.locals import *

"""

All game entities

"""

class Action(object):
     """

     All game actions

     """
     def __init__(self, acter, target):        
          self.acter = acter
          self.target = target

class Collect(Action):
     """

     The collecting, mining action

     """
     def __init__(self, acter, target):        
          self.acter = acter
          self.target = target
     
     
