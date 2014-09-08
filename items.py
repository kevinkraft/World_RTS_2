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
          self.type = itm_type
          self.amount = amount

     def set_item_atributes(self, res_type_names):
          #food
          if self.type == 0:
               self.name = res_type_names[0]
          #wood
          if self.type == 1:
               self.name = res_type_names[1]
          #stone
          if self.type == 2:
               self.name = res_type_names[2]

def display_inventory_atributes(inventory):
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  type  |  Amount  |                                                                       "
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for item in inventory:
          print "|  {0}  |  {1}  |    {2}    |                                                                   ".format(item.name,
                                                                                                                          item.type,
                                                                                                                          item.amount)
          print "-----------------------------------------------------------------------------------------------"

