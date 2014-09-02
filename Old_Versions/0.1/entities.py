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
     def __init__(self, pos, inventory = [], inventory_size = 10, intr_range = 2, speed = 1.0, destination = []): #speed is distance/s, 0.1 s/cycle (not sure)
          self.pos = pos
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed
          self.destination = destination
          self.inventory = inventory
          self.inventory_size = inventory_size

class Building(Entity):
     """

     All structures

     """
     def __init__(self, pos, building_type, inventory = [], inventory_size = 0, unit_capacity = 0):        
          self.pos = pos
          self.name = Entity.random_name()
          self.inventory = inventory
          self.type = building_type
          self.inventory_size = inventory_size
          self.unit_capacity = unit_capacity

     def set_building_atributes(self, building_type_names):
          #main hut
          if self.type == 0:
               self.name = res_type_names[0]
               self.unit_capacity = 10
          #storage pile
          if self.type == 1:
               self.name = res_type_names[1]
               self.inventory_size = 200
               

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
               
def set_res_type_names():
     res_type_names = []
     for i in range(0,3):
          res_type_names.append(Entity.random_name())
     return res_type_names

def display_unit_atributes(Unit_list):
     #table of unit atributes
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  destination  |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for unit in Unit_list:
          print "|  {}  |  {}  |  {}  |                                                                         ".format(unit.name,
                                                                                                                         unit.pos,
                                                                                                                         unit.destination)
          print "-----------------------------------------------------------------------------------------------"

def display_resource_atributes(Resource_list):
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  type  |  amount  |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for resource in Resource_list:
          print "|  {}  |  {}  |  {}  |  {}  |                                                                   ".format(resource.name,
                                                                                                                          resource.pos,
                                                                                                                          resource.type,
                                                                                                                          resource.amount)
          print "-----------------------------------------------------------------------------------------------"
