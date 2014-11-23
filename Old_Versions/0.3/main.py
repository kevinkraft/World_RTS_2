#World RTS 2
#Version: 0.3
#
#Kevin Maguire
#9/11/14
#
#Notes:
# Interface will be multiple choice in terminal menus for now. Tables in ASCII if there are any.
# The game will have continuous coordinates and will not be based on a grid
# Every entity will have a positive grid coordinate(x,y) which increases right for x and down for y, as in pygame.
# Entities will include everything, units, buildings, resources. Except Terrain, which will be based on ranges. 
#
#Add:
#Orders
#  Complex so do it with classes
#  Carried by people in their inventories
#  Unit will have an action artibute to contain current action (done)
#  Unit will have an order list, when an action is finished the first item in order will become the action (done)
#    Action_list and order list are now the same thing (done)
#  So an order will be a series of actions in a list
#Actions
# Add inventory capacity (done)
# Add return to stockpile
#   Add automatic exchange_ with stockpile
#   Add choice to place inventory in stockpile   
#HP
# Implement attack
#Buildings
# Implement enter building
#
#
#Problem:
#  Look at ReceiveInput, CANCEL doesn't work, I don't think the min option works either. See SetUpExchange

import sys
import pygame
from pygame.locals import *
from random import randint
from entities import *
from actions import *
from terrains import *
from items import *
import all_names
from functions import *

"""

Game Parameters

"""
simple_map = [[2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 1, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 1, 1, 1],
              [2, 2, 0, 0, 1, 0, 1, 0, 1, 1],
              [2, 2, 0, 0, 0, 1, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1]]
current_map = simple_map
terr_length = 10

def main():

    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    #Initialise
    Entity_list = []
    Unit_list = []
    selection = []
    terr_list = []
    Resource_list = []
    Building_list = []
    Entity_HP_list = []

    #vals
    start_units = 3
    start_map_resources = 3
    unit_dist_from_you = 2
    res_dist_from_you = 2
    building_dist_from_you = 2

    #clock
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    #initial terrain(not used)
    for i in range(0, len(current_map)):
        current_row = current_map[i]
        for j in range(0, len(current_row)):
            terr = terrain([i*10, j*10],current_map[i][j], terr_length)
            terr.set_terr_parameters()
            terr_list.append(terr)

    #initial units
    #you
    unit_you = Unit([0,0], 10) #pos, intr_rang (default = 2)
    unit_you.name = 'You'
    unit_you.pos = [randint(0,100),randint(0,100)]
    Entity_list.append(unit_you)
    Unit_list.append(unit_you)
    #j others
    for i in range(0, start_units):
        #randomly placed aroung 'you'
        unit = Unit([unit_you.pos[0] + randint(-unit_dist_from_you, unit_dist_from_you),
                     unit_you.pos[1] + randint(-unit_dist_from_you, unit_dist_from_you)])
        Entity_list.append(unit)
        Unit_list.append(unit)

    #initial buildings #one hut one storage pile
    building_type_names = set_entity_type_names(2) #set random name for each type
    building1 = Building([unit_you.pos[0] + randint(-building_dist_from_you, building_dist_from_you),
                          unit_you.pos[1] + randint(-building_dist_from_you, building_dist_from_you)], 0) #pos, type
    building1.set_building_atributes(building_type_names)
    Entity_list.append(building1)
    Building_list.append(building1)
    building2 = Building([unit_you.pos[0] + randint(-building_dist_from_you, building_dist_from_you),
                          unit_you.pos[1] + randint(-building_dist_from_you, building_dist_from_you)], 1) #pos, type
    building2.set_building_atributes(building_type_names)
    Entity_list.append(building2)
    Building_list.append(building2)

    #set units default stockpile
    for unit in Unit_list:
        nearest_stockpile = unit.GetNearestStockpile(Building_list)
        unit.stockpile = nearest_stockpile

    #initial map resources
    res_type_names = set_entity_type_names(3) #set random name for each type
    for i in range(0, start_map_resources):
        #randomly placed aroung 'you'
        resource = Resource([unit_you.pos[0] + randint(-res_dist_from_you, res_dist_from_you),
                             unit_you.pos[1] + randint(-res_dist_from_you, res_dist_from_you)],
                            randint(0, 2),
                            1000) #pos, type, amount
        resource.set_res_atributes(res_type_names)
        Resource_list.append(resource)
        Entity_list.append(resource)

    #main menu
    main_menu()

    #main game loop
    while 1:

        #kill dead entities/remove depleted resources. Entities are marked as dead here but
        #not removed till the end of the loop so actions involving them are not interupted
        for entity in Entity_list:
            if isinstance(entity, Unit):
                if entity.HP <= 0:
                    entity.dead = True
                    print '{0} {1} died, they will not be fogotten'.format(type(entity).__name__, entity.name)
            if isinstance(entity, Building):
                if entity.HP <= 0:
                    entity.dead = True
                    print '{0} {1} was destroyed, we must rebuild'.format(type(entity).__name__, entity.name)
            elif isinstance(entity, Resource):
                if entity.amount <= 0:
                    entity.dead = True
                    print
                
        #do actions
        Entity_HP_list = []
        Entity_HP_list = Unit_list + Building_list
        for entity in Entity_HP_list:
            if entity.action == []:
                continue
            action_ = entity.action[0] #takes the first action, which is the current order 
            #attack
            if isinstance(action_, Attack):
                attack_ = action_
                attack_result = attack_.DoAttack()
                if attack_result == False: #target moved away
                    entity.MoveTo(attack_.target.pos, True) #pos, option. True means the action_list will be prepended not overidden
                elif attack_result == True: #target dead, delete attack
                    entity.action.remove(attack_)
                    del attack_
                else:
                    continue #attack cycle complete
            #collect
            elif isinstance(action_, Collect):
                collect_ = action_
                if collect_.DoCollect(res_type_names) == True: #true if inventory full or acter out of range
                    entity.action.remove(collect_) #remove if acters inventory is full or acter out of range
                    del collect_
                    #go back to stockpile when inventory full
                    entity.MoveTo(entity.stockpile.pos)
                    continue
            #movement
            elif isinstance(action_, Movement): 
                move_ = action_
                if move_.DoMove() == True: #do movement, true is destination reached
                    entity.action.remove(move_) #remove from action list if destination reached
                    del move_
            #exchange
            elif isinstance(action_, Exchange):
                exchange_ = action_
                if exchange_.MakeExchange() == False:
                    #false if something is wrong 
                    print 'Something is wrong with the exchange order you gave to {0}'.format(exchange_.acter)
                    if len(exchange_.item_list) != 1: #if all items were chosen need to change what is printed
                        print 'You asked them to give all of their items to {0} {1}'.format(type(exchange_.target).__name__,
                                                                                            exchange_.target.name)
                        print '{0} has the following items'.format(exchange_.acter.name)
                        display_inventory_atributes(exchange_.acter)    
                    else:
                        print 'You asked them to give {0} {1} to {2} {3}'.format(exchange_.item_amount_list[0], exchange_.item_list[0].name,
                                                                                 type(exchange_.target).__name__, exchange_.target.name)
                    print 'Resubmit choice coming soon. Cancelling exchange'
                else:
                    #exchange completed sucessfully
                    entity.action.remove(exchange_)
                    del exchange_
            else:
                print type(action_)
                print 'That action isnt implemented yet'
                entity.action.remove(action_)
                del action_

        #consolidate unit inventories, remove empty items
        for i in range(0, len(Entity_HP_list)):
            entity = Entity_HP_list[i]
            if entity.inventory == []:
                continue
            else:
                for j in range(0, len(entity.inventory)):
                    item = entity.inventory[j]
                    if item.amount <= 0:
                        #remove if the item is empty
                        entity.inventory.remove(item)
                        del item
                        break
                    for k in range(0, len(entity.inventory)):
                        other_item = entity.inventory[k]
                        if other_item == item:
                            Remove_item = False
                            continue
                        else:
                            if item.type_ == other_item.type_:
                                item.amount = item.amount + other_item.amount
                                entity.inventory.remove(other_item)
                                del other_item
                                Remove_item = True
                                break
                    if Remove_item == True: #this stops iterating over the second item when it has been removed and no longer exists
                        break
                                        
        #timing
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds > 60:
            minutes += 1
            seconds -= 60
        #text = time_font.render(('{}:{}'.format(minutes, seconds)), 1, BLACK) #text,antialiasing,colour
        #textpos = text.get_rect()
        #textpos.centerx = time_xpos
        #textpos.centery = time_ypos
        #screen.blit(text, textpos)
        milliseconds += clock.tick(60) #returns time since the last call, limits the frame rate to 60FPS

        #event loop
        for event in pygame.event.get():
            #quit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #button press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    #add Unit
                    unit = Unit([0,0])
                    Entity_list.append(unit)
                    Unit_list.append(unit)
                    print '{} created'.format(unit.name)
                if event.key == pygame.K_d:
                    #display entities
                    if len(Entity_list) == 0:
                        print 'There are no entites'
                        continue
                    print 'Entity List:'
                    print make_name_list(Entity_list)
                if event.key == pygame.K_s:
                    #select entity
                    if len(Entity_list) == 0:
                        print 'There are no entites'
                        continue
                    else:
                        selection = []
                        #name_list =  make_name_list(Entity_list) #remove if everything is working
                        choice = make_menu_choice('Select an entity', make_name_list(Entity_list))
                        if choice == False:
                            print 'Exited'
                            continue #continue with next event if user cancels
                        selection = Entity_list[choice-1]
                        print '{} selected'.format(selection.name)
                if event.key == pygame.K_o:
                    #modify atributes. this may be useful for quickly moving things for debugging
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    new_x = ReceiveInput('New x-coordinate:', 'Number')
                    if new_x == False:
                        print 'Exited'
                        continue #user cancels
                    new_y = ReceiveInput('New y-coordinate:', 'Number')
                    if new_y == False:
                        print 'Exited'
                        continue #user cancels
                    selection.pos = [new_x, new_y]
                if event.key == pygame.K_m:
                     #reprint main menu
                    main_menu()
                if event.key == pygame.K_u:
                    #unselect entity
                    selection = []
                    print 'Deselected'
                if event.key == pygame.K_t:
                    #display time
                    print '{}:{}'.format(minutes, seconds)
                if event.key == pygame.K_v:
                    #movement
                    while 1: #keeps looping till valid choice made
                        if selection == []:
                            print 'No Unit Selected'
                            break
                        else:
                            new_x = ReceiveInput('New x-coordinate:', 'Number') #string, option
                            #if new_x == False:
                            #    print 'Exited'
                            #    continue #user cancels
                            new_y = ReceiveInput('New y-xcoordinate:', 'Number')
                            #if new_y == False:
                            #    print 'Exited'
                            #    continue #user cancels
                            selection.MoveTo([new_x, new_y])
                            break #break while loop
                if event.key == pygame.K_l:
                    #list unit properties
                    display_unit_atributes(Unit_list)
                if event.key == pygame.K_r:
                    #list resource properties
                    display_resource_atributes(Resource_list)
                if event.key == pygame.K_b:
                    #list building properties
                    display_building_atributes(Building_list)
                if event.key == pygame.K_c:
                    #possible actions for unit 
                    entities_in_range = [] 
                    str_action_list = [] #string of possible actions
                    type_action_list =[]
                    if selection == []:
                        print 'No Unit Selected'
                        break
                    if type(selection) is Building or type(selection) is Resource:
                        print 'Building actions list coming soon'
                        continue
                    for entity in Entity_list: #distance between two points
                        #0 attack
                        #1 enter
                        #2 collect
                        #3 exchange inventory
                        if entity is selection:
                            continue 
                        dist_between = get_dist_between(entity, selection)                    
                        if dist_between < selection.intr_range:
                            if isinstance(entity, Building):
                                str_action_list.append('Enter Buidling {}: coming soon'.format(entity.name))
                                type_action_list.append(1) #1 for Enter (probably not necceassy as not very complex)
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
                    choice = make_menu_choice('Select an Action', str_action_list)
                    if choice == False:
                        print 'Exited'
                        continue #user cancels, continue looping over the next event
                    selected_entity = entities_in_range[choice - 1]
                    selected_action = type_action_list[choice - 1]
                    if selected_action == 0:
                        #attack
                        print '{0} will attack {1} {2}'.format(selection.name, type(selected_entity).__name__, selected_entity.name)
                        attack_ = Attack(selection, selected_entity)
                        selection.action = [attack_]
                    if selected_action == 1:
                        #enter
                        print 'coming soon,{0}'.format(selected_entity.name)
                    if selected_action == 2:
                        #unit collects resource
                        print '{}, Collect {} selected'.format(selected_action, selected_entity.name)                    
                        collect_ = Collect(selection, selected_entity) #acter, target
                        selection.action = [collect_]
                    if selected_action == 3:
                        #exchange inventory between entities
                        print '{}, Exchange inventory with {} selected'.format(selected_action, selected_entity.name)
                        exchange_underway = True
                        while exchange_underway: #while loop so user can cancel and go back a step
                            dir_choice = make_menu_choice('Choose Direction',['{0} to {1}'.format(selection.name, selected_entity.name),
                                                                              '{0} to {1}'.format(selected_entity.name, selection.name)])
                            if dir_choice == False:
                                print 'Exited'
                                break #leave the exchange if user exits
                            while True: #this loop allow the user to go back
                                str_item_list = [] #stores the names of the items
                                if dir_choice == 1:
                                    if SetUpExchange(selection, selected_entity) == True:
                                        exchange_underway = False #finished sucessfully, leave while loops
                                        break
                                    else:
                                        break #go back one step, but not all the way
                                if dir_choice == 2:
                                    if SetUpExchange(selected_entity, selection) == True:
                                        exchange_underway = False #finished sucessfully, leave while loops
                                        break
                                    else:
                                        break #go back one step, but not all the way

                if event.key == pygame.K_h:     
                    #print unit inventories
                    for i in range(0, len(Unit_list)):
                        print i
                        print unit.inventory
                if event.key == pygame.K_j:     
                    #print selections inventory
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    display_inventory_atributes(selection)
                if event.key == pygame.K_x:
                    #print selections action
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    selection.DisplayEntityAction()
                if event.key == pygame.K_q:
                    #exit
                    pygame.quit()
                    sys.exit()
        
        #remove dead entities
        for entity in Entity_list:
            if entity.dead == True:
                Entity_list.remove(entity)
                if isinstance(entity, Building):
                    Building_list.remove(entity)
                if isinstance(entity, Unit):
                    Unit_list.remove(entity)
                if isinstance(entity, Resource):
                    Resource_list.remove(entity)

main()







