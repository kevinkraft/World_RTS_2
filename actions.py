import sys
import pygame
from pygame.locals import *
from copy import deepcopy
from items import *
from entities import *
from functions import *
from config import *

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
          if isinstance(self, Attack):
               print '{0} is attacking {1} {2} at {3}'.format(self.acter.name, type(self.target).__name__, self.target.name, self.acter.pos)
               return
          elif isinstance(self, Collect):
               print '{0} is collecting {1} at {2}'.format(self.acter.name, self.target.name, self.target.pos) 
               return
          elif isinstance(self, Movement):
               print '{0} is moving from [{1:.2f},{2:.2f}] to [{3:.2f},{4:.2f}]'.format(self.acter.name, self.acter.pos[0], self.acter.pos[1],
                                                                                        self.destination[0], self.destination[1])
               return
          elif isinstance(self, Eat):
               print '{0} {1} is eating at [{2:.2f},{3:.2f}]'.format(type(self.acter).__name__, self.acter.name, self.acter.pos[0],
                                                                     self.acter.pos[1])
               return
          else:
               print "That Action hasn't been given a display yet"
               
          return

     def DeleteAction(self):
          #function to "deep" delete some of the atributes of some of the actions
          if isinstance(self, Attack):
               #no longer need to follow target
               self.acter.destination = []
               self.acter.action.remove(self) #remove self from acter action list
               del self
          if isinstance(self, Procreate):
               #need to delete action_ from both male and female actions
               self.acter.action.remove(self)
               self.female.action.remove(self)
               del self
          else:
               print 'self.acter.action in DeleteAction:'
               print self.acter.action
               self.acter.action.remove(self) #remove self from acter action list
               del self
          return


class Collect(Action):
     """

     The collecting, mining action. 
     
     Note: return_to_stockpile is option to return after inventory is full.
     It is needed as it is not always necessary to return. See DoEat()

     """
     def __init__(self, acter, target, return_to_stockpile = True):        
          self.target = target
          self.return_to_stockpile = return_to_stockpile
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
               return None #if acter is too far away return None to end collection
          collects_per_cycle = self.acter.collect_speed/100.0
          self.target.amount = self.target.amount - collects_per_cycle
          item = Item(self.target.type_, collects_per_cycle) #type, amount, name
          item.set_item_atributes(res_type_names)
          self.acter.inventory.append(item)
          return False #return false when done and inventory is not full

     def AutomaticCollectExchange(self):
          #set up an exchange without user interaction. Used for return to stockpile
          #first get resource type and list of item to exchange and amount
          collect_ = self
          acter = collect_.acter
          res_type = collect_.target.type_
          item_exchange_list = []
          item_exchange_amount = []
          for item in acter.inventory: #resource type and item types should correspond
               if item.type_ == res_type:
                    item_exchange_list.append(item)
                    item_exchange_amount.append(item.amount)
          exchange_ = Exchange(acter, acter.stockpile, item_exchange_list, item_exchange_amount) #acter, target, item_list, item_amount_list
          acter.action.insert(0, exchange_) #put exchange_ to beginning of action

class Enter(Action):
     """

     Class to handle the enter building order

     """
     def __init__(self, acter, target):
          self.target = target
          super(Enter, self).__init__(acter)

     def DoEnter(self):
          #function to put a unit into a building using an enter order
          #first check that the building has enough space
          if self.acter in self.target.unit_inventory:
               print '{0} {1} is already in that building'.format(type(self.acter).__name__, self.acter.name)
               self.DeleteAction()
               return
          if self.acter.In_Building != False:
               print '{0} {1} is already in building {2}'.format(type(self.acter).__name__, self.acter.name, self.acter.In_Building.name)
               self.DeleteAction()
               return
          print '(self.target.unit_capacity - self.target.GetUnitInventorySize()):'
          print (self.target.unit_capacity - self.target.GetUnitInventorySize())
          if (self.target.unit_capacity - self.target.GetUnitInventorySize()) < 1:
               print "{0} {1} can't enter {2} {3} as it is full or has no unit capacity".format(type(self.acter).__name__, self.acter.name,
                                                                                                type(self.target).__name__, self.target.name)
               self.DeleteAction()
               return
          else:
               self.acter.In_Building = self.target #give it pointer to building
               self.acter.pos = self.target.pos
               self.target.unit_inventory.append(self.acter)
               #print '{0} {1} has entered {2} {3}'.format(type(self.acter).__name__, self.acter.name,
               #                                           type(self.target).__name__, self.target.name)
               self.DeleteAction() #don't delete it so the unit will go back to building after automatic order. See DoEat().
               #No it has to be deleted. See ReturnToBuilding()
               return
               
def MakeEnterOrder(acter_entity, target_entity, append = False):
     #set up the enter building order
     enter_ = Enter(acter_entity, target_entity)
     if append == True:
          enter_.acter.action.append(enter_)
     else:
          enter_.acter.action = [enter_] #override action list
     print '{0} {1} will enter {2} {3}'.format(type(acter_entity).__name__, acter_entity.name,
                                               type(target_entity).__name__, target_entity.name)
     return
     
class Exchange(Action):
     """

     The class to handle the exchange of items between inventories
     can give multiple items and amounts in a list

     """
     
     def __init__(self, acter, target, item_list, item_amount_list):
          self.item_list = item_list
          self.item_amount_list = item_amount_list
          self.target = target
          super(Exchange, self).__init__(acter)

     def MakeExchange(self):
          #function to make inventory exchanges and test the size of the target inventory
          print 'self.acter.action in MakeExchange:'
          print self.acter.action
          target = self.target
          total_size = 0
          print 'self.item_list:'
          print self.item_list
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

     def MakeOrderExchange(self):
          #function to make an automatic exchange as part of an order. Has extra outputs if something is wrong.
          #If you wan to make the exchange straight away use MakeExchange().
          print 'self.acter.action in MakeOrderExchange:'
          print self.acter.action
          if self.MakeExchange() == False:
               #false if something is wrong 
               print 'Something is wrong with the exchange order you gave to {0}'.format(self.acter)
               if len(self.item_list) != 1: #if all items were chosen need to change what is printed
                    print 'You asked them to give all of their items to {0} {1}'.format(type(self.target).__name__,
                                                                                        self.target.name)
                    print '{0} has the following items'.format(self.acter.name)
                    display_inventory_atributes(self.acter)    
               else:
                    print 'You asked them to give {0} {1} to {2} {3}'.format(self.item_amount_list[0], self.item_list[0].name,
                                                                             type(self.target).__name__, self.target.name)
               print 'Resubmit choice coming soon. Cancelling All actions'
               #clear the action list, this is necessary as return to stockpile creates a loop
               acter_ = self.acter
               for action_ in acter_.action:
                    action_.DeleteAction()
          else:
               #exchange completed sucessfully
               self.DeleteAction()
               #self.acter.action.remove(self)
               #del self
          return

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
                                            ,'Number', True, 0, item_.amount) #title, option, cancel_option, min, max
               amount_choice_list.append(amount_choice)
               if amount_choice == False or amount_choice == None:
                    print 'Exited'
                    return False #user goes back
          exchange_ = Exchange(selection, selected_entity, item_choice_list, amount_choice_list)
          if exchange_.MakeExchange() == False:
               del exchange_ #dont use DeleteAction here as it is never in entity.inventory
               return False #user selects an amount larger then the inventory space of the target, go back
          else:
               return True #ends the inner while

class Attack(Action):
     """

     The class to handle the attack order/action. Parent Collect is arbitrary and will probably change
     in the future. Attack has acter and target atributes. It will be quite similar to Collect

     """
     def __init__(self, acter, target):
          self.target = target
          super(Attack, self).__init__(acter)
     
     def DoAttack(self):
          from entities import Unit, Building #this may be a bad thing to do?
          #do one iteration of an attack
          if get_dist_between(self.target, self.acter) > self.acter.intr_range: #is acter too far away?
               #print "{} has stopped attacking {} as they can only reach {}".format(self.acter.name,
               #                                                                     self.target.name,
               #                                                                     self.acter.intr_range)
               return False #if acter is too far away return False to get acter to move to new target pos
          damage_per_cycle = (self.acter.attack_speed/100.0)*(self.acter.attack_damage)
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
          #first if unit is in building, leave the building
          self.acter.LeaveBuilding()
          the_unit = self.acter
          the_unit.destination = self.destination #make sure the unit has a destination
          distance_per_cycle = the_unit.speed/100.0
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

class Procreate(Action):
     """

     The baby making class. Note male is the acter

     """
     def __init__(self, acter, female, completeness = 0):        
          self.female = female
          self.completeness = completeness
          super(Procreate, self).__init__(acter)

     def DoProcreate(self):
          from entities import Unit
          #do a step in the procreate action
          #There is a lot to add here, baby, child, care for baby, baby needs to be brought food, child can move around but do very little
          #pos, home stockpile, in same building, born hungry so you'd better have food
          new_entity = Unit(self.female.pos, self.female.stockpile, self.female.In_Building, hunger = 30)
          self.female.In_Building.unit_inventory.append(new_entity)
          self.DeleteAction()
          print '{0} {1} has been born'.format(type(new_entity).__name__, new_entity.name)
          return new_entity

def SetupProcreate(selection, selected_entity):
     #set up procreate
     #check if one male and one female
     if selection.gender == selected_entity.gender:
          print 'This action can only be done with units of different genders'
          print '{0} {1} and {0} {2} are both {3}'.format(type(selection).__name__, selection.name, selected_entity.name,
                                                                            selection.gender)
          return
     #check if both in building
     if selection.In_Building == selected_entity.In_Building:
          if selection.In_Building == False:
               print 'This action can only be done when both units are in the same building'
               return
          #make the procreate action
          if selection.gender == 'M':
               male = selection
               female = selected_entity
          elif selection.gender == 'F':
               female = selection
               male = selected_entity
          procreate_ = Procreate(male, female)
          selection.action = [procreate_]
          selected_entity.action = [procreate_]
     else:
          print 'This action can only be done when both units are in the same building'
          return

class Eat(Action):
     """

     The automatic class that controls eating when hungry 

     """
     def __init__(self, acter):        
          super(Eat, self).__init__(acter)
          
     def DoEat(self, Resource_list):
          #do the eat action in each cycle. Send unit to stockpile if has no food. Send unit to get food if
          #none in stockpile
          acter = self.acter
          eat_ = self
          #Fist eat food in the inventory
          if acter.inventory != []:
               food_item = False
               for item_ in acter.inventory:
                    if item_.type_ == 0: #0 for food
                         if item_.amount < eat_speed: #if there isn't enough
                              continue
                         else:
                              food_item = True
                              item_.amount = item_.amount - eat_speed
                              food_amount = eat_speed
               #now eat the food
               if food_item == True:
                    if acter.hunger >= 100:
                         eat_.DeleteAction()
                         return
                    acter.hunger = acter.hunger + food_amount*food_hunger_value
                    return
          #if no food in inventory go to stockpile
          #check if there is food in the stockpile
          stockpile_has_food = False
          for item_ in acter.stockpile.inventory:
               if item_.type_ == 0: #0 for food
                    stockpile_has_food = True
                    break
          if stockpile_has_food == True: #if stockpile not empty go there
               #if unit in building we want them to go back when they have eaten
               if acter.In_Building != False: #if not false they are in a building
                    acter.ReturnToBuilding()
               if acter.pos != acter.stockpile.pos:
                    acter.MoveTo(acter.stockpile.pos, True)
                    return
               else:
                    if eat_.AutomaticFoodExchange() == True:
                         return #exchange made, eat_ will be done from inventory in next cycle
          #if stockpile empty, go collect food
          if Resource_list == []: #no resources
               eat_.DeleteAction()
               return
          food_res = False
          for res_ in Resource_list:
               if res_.type_ == 0: #for food
                    if acter.In_Building != False: #if not false they are in a building
                         acter.ReturnToBuilding()
                    food_res = True
                    if acter.pos != res_.pos: #not at the resource
                         acter.MoveTo(res_.pos, True) #prepend option, don't overwrite
                         return
                    else:
                         collect_ = Collect(acter, res_, False)
                         acter.action.insert(0, collect_)
                         return
          if food_res == False: #no food resources
               eat_.DeleteAction()
               return
                    
     def AutomaticFoodExchange(self):
          #set up an exchange without user interaction. Used for return to stockpile to get food
          eat_ = self
          acter = eat_.acter
          if acter.stockpile.inventory == []:
               return False
          food_item_exists = False
          for item_ in acter.stockpile.inventory:
               if item_.type_ == 0: #for food
                    food_item_exists = True
                    if item_.amount < food_pickup_amount:
                         food_amount = item_.amount
                         food_item = item_
                         break
                    else:
                         food_amount = food_pickup_amount
                         food_item = item_
                         break
          if food_item_exists == False:
               return False
          exchange_ = Exchange(acter.stockpile, acter, [food_item], [food_amount]) #acter, target, item_list, item_amount_list
          acter.action.insert(0, exchange_) #put exchange_ to beginning of action
          return True
               
               
               



