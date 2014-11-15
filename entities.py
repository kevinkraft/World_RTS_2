import sys
import pygame
from pygame.locals import *
import all_names
from random import choice
from items import *
from actions import *

"""

All game entities

"""

#---------------------------------------------------------------------------------

class Entity(object):
     """

     All game entities

     """
     def __init__(self, pos, dead = False):        
          self.pos = pos[:]
          self.name = Entity.random_name()
          self.dead = dead
          
     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)

#---------------------------------------------------------------------------------

class Entity_HP(Entity):
     """

     All game entities with HP and inventory

     """
     def __init__(self, pos, inventory = [], HP = 10, action = [], inventory_capacity = 0, attack_speed = 0, attack_damage = 0, dead = False):
          self.HP = 10
          self.inventory = inventory[:]
          self.action = action[:]
          self.inventory_capacity = inventory_capacity
          self.attack_speed = attack_speed
          self.attack_damage = attack_damage
          super(Entity_HP, self).__init__(pos, dead)
          
     def GetInventorySize(self):
          #returns the total size of everything currently in the entity inventory
          total_size = 0
          for item in self.inventory:
               total_size = total_size + item.GetTotalSize()
          return total_size

     def GetNearestStockpile(self, Building_list):
          #returns pointer to nearest stockpile
          dist = []
          pointer_list = []
          for building in Building_list:
               if building.type_ == 1: #1 for stockpile
                   dist.append(get_dist_between(self, building))
                   pointer_list.append(building)
               else:
                    continue
          return pointer_list[dist.index(min(dist))] #return pointer with min dist
          
     def DisplayEntityAction(self):
          #prints the relevant details of an Entities action
          if self.action == []:
               print '{0} is doing nothing at {1}'.format(self.name, self.pos)
               return
          else:
               self.action[0].DisplayAction()

#---------------------------------------------------------------------------------

class Building(Entity_HP):
     """

     All structures

     """
     def __init__(self, pos = [0,0], building_type = 0, inventory = [], HP = 10, action = [], inventory_capacity = 0, unit_capacity = 0,
                  attack_speed = 0, attack_damage = 0, dead = False):        
          self.name = Entity.random_name()
          self.type_ = building_type
          self.unit_capacity = unit_capacity
          super(Building, self).__init__(pos, inventory, HP, action, inventory_capacity, attack_speed, attack_damage, dead)

     def set_building_atributes(self, building_type_names):
          #main hut
          if self.type_ == 0:
               self.name = building_type_names[0]
               self.unit_capacity = 10
          #storage pile
          if self.type_ == 1:
               self.name = building_type_names[1]
               self.inventory_capacity = 200

               
#---------------------------------------------------------------------------------

class Unit(Entity_HP):
     """

     All movable entities. i.e. people

     """
     def __init__(self, pos, intr_range = 2, inventory = [], HP = 10, action = [], inventory_capacity = 10, speed = 1.0, collect_speed = 1.0,
                  destination = [], stockpile = Building(), attack_speed = 1.0, attack_damage = 1.0, dead = False):
          #speed is distance/s, 0.1 s/cycle 
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed
          self.collect_speed = collect_speed
          self.destination = destination[:]
          self.stockpile = stockpile
          super(Unit, self).__init__(pos, inventory, HP, action, inventory_capacity, attack_speed, attack_damage, dead)
          
     def MoveTo(self, dest, prepend_option = False):
          #move to destination. prepend_option determines wheather the old action_list is replaced
          #or prepended with the new action 
          move_ = Movement(self, dest) #acter, destination
          self.destination = dest
          if prepend_option == True:
               self.action.insert(0, move_) #put move to beginning of action
          else:
               self.action = [move_] #replace move as the only action


#---------------------------------------------------------------------------------

class Resource(Entity):
     """

     All resources on map, the resource will be an inventory item of the map resource

     """
     def __init__(self, pos, res_type, amount, dead = False):        
          self.name = 'default'
          self.type_ = res_type
          self.amount = amount
          super(Resource, self).__init__(pos, dead)

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


#---------------------------------------------------------------------------------
# Methods relating to entities
#---------------------------------------------------------------------------------

def set_entity_type_names(num_types):
     entity_type_names = []
     for i in range(0, num_types):
          entity_type_names.append(Entity.random_name())
     return entity_type_names

def display_building_atributes(Building_list):
     #table of building atributes
     print "-----------------------------------------------------------------------------------------------------"
     print "|  Name  |  Position  |  Type  |  Unit Capacity  |  Inventory Capacity  |  Inventory Size  |   HP  | "
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for build in Building_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   |      {4}      |       {5}       |        {6}        | {7:.2f} |".format(build.name,
                                                                                                                                   build.pos[0], build.pos[1], build.type_, build.unit_capacity, build.inventory_capacity, build.GetInventorySize(), build.HP)

     print "-----------------------------------------------------------------------------------------------"

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

def display_unit_atributes(Unit_list):
     #table of unit atributes
     print "-----------------------------------------------------------------------------------------------------"
     print "|  name  |  position  |  destination  |  HP |"
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for unit in Unit_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   | {4:.2f} |                                             ".format(unit.name,
                                                                                                                          unit.pos[0],
                                                                                                                          unit.pos[1],
                                                                                                                          unit.destination,
                                                                                                                          unit.HP)
     print "-----------------------------------------------------------------------------------------------"


          
