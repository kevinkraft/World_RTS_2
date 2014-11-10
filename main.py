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
#  Unit will have an action artibute to contain current action
#  Unit will have an order list, when an action is finished the first item in order will become the action
#  So an order will be a series of actions in a list
#Actions
# Add movement to actions(done)
#   Complete overhaul
#     Movement will be an action, with an acter and destination(done)
#     Will need a separate class to inplement this(done)
#     need to remove the destination atribute of a unit(still going to use it)
#     The unit will have an action which contains the action class instance to be done (done)
# Add inventory capacity (done)
# Add return to stockpile
# Add choice to place inventory in stockpile   
#HP
# Implement attack
#Buildings
# Implement enter building

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
    Order_list = []
    terr_list = []
    Resource_list = []
    Building_list = []

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
                    
        #do actions
        for unit in Unit_list:
            if unit.action == []:
                continue
            action_ = unit.action[0] #takes the first action, which is the current order 
            #collecting resources
            if isinstance(action_, Collect):
                collect_ = action_
                if collect_.DoCollect(res_type_names) == True: #true if inventory full or acter out of range
                    unit.action.remove(collect_) #remove if acters inventory is full or acter out of range
                    del collect_
                    #go back to stockpile when inventory full
                    unit.MoveTo(unit.stockpile.pos)
                    continue
                    
            #movements
            elif isinstance(action_, Movement): 
                move_ = action_
                if move_.DoMove() == True: #do movement, true is destination reached
                    unit.action.remove(move_) #remove from action list if destination reached
                    del move_
            else:
                print type(action_)
                print 'That action isnt implemented yet'
                unit.action.remove(action_)
                del action_

        #consolidate unit inventories
        for i in range(0, len(Unit_list)):
            unit = Unit_list[i]
            if unit.inventory == []:
                continue
            else:
                for j in range(0, len(unit.inventory)):
                    item = unit.inventory[j]
                    for k in range(0, len(unit.inventory)):
                        other_item = unit.inventory[k]
                        if other_item == item:
                            Remove_item = False
                            continue
                        else:
                            if item.type_ == other_item.type_:
                                item.amount = item.amount + other_item.amount
                                unit.inventory.remove(other_item)
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
                            continue #continue with next event if user cancels
                        selection = Entity_list[choice-1]
                        print '{} selected'.format(selection.name)
                if event.key == pygame.K_o:
                    #modify atributes. this may be useful for quickly moving things for debugging
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    new_x = ReceiveInput('New x-coordinate:', 'Number')
                    new_y = ReceiveInput('New y-coordinate:', 'Number')
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
                            new_y = ReceiveInput('New y-xcoordinate:', 'Number')
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
                            entities_in_range.append(entity)
                            if type(entity) is Unit or Building:
                                str_action_list.append('Switch inventory with {} {}: coming soon'.format(type(entity).__name__, entity.name))
                                type_action_list.append(3) #3 for exchange inventory                                
                            if type(entity) is Unit:
                                str_action_list.append('Attack {}, coming soon'.format(entity.name))
                                type_action_list.append(0) #0 for attack
                            if type(entity) is Building:
                                str_action_list.append('Enter Buidling {}: coming soon'.format(entity.name))
                                type_action_list.append(1) #1 for Enter (probably not necceassy as not very complex)
                                str_action_list.append('Switch inventory with Buidling {}: coming soon'.format(entity.name))
                                type_action_list.append(3) #3 for exchange inventory
                            if type(entity) is Resource:
                                str_action_list.append('Collect {}'.format(entity.name))
                                type_action_list.append(2) #2 for collection            
                    choice = make_menu_choice('Select an Action', str_action_list)
                    if choice == False:
                        continue #user cancels, continue looping over the next event
                    selected_entity = entities_in_range[choice - 1]
                    selected_action = type_action_list[choice - 1]
                    if selected_action == 0:
                        print 'coming soon'
                    if selected_action == 1:
                        print 'coming soon'
                    if selected_action == 2:
                        print '{}, Collect {} selected'.format(selected_action, selected_entity.name)                    
                        collect_ = Collect(selection, selected_entity) #acter, target
                        selection.action = [collect_]
                    if selected_action == 3:
                        print '{}, Exchange inventory with {} selected'.format(selected_action, selected_entity.name)
                        
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
                if event.key == pygame.K_q:
                    #exit
                    pygame.quit()
                    sys.exit()

main()







