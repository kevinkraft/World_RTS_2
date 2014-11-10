import sys
import pygame
from pygame.locals import *

"""

Items, including resources

"""
# 0 = food size 1
# 1 = wood size 1
# 2 = stone size 2
#


class Item(object):
     """

     All game items

     """
     def __init__(self, itm_type = 0, amount = 1, name = 'default', size = 1):        
          self.name = name
          self.type_ = itm_type
          self.amount = amount
          self.size = size

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
               self.size = 2

     def GetTotalSize(self):
          #returns the total size of that type in the inventory
          return (self.size)*(self.amount)
          
def display_inventory_atributes(selection):
     inv = selection.inventory
     print "--------------------------------------------------------------------------------------------------"
     print "|  Name  |  Type  |  Amount  |  Unit Size |  Total Size  |                                        "
     print "--------------------------------------------------------------------------------------------------"
     print "--------------------------------------------------------------------------------------------------"             
     for j in range(0, len(inv)):
          item = inv[j]
          print "|  {0}  |  {1}  |    {2:.2f}    |   {3}   |  {4:.2f}  |                                     ".format(item.name,
                                                                                                                      item.type_,
                                                                                                                      item.amount,
                                                                                                                      item.size,
                                                                                                                      item.GetTotalSize())
          print "--------------------------------------------------------------------------------------------"

