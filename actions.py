import sys
import pygame
from pygame.locals import *
from copy import deepcopy
from items import *
from entities import *
from functions import *
from config import *

"""

All game actions

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
          elif isinstance(self, Construct):
               print '{0} {1} is constructing {2} at [{3:.2f},{4:.2f}]. It needs {5} more work'.format(type(self.acter).__name__,
                                                                                                       self.acter.name,
                                                                                                       self.construction.name,
                                                                                                       self.construction.pos[0],
                                                                                                       self.construction.pos[1],
                                                                                                       self.construction.work)
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
          elif isinstance(self, Procreate):
               #need to delete action_ from both male and female actions
               self.acter.action.remove(self)
               self.female.action.remove(self)
               del self
          else:
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
               Info("{0} can't collect {1} as they can only reach {2}m, {0} will move within range".format(self.acter.name,
                                                                                                           self.target.name,
                                                                                                           self.acter.intr_range), 
                    'normal')
               self.acter.MoveTo(self.target.pos, prepend_option = True) #if acter is too far away move them into range
               return False #return false when done and inventory is not full
          collects_per_cycle = self.acter.collect_speed/100.0
          self.target.amount = self.target.amount - collects_per_cycle
          item = Item(self.target.type_, collects_per_cycle) #type, amount, name
          item.set_item_atributes(res_type_names)
          self.acter.inventory.append(item)
          return False 

     def AutomaticCollectExchange(self):
          #set up an exchange without user interaction. Used for return to stockpile
          #first get resource type and list of item to exchange and amount
          #Note: I could use dump inventory here, but for later additions(weapons) its best not to
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

def SetupCollect(selection, selected_entity):
     #set up collect action
     print 'Collect {} selected'.format(selected_entity.name)                    
     collect_ = Collect(selection, selected_entity) #acter, target
     selection.action = [collect_]

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
          Info('(self.target.unit_capacity - self.target.GetUnitInventorySize()):', 'debug')
          Info((self.target.unit_capacity - self.target.GetUnitInventorySize()), 'debug')
          if (self.target.unit_capacity - self.target.GetUnitInventorySize()) < 1:
               print "{0} {1} can't enter {2} {3} as it is full or has no unit capacity".format(type(self.acter).__name__, self.acter.name,
                                                                                                type(self.target).__name__, self.target.name)
               self.DeleteAction()
               return
          else:
               self.acter.In_Building = self.target #give it pointer to building
               self.acter.pos = self.target.pos[:]
               self.target.unit_inventory.append(self.acter)
               #print '{0} {1} has entered {2} {3}'.format(type(self.acter).__name__, self.acter.name,
               #                                           type(self.target).__name__, self.target.name)
               self.DeleteAction() #don't delete it so the unit will go back to building after automatic order. See DoEat().
               #No it has to be deleted. See ReturnToBuilding()
               return
               
def SetupEnter(acter_entity, target_entity, append = False):
     #set up the enter building order
     enter_ = Enter(acter_entity, target_entity)
     if append == True:
          enter_.acter.action.append(enter_)
     else:
          enter_.acter.action = [enter_] #override action list
     print '{0} {1} will enter {2} {3}'.format(type(acter_entity).__name__, acter_entity.name,
                                               type(target_entity).__name__, target_entity.name)
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

     def DoExchange(self):
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

     def MakeOrderExchange(self):
          #function to do an automatic exchange as part of an order. Has extra outputs if something is wrong.
          #If you wan to make the exchange straight away use DoExchange().
          if self.DoExchange() == False:
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

def SetupExchangeInternal(selection, selected_entity):
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
          if exchange_.DoExchange() == False:
               del exchange_ #dont use DeleteAction here as it is never in entity.inventory
               return False #user selects an amount larger then the inventory space of the target, go back
          else:
               return True #ends the inner while

def SetupExchange():
     #set up the exchange action order

     print '{}, Exchange inventory with {} selected'.format(selected_entity.name)
     exchange_underway = True
     while exchange_underway: #while loop so user can cancel and go back a step
          dir_choice = make_menu_choice('Choose Direction',['{0} to {1}'.format(selection.name, selected_entity.name),
                                                            '{0} to {1}'.format(selected_entity.name, selection.name)])
          if dir_choice == False:
               print 'Exited'
               break #leave the exchange if user exits
          while True: #this loop allows the user to go back
               str_item_list = [] #stores the names of the items
               if dir_choice == 1:
                    if SetupExchangeInternal(selection, selected_entity) == True:
                         exchange_underway = False #finished sucessfully, leave while loops
                         break
                    else:
                         break #go back one step, but not all the way
               if dir_choice == 2:
                    if SetupExchangeInternal(selected_entity, selection) == True:
                         exchange_underway = False #finished sucessfully, leave while loops
                         break
                    else:
                         break #go back one step, but not all the way
     return

def AutomaticExchange(acter, target, item_type, amount):
     #function to make an automatic exchange as part of some other action, see DoConstruct
     if target.inventory == []:
          return False
     item_exists = False
     for item_ in target.inventory:
          if item_.type_ == item_type: 
               item_exists = True
               if item_.amount < amount:
                    take_amount = - item_.amount #it's minus so the unit can own the action
                    take_item = item_
                    break
               else:
                    take_amount = - amount #it's minus so the unit can own the action
                    take_item = item_
                    break
     if item_exists == False:
          return False
     exchange_ = Exchange(acter, target, [take_item], [take_amount]) #acter, target, item_list, item_amount_list
     acter.action.insert(0, exchange_) #put exchange_ to beginning of action
     return True

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

def SetupAttack(selection, selected_entity):
     #set up the attack order
     print '{0} will attack {1} {2}'.format(selection.name, type(selected_entity).__name__, selected_entity.name)
     attack_ = Attack(selection, selected_entity)
     selection.action = [attack_]

  

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
          #First eat food in the inventory
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
                         collect_ = Collect(acter, res_, False) #return to stockpile False, so they dont starve while collecting
                         acter.action.insert(0, collect_)
                         return
          if food_res == False: #no food resources
               eat_.DeleteAction()
               return
                    
     def AutomaticFoodExchange(self):
          #WILL CONBINE THIS WITH AutomaticExchange BECUASE THEY ARE THE SAME
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
                         food_amount = - item_.amount #it's minus so the unit can own the action
                         food_item = item_
                         break
                    else:
                         food_amount = - food_pickup_amount #it's minus so the unit can own the action
                         food_item = item_
                         break
          if food_item_exists == False:
               return False
          #if the units inventory is full they wont be able to eat
          #if stockpile is full they won't be able to dump their inventory
          unit_inv_size = acter.GetInventorySize()
          if acter.stockpile.GetInventorySize() + unit_inv_size >= acter.stockpile.inventory_capacity:
               acter.DropInventory()
          elif unit_inv_size + food_amount > acter.inventory_capacity:
               acter.DumpInventory()
          exchange_ = Exchange(acter, acter.stockpile, [food_item], [food_amount]) #acter, target, item_list, item_amount_list
          acter.action.insert(0, exchange_) #put exchange_ to beginning of action
          return True
               
class Construct(Action):
     """

     The clss that controls contruction and building

     """
     #this doesnt work, every Construct has to be made with a preexisting Construction
     #def __new__(cls, acter):
     #     from entities import Construction
     #     construction = Construction()
     #     return super(Construct).__init__(cls, acter, construction)

     def __init__(self, acter, construction):
          self.construction = construction
          super(Construct, self).__init__(acter)

     def DoConstruct(self):
          #do one iteration of the construction action
          materials = self.construction.materials 
          acter = self.acter
          #if the construction is finished
          if self.construction == None:
               Info("{0}'s construction has been finished. Deleting construct action.".format(self.acter),'debug')
               self.DeleteAction()
               return
          #how much free space does unit have in inventory
          acter_free_space = acter.inventory_capacity - acter.GetInventorySize()
          #reduce materials needed from items in unit inventory
          if acter.inventory == []:
               pass
          else:
               for key in materials.keys():
                    for item_ in acter.inventory:
                         if item_.type_ == key:
                              if materials[key] > 0:
                                   if item_.amount > materials[key]:
                                        item_.amount = item_.amount - materials[key]
                                        materials[key] = 0
                                        Info('{0} transferred {1} of type {2} to {3}'.format(acter.name, materials[key], key,
                                                                                             self.construction.name),'debug')
                                        return
                                   else:
                                        materials[key] = materials[key] - item_.amount
                                        Info('{0} transferred {1} of type {2} to {3}'.format(acter.name, item_.amount, key,
                                                                                             self.construction.name),'debug')
                                        acter.inventory.remove(item_)
                                        del item_
                                        return
          #go and get resources if needed
          need_resources = False
          for key in materials.keys():
               if materials[key] > 0: #resource needed
                    need_resources = True
          if need_resources == True:
               for key in materials.keys():
                    if materials[key] > 0: #resource needed
                         #check if the resource is in the stockpile
                         in_stockpile = AmountInStockpile(acter.stockpile, key)
                         if in_stockpile == None: #stockpile,item_type
                              #Info('Resources Needed for {0}. {1} of type {2} needed'.format(self.construction.name,
                              #                                                               materials[key],
                              #                                                               key), 'normal')
                              continue
                         else:
                              if in_stockpile < acter_free_space:
                                   take_amount = in_stockpile
                              else:
                                   take_amount = acter_free_space
                         #go and get item
                         acter.MoveTo(self.construction.pos, True) #prepend true
                         #if half inv is full, dump it to make space
                         if acter_free_space < Unit_default_inv_cap/2: 
                              acter.DumpInventory()
                              acter_free_space = acter.inventory_capacity - acter.GetInventorySize()
                         AutomaticExchange(acter, acter.stockpile, key, take_amount) #acter, target, item_type, amount
                         acter.MoveTo(acter.stockpile.pos, True) #prepend true
                         return
               #print 'Resources Needed'
          elif need_resources == False:
               #we have all the materials, start building
               work_per_cycle = acter.construct_speed/100.0               
               self.construction.work = self.construction.work - work_per_cycle
               #delete action if the construct is finished
               if self.construction.work <= 0:
                    self.DeleteAction()
                    return
               return
     
def SetupConstruct(selection, selected_entity):
     #set up a construct for an existing construction
     #make the Construct action class and give it to entity
     construct_ = Construct(selection, selected_entity)     
     selection.action = [construct_]
     return
     
def SetupNewConstruct(selection, building_type_names, Construction_list):
     from entities import Construction
     #set up for construction, where user chooses what to build, where Construction() is made

     #make dict of buildings that can be constructed, type:bool
     #need to have enough resources in the stockpile(might remove this later)
     can_build = {}
     building_types = range(len(building_type_names))
     for i in building_types:
          materials_needed = materials_types[i] #this is a global vec containing the necessary materials for each building type
          enough_in_stockpile = {}
          for key in materials_needed:
               item_type = key
               item_amount = materials_needed[key]
               #if we don't need any
               if item_amount == 0.0:
                    enough_in_stockpile[item_type] = True
                    continue
               #if the stockpile is completely empty
               if selection.stockpile.inventory == []:
                    enough_in_stockpile[item_type] = False
                    continue
               else:
                    for item in selection.stockpile.inventory:
                         if (item.type_ == item_type) and (item.amount >= item_amount):
                              enough_in_stockpile[item_type] = True
                         else:
                              enough_in_stockpile[item_type] = False
          if False in enough_in_stockpile.values():
               can_build[i] = False
          else:
               can_build[i] = True
     #return if can't build any
     if True not in can_build.values():
          print "You don't have enough resources to build anything"
          return
     #make a list of names out of the bool dict 
     name_list = []
     types_list = []
     for key in can_build:
          if can_build[key] == True:
               name_list.append(building_type_names[key])
               types_list.append(key)
     #display ones that can be built in a menu choice
     choice = make_menu_choice('Which building do you want to construct?', name_list)
     if choice == False:
          return
     construction_choice = types_list[choice - 1]
     pos = XYInput('Where do you want to build it?')
     if pos == False: #user cancelled, return
          return
     #make the Construction entity class, it will become a Building
     construction_ = Construction(pos, construction_choice)
     construction_.set_construction_atributes(building_type_names)
     Construction_list.append(construction_)
     #make the Construct action class and give it to entity
     construct_ = Construct(selection, construction_)     
     selection.action = [construct_]
     return
     
          
               



