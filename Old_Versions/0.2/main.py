#World RTS 2
#Version: 0.2
#
#Kevin Maguire
#11/08/14
#
#Notes:
# Interface will be multiple choice in terminal menus for now. Tables in ASCII if there are any.
# The game will have continuous coordinates and will not be based on a grid
# Every entity will have a positive grid coordinate(x,y) which increases right for x and down for y, as in pygame.
# Entities will include everything, units, buildings, resources. Except Terrain, which will be based on ranges. 
#
#Add:
# Orders
#  First do the movement mechanic(done)
#  Complex so do it with classes
#  Carried by people in their inventories
# Inventory
#  item classes held in an entity.inventory list
# Resources
#  map resource is an entity class, inventory resource is an item class
#  ability to collect resources (done)
#   action list(Done)
#    make sure you can only get action list for units, for now(done)
#   add to inventory (done)
#    make a new item instance in each run then make a section to consolidate unit inventories.(done)
#Collect
# Add inventory capacity, add return to stockpile, add choice to place inventory in stockpile   
# HP
#  Buildings and units have HP, resource entities dont
#  So I may need to have units and HP in their own entity subclass  
#  Might be the same for int_range
# Buildings
#  Made with random name for each type. MAke three types for now but only use one.(done)
#
#Problems:
# (fixed woo!)Inventory display is always the same, regardless of what unit is selected
#   All of the unit had the same copy of inventory so any change to inventory stuck to all unit.inventory atributes.
#   To fix you have to give each unit its own copy of inventory when the unit is initialized.


import sys
import pygame
from pygame.locals import *
from random import randint
from math import sqrt
from math import pow
from entities import *
from actions import *
from terrains import *
from items import *
import all_names

"""

Game Parameter

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
    action_list = []

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

        #Movements
        for i in range(0, len(Unit_list)):
            the_unit = Unit_list[i]
            if the_unit.destination == []:
                continue
            else:
                distance_per_cycle = the_unit.speed/60.0
                if the_unit.pos[0] == the_unit.destination[0]: #dont move in x dir if its already in line, then move in y dir
                    if the_unit.pos[1] == the_unit.destination[1]:
                        the_unit.destination = [] #destination reached
                        print "{} moved to {}".format(the_unit.name, the_unit.pos)
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
                    
        #do actions
        for l in range(0, len(action_list)):
            #collecting resources
            action_ = action_list[l]
            if type(action_) == Collect:
                collect_ = action_
                if get_dist_between(collect_.target, collect_.acter) > collect_.acter.intr_range:
                    action_list.remove(collect_) #remove if acter has moved too far away
                    del collect_
                    continue
                else:
                    collects_per_cycle = collect_.acter.collect_speed/60.0
                    collect_.target.amount = collect_.target.amount - collects_per_cycle
                    item = Item(collect_.target.type_, collects_per_cycle) #type, amount, name
                    item.set_item_atributes(res_type_names)
                    collect_.acter.inventory.append(item)

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
        #text = time_font.render(("{}:{}".format(minutes, seconds)), 1, BLACK) #text,antialiasing,colour
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
                    print "{} created".format(unit.name)
                if event.key == pygame.K_d:
                    #display entities
                    if len(Entity_list) == 0:
                        print "There are no entites"
                        continue
                    print "Entity List:"
                    print make_name_list(Entity_list)
                if event.key == pygame.K_s:
                    #select entity
                    if len(Entity_list) == 0:
                        print "There are no entites"
                        continue
                    else:
                        selection = []
                        name_list = make_name_list(Entity_list)
                        choice = make_menu_choice("Select an entity", name_list)
                        selection = Entity_list[choice-1]
                        print "{} selected".format(selection.name)
                if event.key == pygame.K_p:
                    #display entity atributes
                    if selection == []:
                        print "No Entity Selected"
                        continue
                    print "{}'s position is {}".format(selection.name, selection.pos)
                if event.key == pygame.K_o:
                    #modify atributes
                    if selection == []:
                        print "No Entity Selected"
                        continue
                    new_x = input("New x-coordinate:  ")
                    new_y = input("New y-coordinate:  ")
                    selection.pos = [new_x, new_y]
                if event.key == pygame.K_m:
                     #reprint main menu
                    main_menu()
                if event.key == pygame.K_u:
                    #unselect entity
                    selection = []
                    print "Deselected"
                if event.key == pygame.K_t:
                    #display time
                    print "{}:{}".format(minutes, seconds)
                if event.key == pygame.K_v:
                    #movement
                    while 1: #keeps looping till valid choice made
                        if selection == []:
                            print "No Unit Selected"
                            break
                        try:
                            new_x = input("New x-coordinate:  ")
                            new_y = input("New y-coordinate:  ")
                        except NameError:
                            print "invalid Choice"
                        except SyntaxError:
                            print "invalid Choice"
                        else:
                            selection.destination = [new_x, new_y]
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
                        print "No Unit Selected"
                        break
                    if type(selection) is Building or type(selection) is Resource:
                        print "Building actions list coming soon"
                        continue
                    for entity in Entity_list: #distance between two points
                        dist_between = get_dist_between(entity, selection)                    
                        if dist_between < selection.intr_range:
                            entities_in_range.append(entity)
                            if type(entity) is Unit:
                                str_action_list.append("Attack {}, coming soon".format(entity.name))
                                type_action_list.append(0) #0 for attack
                            if type(entity) is Building:
                                str_action_list.append("Enter Buidling {}: coming soon".format(entity.name))
                                type_action_list.append(1) #1 for Enter (probably not necceassy as not very complex)
                            if type(entity) is Resource:
                                str_action_list.append("Collect {}".format(entity.name))
                                type_action_list.append(2) #2 for collection            
                    choice = make_menu_choice("Select an Action", str_action_list)
                    selected_entity = entities_in_range[choice - 1]
                    selected_action = type_action_list[choice - 1]
                    if selected_action == 0:
                        print "coming soon"
                    if selected_action == 1:
                        print "coming soon"
                    if selected_action == 2:
                        print "{}, Collect {} selected".format(selected_action, selected_entity.name)                    
                        collect_ = Collect(selection, selected_entity) #acter, target
                        action_list.append(collect_) 
                        #selection.UpdateAction()
                if event.key == pygame.K_y:     
                    #print action list
                    print action_list
                if event.key == pygame.K_h:     
                    #print unit inventories
                    for i in range(0, len(Unit_list)):
                        print i
                        print unit.inventory
                if event.key == pygame.K_j:     
                    #print selections inventory
                    if selection == []:
                        print "No Entity Selected"
                        continue
                    display_inventory_atributes(selection)
                if event.key == pygame.K_q:
                    #exit
                    pygame.quit()
                    sys.exit()

def make_menu_choice(*strs):
    #menu with built in choice
    print "-----------------------------------------"
    print strs[0]
    for i in range(0,len(strs[1])):
        print "{}) {}".format(i+1, strs[1][i])
    print "----------------------------------------"
    while 1:
        try:
            choice = int(input("> "))
        except NameError:
            print "Invalid Choice"
        except SyntaxError:
            print "Invalid Choice"
        else:
            if choice > len(strs[1]) or choice < 1:
                print "Invalid Choice"
            else:
                return choice
    
def make_menu(*strs):
    #menu with no built in choice and specified associated keys
    print "-----------------------------------------"
    print strs[0]
    for i in range(0,len(strs[1])):
        print "{}) {}".format(strs[1][i], strs[2][i])
    print "----------------------------------------"
    
def make_name_list(Entity_list):
    #make list of entity names
    name_list = []
    for i in range(0, len(Entity_list)):
        name_list.append(Entity_list[i].name)
    return name_list

def get_dist_between(entity1, entity2):
    dist_between = sqrt(pow(entity1.pos[0] - entity2.pos[0], 2) + pow(entity1.pos[1] - entity2.pos[1], 2))
    return dist_between

#not used
#def make_pos_list(Entity_list):
#    #make list of entity positionss
#    pos_list = []
#    for i in range(0, len(Entity_list)):
#        pos_list.append(Entity_list[i].pos)
#    return pos_list

#not used
#def make_dest_list(Entity_list):
#    #make list of entity destinations
#    dest_list = []
#    for i in range(0, len(Entity_list)):
#        dest_list.append(Entity_list[i].destination)
#    return dest_list

#not used
#def make_type_list(Entity_list):
#    #make list of entity type
#    type_list = []
#    for i in range(0, len(Entity_list)):
#        type_list.append(Entity_list[i].type_)
#    return type_list

#not used
#def make_amount_list(Entity_list):
#    #make list of entity amounts
#    amount_list = []
#    for i in range(0, len(Entity_list)):
#        amount_list.append(Entity_list[i].type_)
#    return amount_list

def main_menu():
    make_menu("What would you like to do?",["a", "d", "s", "p", "o", "m", "u", "t","v", "l","r","b","c","j","q"], ["Add Unit",
                                                                                                                   "Display Entities",
                                                                                                                   "Select Entity",
                                                                                                                   "Display entity atributes",
                                                                                                                   "Modify Entity Atributes",
                                                                                                                   "Display Menu", 
                                                                                                                   "Unselect Entity",
                                                                                                                   "Display Time",
                                                                                                                   "Move Unit",
                                                                                                                   "Display List",
                                                                                                                   "Display Resources",
                                                                                                                   "Display Buildings",
                                                                                                                   "Do Action",
                                                                                                                   "Display Items",
                                                                                                                   "Quit"])
    

main()







