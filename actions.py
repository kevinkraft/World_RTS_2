import sys
import pygame
from pygame.locals import *
from items import *
from entities import *
from functions import *

"""

All game entities

"""

class Action(object):
     """

     All game actions

     """
     def __init__(self, acter):        
          self.acter = acter

class Collect(Action):
     """

     The collecting, mining action

     """
     def __init__(self, acter, target):        
          self.target = target
          super(Collect, self).__init__(acter)

     def DoCollect(self, res_type_names):
          #take resource item from resource and gives it to unit
          if self.acter.inventory_size <= self.acter.GetInventorySize(): #is inventory full?
               print "{}'s inventory is at it's maximum size of {}".format(self.acter.name,
                                                                           self.acter.inventory_size)
               return True #if inventory full return true
          if get_dist_between(self.target, self.acter) > self.acter.intr_range: #is acter too far away?
               print "{} has stop collecting {} as they can only reach {}m".format(self.acter.name,
                                                                                   self.target.name,
                                                                                   self.acter.intr_range)
               return True #if acter is too far away return true to end collection
          collects_per_cycle = self.acter.collect_speed/60.0
          self.target.amount = self.target.amount - collects_per_cycle
          item = Item(self.target.type_, collects_per_cycle) #type, amount, name
          item.set_item_atributes(res_type_names)
          self.acter.inventory.append(item)
          return False #return false when done and inventory is not full

class Movement(Action):
     """

     The moving class

     """
     def __init__(self, acter, destination):        
          self.destination = destination
          super(Movement, self).__init__(acter)
          
     def DoMove(self):
          #move the unit one step towards destination
          the_unit = self.acter
          distance_per_cycle = the_unit.speed/60.0
          if the_unit.pos[0] == the_unit.destination[0]: #dont move in x dir if its already in line, then move in y dir
               if the_unit.pos[1] == the_unit.destination[1]:
                    the_unit.destination = [] #destination reached
                    print "{} moved to {}".format(the_unit.name, the_unit.pos)
                    return True
               elif abs(the_unit.pos[1] - the_unit.destination[1]) < distance_per_cycle: #last step in y
                    the_unit.pos[1] = the_unit.destination[1]
               elif the_unit.pos[1] < the_unit.destination[1]:
                    the_unit.pos[1] = the_unit.pos[1] + distance_per_cycle
               elif the_unit.pos[1] > the_unit.destination[1]:
                    the_unit.pos[1] = the_unit.pos[1] - distance_per_cycle
          elif abs(the_unit.pos[0] - the_unit.destination[0]) < distance_per_cycle:
               the_unit.pos[0] = the_unit.destination[0]
          elif the_unit.pos[0] < the_unit.destination[0]:
               the_unit.pos[0] = the_unit.pos[0] + distance_per_cycle
          elif the_unit.pos[0] > the_unit.destination[0]:
               the_unit.pos[0] = the_unit.pos[0] - distance_per_cycle
          self.destination = the_unit.destination
          return False


          
          
