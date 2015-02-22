import sys
import pygame
from pygame.locals import *
from entities import *
from actions import *

"""

script to contain modules for all the large main loop functions that I don't want in main.py

"""

def ChooseAction(selection, Entity_list, building_type_names, Construction_list):
    #function in which user chooses an action for a list of possible actions
    #Entities to act on must be in range
    #Problem: If there are lots of Entities this is a nightmare to display, need
    #         to make it so that the action to do is selected first before selecting entity based
    #         on what is available not who is available.
    #         Do this as part of the game manager
    
    entities_in_range = [] 
    str_action_list = [] #string of possible actions
    type_action_list =[]
    if selection == []:
        print 'No Unit Selected'
        return
    if type(selection) is Building or type(selection) is Resource:
        print 'Buildings and Resource actions list coming soon'
        return
    for entity in Entity_list + Construction_list:
        #0 attack
        #1 enter
        #2 collect
        #3 exchange inventory
        #4 Procreate
        #5 new Construct
        #6 existing construct
        if entity is selection:
            continue 
        #actions where distance matters
        dist_between = get_dist_between(entity, selection)                    
        if dist_between < selection.intr_range:
            if isinstance(entity, Building):
                str_action_list.append('Enter Buidling {}'.format(entity.name))
                type_action_list.append(1) #1 for Enter 
                entities_in_range.append(entity)
            if isinstance(entity, Resource):
                str_action_list.append('Collect {}'.format(entity.name))
                type_action_list.append(2) #2 for collection            
                entities_in_range.append(entity)
            if isinstance(entity, (Unit, Building)):
                str_action_list.append('Attack {0} {1}'.format(type(entity).__name__, entity.name))
                type_action_list.append(0) #0 for attack
                entities_in_range.append(entity)
                str_action_list.append('Switch inventory with {} {}'.format(type(entity).__name__, entity.name))
                type_action_list.append(3) #3 for exchange inventory                                            
                entities_in_range.append(entity)
            if isinstance(entity, Unit):
                str_action_list.append('Procreate with {0} {1} {2}'.format(entity.gender, type(entity).__name__, entity.name))
                type_action_list.append(4) #4 for procreate
                entities_in_range.append(entity)
            if isinstance(entity, Construction):
                str_action_list.append('Construct {0}'.format(entity.name))
                type_action_list.append(6) #4 for procreate
                entities_in_range.append(entity)
        #actions where distance doesnt matter
        if isinstance(entity, Unit):
            str_action_list.append('Construct Something')
            type_action_list.append(5) #5 for new construct
            entities_in_range.append(None)
    choice = make_menu_choice('Select an Action', str_action_list)
    if choice == False:
        print 'Exited'
        return #user cancels, continue looping over the next event
    selected_entity = entities_in_range[choice - 1]
    selected_action = type_action_list[choice - 1]
    if selected_action == 0:
        #attack
        SetupAttack(selection, selected_entity)
    if selected_action == 1:
        #enter
        SetupEnter(selection, selected_entity)
    if selected_action == 2:
        #unit collects resource
        SetupCollect(selection, selected_entity)
    if selected_action == 3:
        #exchange inventory between entities
        SetupExchange(selection, selectted_entity)
    if selected_action == 4:
        #procreate
        SetupProcreate(selection, selected_entity)                        
    if selected_action == 5:
        #new construct
        SetupNewConstruct(selection, building_type_names, Construction_list)   
    if selected_action == 6:
        #existing construct
        SetupConstruct(selection, selected_entity)   

    return

def ChooseMovement(selection):
    #user chooses the point to move to
    
    while 1: #keeps looping till valid choice made
        if selection == []:
            print 'No Unit Selected'
            break
        else:
            new_x = ReceiveInput('New x-coordinate:', 'Number', True) #string, option, cancel_option
            if new_x == None:
                print 'Exited'
                break #user cancels
            new_y = ReceiveInput('New y-xcoordinate:', 'Number', True)
            if new_y == None:
                print 'Exited'
                break #user cancels
            selection.MoveTo([new_x, new_y])
            break #break while loop
    return

def SelectEntity(Entity_list):
     if len(Entity_list) == 0:
          print 'There are no entites'
          return []
     else:
          selection = []
          choice = make_menu_choice('Select an entity', make_name_type_list(Entity_list))
          if choice == False:
               print 'Exited'
               return []#continue with next event if user cancels
          selection = Entity_list[choice-1]
          print '{} selected'.format(selection.name)
          return selection
