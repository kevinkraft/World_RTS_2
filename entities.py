import sys
import pygame
from pygame.locals import *
from config import *
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

     All game entities with HP

     """
     def __init__(self, pos, HP = 10, dead = False):
          self.HP = 10
          super(Entity_HP, self).__init__(pos, dead)

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

class Entity_Action(Entity_HP):
     """

     All game entities where actions and inventory are relevant

     """
     def __init__(self, pos, inventory = [], HP = 10, action = [], inventory_capacity = 0, attack_speed = 0, attack_damage = 0, dead = False):
          self.action = action[:]
          self.attack_speed = attack_speed
          self.inventory = inventory[:]
          self.inventory_capacity = inventory_capacity
          self.attack_damage = attack_damage
          super(Entity_Action, self).__init__(pos, HP, dead)

     def GetInventorySize(self):
          #returns the total size of everything currently in the entity inventory
          total_size = 0
          for item in self.inventory:
               total_size = total_size + item.GetTotalSize()
          return total_size

     def DisplayEntityAction(self):
          #prints the relevant details of an Entities action
          if self.action == []:
               print '{0} is doing nothing at {1}'.format(self.name, self.pos)
               return
          else:
               self.action[0].DisplayAction()

     def DropInventory():
          #function that makes the entity drop their inventory items onto the map
          #need to set up item_ positions before I make this function

          print 'ENTITIES: Entity_Action: DropInventory is not yet configured'
          return

#---------------------------------------------------------------------------------

class Building(Entity_Action):
     """

     All structures

     """
     def __init__(self, pos = [0,0], building_type = 0, inventory = [], HP = 10, action = [], inventory_capacity = 0, unit_capacity = 0,
                  attack_speed = 0, attack_damage = 0, dead = False, unit_inventory = [], materials = {}):        
          self.name = Entity.random_name()
          self.type_ = building_type
          self.unit_capacity = unit_capacity
          self.unit_inventory = unit_inventory[:]
          self.materials = materials
          super(Building, self).__init__(pos, inventory, HP, action, inventory_capacity, attack_speed, attack_damage, dead)

     def set_building_atributes(self, building_type_names):
          #main hut/keep
          if self.type_ == 0:
               self.name = building_type_names[0]
               self.unit_capacity = main_hut_default_unit_cap
               self.materials = materials_type0
          #storage pile/stockpile
          if self.type_ == 1:
               self.name = building_type_names[1]
               self.inventory_capacity = 200
               self.materials = materials_type1
          #hut/house     
          if self.type_ == 2:
               self.name = building_type_names[2]
               self.inventory_capacity = hut_default_inv_cap
               self.unit_capacity = hut_default_unit_cap
               self.materials = materials_type2

     def GetUnitInventorySize(self):
          #returns the number of units in the unit_inventory
          val = len(self.unit_inventory)
          return val
     
     def DisplayGarrison(self):
          #prints the atributes of the units in the buildings garrison
          if self.unit_inventory == []:
               print '{0} {1} has no garrison, it has {2} available space'.format(type(self).__name__, self.name, self.unit_capacity)
               return
          print "-----------------------------------------------------------------------------------------------------"
          print "|  name  |  position  |  Gender  |     "
          print "-----------------------------------------------------------------------------------------------------"
          print "-----------------------------------------------------------------------------------------------------"             
          for unit_ in self.unit_inventory:
               print "|  {0}  |  [{1:.2f},{2:.2f}]  |    {3}    |                                             ".format(unit_.name,
                                                                                                                       unit_.pos[0],
                                                                                                                       unit_.pos[1],
                                                                                                                       unit_.gender)

          print "-----------------------------------------------------------------------------------------------------"
          return
               
class Construction(Entity_HP):
     """

     Unfinished buildings. materials is a dictionary of the necessary materials, these numbers are reduced to zero by units
     giving resources to the Construction.

     """
     def __init__(self, pos, building_type, materials = {}, name = 'default', work = 0, HP = 10, dead = False):
          self.name = name
          self.type_ = building_type
          self.materials = materials
          self.work = work
          super(Construction, self).__init__(pos, HP, dead)

     def set_construction_atributes(self, building_type_names):
          #main hut/keep
          if self.type_ == 0:
               self.name = building_type_names[0]+' construction'
               self.materials = materials_type0
               self.work = construct_work0
          #storage pile/stockpile
          if self.type_ == 1:
               self.materials = materials_type1
               self.name = building_type_names[1]+' construction'
               self.work = construct_work1
          #hut/house     
          if self.type_ == 2:
               self.materials = materials_type2
               self.name = building_type_names[2]+' construction'
               self.work = construct_work2


#---------------------------------------------------------------------------------

class Unit(Entity_Action):
     """

     All movable entities. i.e. people

     """
     def __init__(self, pos, stockpile = Building(), In_Building = False, intr_range = 2, inventory = [], HP = 10, action = [],
                  inventory_capacity = Unit_default_inv_cap, speed = 1.0, collect_speed = 1.0, destination = [], attack_speed = 1.0,
                  attack_damage = 1.0, dead = False, gender = 'M', hunger = 100, construct_speed = 1.0):
          #speed is distance/s, 0.1 s/cycle 
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed
          self.collect_speed = collect_speed
          self.destination = destination[:]
          self.stockpile = stockpile
          self.In_Building = In_Building
          self.gender = choice(['M','F'][:])
          self.hunger = hunger
          self.construct_speed = construct_speed
          super(Unit, self).__init__(pos, inventory, HP, action, inventory_capacity, attack_speed, attack_damage, dead)
          
     def MoveTo(self, dest, prepend_option = False, append_option = False):
          #move to destination. prepend_option determines wheather the old action_list is replaced
          #or prepended with the new action 
          move_ = Movement(self, dest) #acter, destination
          self.destination = dest
          if prepend_option == True and append_option == True:
               print '############SOME FUCTION IS CONFIGURED INCORRECTLY#############'
          elif prepend_option == True:
               self.action.insert(0, move_) #put move to beginning of action
          elif append_option == True:
               self.action.append(move_) #put move to end, see DoEat()
          else:
               self.action = [move_] #replace move as the only action

     def TestInBuilding(self):
          #returns False if not in bulding
          #returns building pointer if in building
          if self.In_Building == False:
               return False
          else:
               build_ = self.In_Building 
               return build_

     def TestInBuildingStr(self):
          #returns 'No' if not in building
          #returns building.name at building pos if in building
          build_bool = self.TestInBuilding()
          if build_bool == False:
               return 'No'
          else:
               build_str = '{0} at [{1:.0f},{2:.0f}]'.format(build_bool.name, build_bool.pos[0], build_bool.pos[1])
               return build_str

     def LeaveBuilding(self):
          #entities In_Building is reset to false, entity removed from building inventory
          if isinstance(self, Unit):
               if self.In_Building == False:
                    return
               else:
                    self.In_Building.unit_inventory.remove(self)
                    self.In_Building = False
                    return
          else:
               return

     def ReturnToBuilding(self):
          #puts a move and an enter action to the end of unit action do that they will return to
          #the building they are in NOW after then have completed some other actions. This should
          #be called before those actions are inserted into the action
          if self.In_Building == False:
               print '###########ReturnToBuilding HAS BEEN USED INCORRECTLY##############'
               return
          self.MoveTo(self.In_Building.pos, append_option = True) #append as we want it at the end
          MakeOrderEnter(self, self.In_Building, append = True) #so unit will go back to building then enter when done eating
          return

     def DumpInventory(self):
          #exchange everything in the inventory with the units stockpile
          #this will need to be adapted when I introduce things like weapons in the inventories

          stockpile = self.stockpile
          #save initial position
          initpos = self.pos
          #do move back to initial position
          self.MoveTo(initpos, prepend_option = True)
          #get the amounts in the item list
          if self.inventory == []:
               return
          item_amount_list = []
          for item_ in self.inventory:
               item_amount_list.append(item_.amount)
          #do the exchange
          exchange_ = Exchange(self, stockpile, self.inventory, item_amount_list)
          self.action.insert(0, exchange_)
          #move unit to stockpile
          if self.pos != stockpile.pos:
               self.MoveTo(stockpile.pos, prepend_option = True)

          return
          
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


#---------------------------------------------------------------------------------
# Methods relating to entities
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Displays
#---------------------------------------------------------------------------------

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
     print "|  name  |  position  |  destination  |  HP | In Building |  Gender  | Hunger | "
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for unit in Unit_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   | {4:.2f} |     {5}    |    {6}   |    {7:.2f}    |     ".format(unit.name,
                                                                                                                          unit.pos[0], unit.pos[1], unit.destination, unit.HP, unit.TestInBuildingStr(), unit.gender, unit.hunger)

     print "-----------------------------------------------------------------------------------------------"

def display_construction_atributes(Construction_list):
     #table of construction
     print "-----------------------------------------------------------------------------------------------------"
     print "|       name       |  position  |  type  | Required Work | "
     print "-----------------------------------------------------------------------------------------------------"
     print "-----------------------------------------------------------------------------------------------------"             
     for construction_ in Construction_list:
          print "|  {0}  |  [{1:.2f},{2:.2f}]  |   {3}   | {4} | ".format(construction_.name, construction_.pos[0], construction_.pos[1], construction_.type_, construction_.work)

     print "-----------------------------------------------------------------------------------------------"

#---------------------------------------------------------------------------------
# Others
#---------------------------------------------------------------------------------

def set_entity_type_names(num_types):
     entity_type_names = []
     for i in range(0, num_types):
          entity_type_names.append(Entity.random_name())
     return entity_type_names
