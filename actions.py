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
     def __init__(self, acter):        
          self.acter = acter

class Collect(Action):
     """

     The collecting, mining action

     """
     def __init__(self, acter, target):        
          self.target = target
          super(Collect, self).__init__(acter)

     def DoCollect(self):
          collects_per_cycle = self.acter.collect_speed/60.0
          self.target.amount = self.target.amount - collects_per_cycle
          item = Item(self.target.type_, collects_per_cycle) #type, amount, name
          item.set_item_atributes(res_type_names)
          self.acter.inventory.append(item)


class Movement(Action):
     """

     The moving class

     """
     def __init__(self, acter, destination):        
          self.destination = destination
          super(Movement, self).__init__(acter)
          
     def DoMove(self):
          the_unit = self.acter
          distance_per_cycle = the_unit.speed/60.0
          if the_unit.pos[0] == the_unit.destination[0]: #dont move in x dir if its already in line, then move in y dir
               if the_unit.pos[1] == the_unit.destination[1]:
                    the_unit.destination = [] #destination reached
                    print "{} moved to {}".format(the_unit.name, the_unit.pos)
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


          
          
