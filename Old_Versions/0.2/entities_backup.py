import sys
import pygame
from pygame.locals import *
import all_names
from random import choice

"""

All game entities

"""

#---------------------------------------------------------------------------------

class Entity(object):
     """

     All game entities

     """
     def __init__(self, pos, inventory = []):        
          self.pos = pos[:]
          self.name = Entity.random_name()
          self.inventory = inventory[:]
          
     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)


#---------------------------------------------------------------------------------

class Entity_HP(Entity):
     """

     All game entities with HP

     """
     def __init__(self, pos, inventory = [], HP = 10):        
          self.pos = pos[:]
          self.name = Entity.random_name()
          self.inventory = inventory[:]
          self.HP = 10
          
     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)

#---------------------------------------------------------------------------------

class Unit(Entity_HP):
     """

     All movable entities. i.e. people

     """
     def __init__(self, pos, intr_range = 2, inventory = [], HP = 10, inventory_size = 10, speed = 1.0, collect_speed = 1.0, 
                  destination = []): #speed is distance/s, 0.1 s/cycle (not sure)
          self.pos = pos
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed
          self.destination = destination
          self.inventory = inventory[:]
          self.HP = 10
          self.inventory_size = inventory_size
          self.collect_speed = collect_speed
          

#---------------------------------------------------------------------------------

class Building(Entity_HP):
     """

     All structures

     """
     def __init__(self, pos, building_type, inventory = [], HP = 10, inventory_size = 0, unit_capacity = 0):        
          self.pos = pos
          self.name = Entity.random_name()
          self.inventory = inventory[:]
          self.HP = 10
          self.type_ = building_type
          self.inventory_size = inventory_size
          self.unit_capacity = unit_capacity

     def set_building_atributes(self, building_type_names):
          #main hut
          if self.type_ == 0:
               self.name = building_type_names[0]
               self.unit_capacity = 10
          #storage pile
          if self.type_ == 1:
               self.name = building_type_names[1]
               self.inventory_size = 200

               
#---------------------------------------------------------------------------------

class Resource(Entity):
     """

     All resources on map, the resource will be an inventory item of the map resource

     """
     def __init__(self, pos, res_type, amount, inventory = []):        
          self.pos = pos
          self.name = 'default'
          self.inventory = inventory
          self.type_ = res_type
          self.amount = amount

     def set_res_atributes(self, res_type_names):
          #food
          if self.type_ == 0:
               self.name = res_type_names[0]
          #wood
          if self.type_ == 1:
               self.name = res_type_names[1]
          #stone
          if self.type_ == 2:
               self.name = res_type_names[2]

def display_resource_atributes(Resource_list):
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  type  |  amount  |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for resource in Resource_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   |  {4:.2f}  |                                      ".format(resource.name,
                                                                                                                     resource.pos[0],
                                                                                                                     resource.pos[1],
                                                                                                                     resource.type_,
                                                                                                                     resource.amount)
          print "-----------------------------------------------------------------------------------------------"

#---------------------------------------------------------------------------------

def set_entity_type_names(num_types):
     entity_type_names = []
     for i in range(0,num_types):
          entity_type_names.append(Entity.random_name())
          return entity_type_names

def display_building_atributes(Building_list):
     #table of building atributes
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  type  |  unit capacity  |  inventory size  |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for build in Building_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   |     {4}     |     {5}     |                           ".format(build.name,
                                                                                                                          build.pos[0],
                                                                                                                          build.pos[1],
                                                                                                                          build.type_,
                                                                                                                          build.unit_capacity,build.inventory_size)
     print "-----------------------------------------------------------------------------------------------"

def display_unit_atributes(Unit_list):
     #table of unit atributes
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  destination  |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for unit in Unit_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   |                                                      ".format(unit.name,
                                                                                                                         unit.pos[0],
                                                                                                                         unit.pos[1],
                                                                                                                         unit.destination)
     print "-----------------------------------------------------------------------------------------------"



          
