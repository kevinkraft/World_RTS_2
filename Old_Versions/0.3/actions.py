import sys
import pygame
from pygame.locals import *
from copy import deepcopy
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

     def DisplayAction(self):
          #displays the relevant atributes of the action self depending on type
          if isinstance(self, Collect):
               print '{0} is collecting {1} at {2}'.format(self.acter.name, self.target.name, self.target.pos) 
          elif isinstance(self, Movement):
               print '{0} is moving from [{1:.2f},{2:.2f}] to [{3:.2f},{4:.2f}]'.format(self.acter.name, self.acter.pos[0], self.acter.pos[1],
                                                                                        self.destination[0], self.destination[1])
          elif isinstance(self, Attack):
               print '{0} is attacking {1} {2} at {3}'.format(self.acter.name, type(self.target).__name__, self.target.name, self.acter.pos)
          else:
               print "That Action hasn't been given a display yet"
               
          return

class Collect(Action):
     """

     The collecting, mining action

     """
     def __init__(self, acter, target):        
          self.target = target
          super(Collect, self).__init__(acter)

     def DoCollect(self, res_type_names):
          #take resource item from resource and gives it to unit
          if self.acter.inventory_capacity <= self.acter.GetInventorySize(): #is inventory full?
               print "{}'s inventory is at it's maximum size of {}".format(self.acter.name,
                                                                           self.acter.inventory_capacity)
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

class Exchange(Collect):
     """

     The class to handle the exchange of items between inventories
     can give multiple items and amounts in a list

     """
     
     def __init__(self, acter, target, item_list, item_amount_list):
          self.item_list = item_list
          self.item_amount_list = item_amount_list
          super(Exchange, self).__init__(acter, target)

     def MakeExchange(self):
          #function to make inventory exchanges and test the size of the target inventory
          target = self.target
          total_size = 0
          for i in range(0, len(self.item_list)):
               amount = self.item_amount_list[i]
               total_size += self.item_list[i].GetTotalSize(False, amount) 
               #GetTotalSize argument, amount, to get size of, default = item.amount. The items in item_list are those
               #from the acter, so they may not have the same amount as those we will be creating to give to the target
          available_space = target.inventory_capacity - target.GetInventorySize()
          if available_space <= total_size:
               print '{0} only has {1} available space'.format(target.name, available_space)
               print 'Those items take up {0} space'.format(total_size)
               return False
          else:
               for j in range(0, len(self.item_list)):
                    item = self.item_list[j]
                    item_t_copy = deepcopy(item)
                    item_t_copy.amount = self.item_amount_list[j]
                    target.inventory.append(item_t_copy) #add to target inventory
                    item_a_copy = deepcopy(item)
                    item_a_copy.amount = -self.item_amount_list[j] #its minus, so when consolidate inventory is called it will be dealt with
                    self.acter.inventory.append(item_a_copy)
                    print 'Finsihed exchange, {0} {1} has been transferred from {2} to {3}'.format(item_t_copy.amount, item_t_copy.name,
                                                                                                   self.acter.name, self.target.name)
          return True

def SetUpExchange(selection, selected_entity):
     #set up with user interaction menus to make exchange properties
     while True:
          str_item_list = []
          for item in selection.inventory:
               str_item_list.append('{0}[unit size {1}][amount {2}]'.format(item.name, item.size, item.amount))
          str_item_list.append('All')
          item_choice = make_menu_choice('Which Item?', str_item_list)
          if item_choice == False:
               print 'Exited'
               return False #go back
          item_choice_list = []
          if item_choice == len(str_item_list): #if all is selected
               item_choice_list = selection.inventory[:]
          else:
               item_choice_list = [selection.inventory[item_choice - 1]]
          amount_choice_list = []
          for item_ in item_choice_list:
               amount_choice = ReceiveInput('{0} has {1:.2f} {2}. How much to exchange?'.format(selection.name,
                                                                                                item_.amount, item_.name)
                                            ,'Number', 0, item_.amount) #title, option, min, max
               amount_choice_list.append(amount_choice)
               if amount_choice == False: #Not sure this is possible, I removed this from ReceiveInput function
                    print 'Exited'
                    return False #user goes back
          exchange_ = Exchange(selection, selected_entity, item_choice_list, amount_choice_list)
          if exchange_.MakeExchange() == False:
               del exchange_
               return False #user selects an amount larger then the inventory space of the target, go back
          else:
               return True #ends the inner while

class Attack(Collect):
     """

     The class to handle the attack order/action. Parent Collect is arbitrary and will probably change
     in the future. Attack has acter and target atributes. It will be quite similar to Collect

     """
     def __init__(self, acter, target):
          super(Attack, self).__init__(acter, target)
     
     def DoAttack(self):
          from entities import Unit, Building #this may be a bad thing to do?
          #do one iteration of an attack
          if get_dist_between(self.target, self.acter) > self.acter.intr_range: #is acter too far away?
               #print "{} has stopped attacking {} as they can only reach {}".format(self.acter.name,
               #                                                                     self.target.name,
               #                                                                     self.acter.intr_range)
               return False #if acter is too far away return False to get acter to move to new target pos
          damage_per_cycle = (self.acter.attack_speed/60.0)*(self.acter.attack_damage)
          self.target.HP = self.target.HP - damage_per_cycle
          if self.target.dead == True: #remove attack_ if target is dead
               target_ = self.target
               if isinstance(target_, Unit):
                    print '{0} {1} was murdered by {2} {3}, they will pay dearly for this'.format(type(self.target).__name__, self.target.name,
                                                                                                  type(self.acter).__name__, self.acter.name)
               if isinstance(self.target, Building):
                    print '{0} {1} was destroyed by {2} {3}, they will pay dearly for this'.format(type(self.target).__name__,
                                                                                                   self.target.name, type(self.acter).__name__,
                                                                                                   self.acter.name)
               return True
          return 
  

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


          
          
