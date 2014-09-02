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
     def __init__(self, pos, inventory = []):        
          self.pos = pos
          self.name = Entity.random_name()
          self.inventory = inventory
          
     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)


class Unit(Entity):
     """

     All movable entities. i.e. people

     """
     def __init__(self, pos, inventory = [], intr_range = 2, speed = 1.0, destination = []): #speed is distance/s, 0.1 s/cycle (not sure)
          self.pos = pos
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed
          self.destination = destination
          self.inventory = inventory

     def display_unit_atributes(self):
          print "|  {}  |  {}  |                                                                                ".format(self.name, self.pos)
          print "-----------------------------------------------------------------------------------------------"
          
class Resource(Entity):
     """

     All resources on map, the resource will be an inventory item of the map resource

     """
     def __init__(self, pos, res_type, amount, inventory = []):        
          self.pos = pos
          self.name = 'default'
          self.inventory = inventory
          self.type = res_type
          self.amount = amount

     def set_res_atributes(self, res_type_names):
          #food
          if self.type == 0:
               self.name = res_type_names[0]
          #wood
          if self.type == 1:
               self.name = res_type_names[1]
          #stone
          if self.type == 2:
               self.name = res_type_names[2]
               
     def display_resource_atributes(self):
          print "|  {}  |  {}  |  {}  |  {}  |                                                                  ".format(self.name,
                                                                                                                         self.pos,
                                                                                                                         self.type,
                                                                                                                         self.amount)
          print "-----------------------------------------------------------------------------------------------"

def set_res_type_names():
     res_type_names = []
     for i in range(0,3):
          res_type_names.append(Entity.random_name())
     return res_type_names
