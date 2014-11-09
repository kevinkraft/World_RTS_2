import sys
import pygame
from pygame.locals import *

"""

Items, including resources

"""
# 0 = food
# 1 = wood
# 2 = stone
#


class Item(object):
     """

     All game items

     """
     def __init__(self, itm_type = 0, amount = 1, name = 'default'):        
          self.name = name
          self.type_ = itm_type
          self.amount = amount

     def set_item_atributes(self, res_type_names):
          #food
          if self.type_ == 0:
               self.name = res_type_names[0]
          #wood
          if self.type_ == 1:
               self.name = res_type_names[1]
          #stone
          if self.type_ == 2:
               self.name = res_type_names[2]

def display_inventory_atributes(selection):
     inv = selection.inventory
     print selection.inventory
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  type  |  Amount  |                                                                       "
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for j in range(0, len(inv)):
          item = inv[j]
          print "|  {0}  |  {1}  |    {2:.2f}    |                                                               ".format(item.name,
                                                                                                                          item.type_,
                                                                                                                          item.amount)
          print "-----------------------------------------------------------------------------------------------"

