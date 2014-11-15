import sys
import pygame
from pygame.locals import *

"""

orders need to be classes as they are complex instructions carried by messengers as inventory

"""

class Order(object):
     """

     All game items. holder is the person who has it in their inventory. action_list is a list of class action instances.
     target is the class entity instance who the order is for 

     """
     def __init__(self, holder, action_list, target):        
          self.holder = holder
          self.action_list = action_list[:]
          self.target = target
