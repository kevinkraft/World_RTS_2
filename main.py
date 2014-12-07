#World RTS 2
#Version: 0.4
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
#  Section to allow You to give orders
#Add build building
#Procreate
#  This action creates a baby which must be cared for by someone unless it dies and must also be brought food
#    Add the above feture
#I NEED TO SORT OUT MODULE NAMES FOR ACTIONS, MAKE EVERYTHING EASY TO UNDERSTAND AND HAVE THE SAME NAMES
#  Need some or all of the following modules for each action:
#    Setup(user interface setup), action_.Do(do now, basic), action_.MakeOrder(do later, extra options), Automatic(depends on whats needed)   
#
#Problem: There are too many messages being displayed

import sys
import pygame
from pygame.locals import *
from random import randint
from config import *
from entities import *
from actions import *
from terrains import *
from items import *
import all_names
from functions import *

"""

Main fuction. Do python main.py to run game

"""

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
    Entity_HP_list = [] #this is filled in each loop

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
    unit_you = Unit([0,0], intr_range = 10) #pos, intr_range (default = 2)
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
    for j in range(0, start_food_resources):
        resource = Resource([unit_you.pos[0] + randint(-res_dist_from_you + res_dist_factor*j, res_dist_from_you + res_dist_factor*j),
                             unit_you.pos[1] + randint(-res_dist_from_you  + res_dist_factor*j, res_dist_from_you + res_dist_factor*j)],
                            0,
                            1000) #pos, type, amount
        resource.set_res_atributes(res_type_names)
        Resource_list.append(resource)
        Entity_list.append(resource)
    for i in range(0, start_random_map_resources):
        #randomly placed aroung 'you'
        resource = Resource([unit_you.pos[0] + randint(-res_dist_from_you + res_dist_factor*i, res_dist_from_you + res_dist_factor*i),
                             unit_you.pos[1] + randint(-res_dist_from_you + res_dist_factor*i, res_dist_from_you + res_dist_factor*i)],
                            randint(1, 2),
                            1000) #pos, type, amount
        resource.set_res_atributes(res_type_names)
        Resource_list.append(resource)
        Entity_list.append(resource)

    #main menu
    main_menu()

    #main game loop
    while 1:

        #control hunger
        #Decrease Hunger, take damage if hunger is zero
        for unit in Unit_list:
            unit.hunger = unit.hunger - hunger_per_cycle
            if unit.hunger <= 0:
                unit.hunger = 0
                unit.HP = unit.HP - hunger_per_cycle_damage
                if int(unit.HP) % 5 == 0: #print when HP on even number
                    print '{0} {1} is starving to death'.format(type(unit).__name__, unit.name)
            if unit.hunger <= 50:
                eat_order = False
                for action_ in unit.action: #if the unit already has an eat order then dont add one
                    if isinstance(action_, Eat):
                        eat_order = True
                if eat_order == False:
                    eat_ = Eat(unit) #go and eat
                    unit.action.insert(0, eat_)
            
        #kill dead entities/remove depleted resources. Entities are marked as dead here but
        #not removed till the end of the loop so actions involving them are not interupted
        for entity in Entity_list:
            if isinstance(entity, Unit):
                if entity.HP <= 0:
                    entity.dead = True
                    print '{0} {1} died, they will not be forgotten'.format(type(entity).__name__, entity.name)
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
                    attack_.DeleteAction()
                else:
                    continue #attack cycle complete
            #collect
            elif isinstance(action_, Collect):
                collect_ = action_
                collect_result = collect_.DoCollect(res_type_names)
                if  collect_result == True: #true if inventory full
                    if collect_.return_to_stockpile == True:
                        #go back to stockpile when inventory full
                        entity.MoveTo(collect_.target.pos, True) #add return to target to keep collecting
                        collect_.AutomaticCollectExchange() #add exchange with stockpile
                        entity.MoveTo(entity.stockpile.pos, True) #add move to stockpile
                        continue
                    else: #done return to stockpile for whatever reason
                        collect_.DeleteAction()
                elif collect_result == None: #out of range
                    collect_.DeleteAction()
                    continue
            #movement
            elif isinstance(action_, Movement): 
                move_ = action_
                if move_.DoMove() == True: #do movement, true is destination reached
                    move_.DeleteAction()
            #exchange
            elif isinstance(action_, Exchange):
                exchange_ = action_
                exchange_.MakeOrderExchange()
            #Enter
            elif isinstance(action_, Enter):
                enter_ = action_
                enter_.DoEnter()
            #Procreate
            elif isinstance(action_, Procreate):
                procreate_ = action_
                new_entity = procreate_.DoProcreate()
                Entity_list.append(new_entity)
                Unit_list.append(new_entity)
            #Eat
            elif isinstance(action_, Eat):
                eat_ = action_
                eat_.DoEat(Resource_list)
            else:
                print type(action_)
                print 'That action isnt implemented yet'
                action_.DeleteAction()

        #consolidate unit inventories, remove empty items
        ConsolidateInventories(Entity_HP_list)
                                        
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
                if event.key == pygame.K_s:
                    #select entity
                    selection = SelectEntity(Entity_list)
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
                if event.key == pygame.K_d:
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
                        print 'Buildings and Resource actions list coming soon'
                        continue
                    for entity in Entity_list: #distance between two points
                        #0 attack
                        #1 enter
                        #2 collect
                        #3 exchange inventory
                        #4 Procreate
                        if entity is selection:
                            continue 
                        dist_between = get_dist_between(entity, selection)                    
                        if dist_between < selection.intr_range:
                            if isinstance(entity, Building):
                                str_action_list.append('Enter Buidling {}'.format(entity.name))
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
                            if isinstance(entity, Unit):
                                str_action_list.append('Procreate with {0} {1} {2}'.format(entity.gender, type(entity).__name__, entity.name))
                                type_action_list.append(4) #4 for procreate
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
                        MakeEnterOrder(selection, selected_entity)
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
                    if selected_action == 4:
                        #procreate
                        SetupProcreate(selection, selected_entity)                        
                if event.key == pygame.K_h:     
                    #print unit inventories
                    for i in range(0, len(Unit_list)):
                        print i
                        print unit.inventory
                if event.key == pygame.K_i:     
                    #print selections inventory
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    display_inventory_atributes(selection)
                if event.key == pygame.K_g:     
                    #print selected buildings unit inventory
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    if not isinstance(selection, Building):
                        print 'Only buildings can have garrisons'
                        continue
                    selection.DisplayGarrison()
                if event.key == pygame.K_l:
                    print 'Unit_list[0].action:'
                    print Unit_list[0].action
                    print "--------------------------------------------------------------------"
                    for unit in Unit_list: 
                        unit.DisplayEntityAction()
                    print "--------------------------------------------------------------------"
                if event.key == pygame.K_x:
                    #cancel action
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    for action_ in selection.action:
                        action_.DeleteAction()
                    selection.action = []
                    print 'All {0} {1} actions cancelled'.format(type(selection).__name__, selection.name)
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







