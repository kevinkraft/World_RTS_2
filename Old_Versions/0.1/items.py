import sys
import pygame
from pygame.locals import *

"""

Items, including resources

"""
class Item(object):
     """

     All game items

     """
     def __init__(self, itm_type = 0, amount = 1, name = 'default'):        
          self.name = name
          self.itm_type = itm_type
          self.amount = amount

    
