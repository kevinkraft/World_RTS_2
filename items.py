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
     #################################################################################################
     #   Note that Resource Type MUST match with its corresponding item type. See AutomaticExchange
     #################################################################################################
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

     def GetTotalSize(self, option = True, amount = 0):
          if option == True:
               amount = self.amount
          #returns the total size of that item. Its default to the amount factor being the amount
          #of that item but can be changed if you just want to know the size of a fraction of the
          #amount. See MakeExchange().
          val = (self.size)*(amount)
          return val
          
def display_inventory_atributes(selection):
     inv = selection.inventory
     print "--------------------------------------------------------------------------------------------------"
     print "|  Name  |  Type  |  Amount  |  Unit Size |  Total Size  |   Capacity |                           "
     print "--------------------------------------------------------------------------------------------------"
     for j in range(0, len(inv)):
          item = inv[j]
          print "|  {0}  |  {1}  |    {2:.2f}    |      {3}      |     {4:.2f}     |        {5}       |       ".format(item.name, 
                                                                                                                       item.type_, item.amount, item.size, item.GetTotalSize(), selection.inventory_capacity)

     print "--------------------------------------------------------------------------------------------"

def ConsolidateInventories(Entity_HP_list):
    #consolidate unit inventories, remove empty items
    for i in range(0, len(Entity_HP_list)):
        entity = Entity_HP_list[i]
        if entity.inventory == []:
            continue
        else:
            for j in range(0, len(entity.inventory)):
                item = entity.inventory[j]
                if item.amount < 0.01:
                    #remove if the item is empty
                    entity.inventory.remove(item)
                    del item
                    break
                for k in range(0, len(entity.inventory)):
                    other_item = entity.inventory[k]
                    if other_item == item:
                        Remove_item = False
                        continue
                    else:
                        if item.type_ == other_item.type_:
                            item.amount = item.amount + other_item.amount
                            entity.inventory.remove(other_item)
                            del other_item
                            Remove_item = True
                            break
                if Remove_item == True: #this stops iterating over the second item when it has been removed and no longer exists
                    break
    return
