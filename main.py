#World RTS 2
#Version: 0.1
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
# Select Entity(done)
# default menu function(done)
# Display entity atributes(done)
#  Add More atributes
# Modify atrributes(done)
# Orders
#  First do the movement mechanic
#  Complex so do it with classes
#  Carried by people in their inventories
# Inventory
#  item classes held in an entity.inventory list
# Resources
#  map resource is an entity class, inventory resource is an item class
# Terrain(done)
#  Will be based on ranges(done)
#  will be defined by a matrix(done)
# Expand entity class(done)
# Movement(done)
#  Too complicated. Forget terrain. I'll just do really simple movemnt for now.
#   just move the position by a little bit towards the destination each iteration. The size of the move of course depends on the speed.
#   Moves in x dir first then y dir
#  each unit will have a move list, each cycle the unit will be moved to the next point on its list of moves,(no)
#  or wont be moved at all if its list is empty. No need to use classes for a move.(no)
#  Need to write algorithm to pick best route(no)
# Useful display(done)
# HP
#  Buildings and units have HP, resource entities dont
#  So I may need to have units and HP in their own entity subclass  
#  Might be the same for int_range
#
#Problem:
# Can only move 'you' can't move any of the other units

import sys
import entities
import terrains
import pygame
from pygame.locals import *
import all_names
from random import randint

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


    #vals
    start_units = 1
    start_map_resources = 3

    #clock
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    #initial terrain(not used)
    for i in range(0, len(current_map)):
        current_row = current_map[i]
        for j in range(0, len(current_row)):
            terr = terrains.terrain([i*10, j*10],current_map[i][j], terr_length)
            terr.set_terr_parameters()
            terr_list.append(terr)

    #initial units
    #you
    unit_you = entities.Unit([0,0])
    unit_you.name = 'You'
    unit_you.pos = [randint(0,100),randint(0,100)]
    Entity_list.append(unit_you)
    Unit_list.append(unit_you)
    #j others
    for i in range(0, start_units):
        #randomly placed aroung 'you'
        unit = entities.Unit([unit_you.pos[0] + randint(-10, 10), unit_you.pos[0] + randint(-10, 10)])
        Entity_list.append(unit)
        Unit_list.append(unit)
    print Unit_list
    print "Unit_list[1].destination"
    print Unit_list[1].destination

        
    #initial map resources
    res_type_names = entities.set_res_type_names()
    for i in range(0, start_map_resources):
        #randomly placed aroung 'you'
        resource = entities.Resource([unit_you.pos[0] + randint(-50, 50), unit_you.pos[0] + randint(-50, 50)],
                                     randint(0, 2),
                                     1000) #pos, type, amount
        resource.set_res_atributes(res_type_names)
        Resource_list.append(resource)


    #main game loop
    while 1:

        #main menu
        main_menu()


        while 1:

            #Movements
            for unit in Unit_list:
                print unit.destination
                print unit.name
                if unit.destination == []:
                    break
                else:
                    print "in movement cycle"
                    distance_per_cycle = unit.speed/60.0
                    if unit.pos[0] == unit.destination[0]: #dont move in x dir if its already in line, then move in y dir
                        if unit.pos[1] == unit.destination[1]:
                            unit.destination = [] #destination reached
                        elif abs(unit.pos[1] - unit.destination[1]) < distance_per_cycle: #last step in y
                            unit.pos[1] = unit.destination[1]
                        elif unit.pos[1] < unit.destination[1]:
                            unit.pos[1] = unit.pos[1] + distance_per_cycle
                        elif unit.pos[1] > unit.destination[1]:
                            unit.pos[1] = unit.pos[1] - distance_per_cycle
                    elif abs(unit.pos[0] - unit.destination[0]) < distance_per_cycle: #reach x destination if less than one cycle distance away
                        unit.pos[0] = unit.destination[0]
                    elif unit.pos[0] < unit.destination[0]:
                        unit.pos[0] = unit.pos[0] + distance_per_cycle
                    elif unit.pos[0] > unit.destination[0]:
                        unit.pos[0] = unit.pos[0] - distance_per_cycle
                    print "{} moved to {}".format(unit.name, unit.pos)

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
                        unit = entities.Unit([0,0])
                        Entity_list.append(unit)
                        Unit_list.append(unit)
                        print "{} created".format(unit.name)
                    if event.key == pygame.K_d:
                        #display entities
                        if len(Entity_list) == 0:
                            print "There are no entites"
                            break
                        print "Entity List:"
                        print make_name_list(Entity_list)
                    if event.key == pygame.K_s:
                        #select entity
                        if len(Entity_list) == 0:
                            print "There are no entites"
                            break
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
                            break
                        print "{}'s position is {}".format(selection.name, selection.pos)
                    if event.key == pygame.K_o:
                        #modify atributes
                        if selection == []:
                            print "No Entity Selected"
                            break
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
                        if selection == []:
                            print "No Unit Selected"
                            break
                        new_x = input("New x-coordinate:  ")
                        new_y = input("New y-coordinate:  ")
                        selection.destination = [new_x, new_y]
                        print "Unit_list[1].destination"
                        print Unit_list[1].destination
                    if event.key == pygame.K_l:
                        unit_name_list = make_name_list(Unit_list)
                        unit_pos_list = make_pos_list(Unit_list)
                        print "-----------------------------------------------------------------------------------------------------"
                        print "|  name  |  position  |"
                        print "-----------------------------------------------------------------------------------------------------"
                        print "-----------------------------------------------------------------------------------------------------"
                        for unit in Unit_list:
                            unit.display_unit_atributes()
                    if event.key == pygame.K_r:
                        res_name_list = make_name_list(Resource_list)
                        res_type_list = make_type_list(Resource_list)
                        res_name_list = make_name_list(Resource_list)
                        res_amount_list = make_amount_list(Resource_list)
                        print "-----------------------------------------------------------------------------------------------------"
                        print "|  name  |  position  |  type  |  amount  |"
                        print "-----------------------------------------------------------------------------------------------------"
                        print "-----------------------------------------------------------------------------------------------------"
                        for resource in Resource_list:
                            resource.display_resource_atributes()

                    if event.key == pygame.K_q:
                        #exit
                        pygame.quit()
                        sys.exit()

                    break

            
                

def make_menu_choice(*strs):
    #menu with build in choice
    print "-----------------------------------------"
    print strs[0]
    for i in range(0,len(strs[1])):
        print "{}) {}".format(i+1, strs[1][i])
    print "----------------------------------------"
    choice = input("> ")
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

def make_pos_list(Entity_list):
    #make list of entity positionss
    pos_list = []
    for i in range(0, len(Entity_list)):
        pos_list.append(Entity_list[i].pos)
    return pos_list

def make_type_list(Entity_list):
    #make list of entity type
    type_list = []
    for i in range(0, len(Entity_list)):
        type_list.append(Entity_list[i].type)
    return type_list

def make_amount_list(Entity_list):
    #make list of entity amounts
    amount_list = []
    for i in range(0, len(Entity_list)):
        amount_list.append(Entity_list[i].type)
    return amount_list

def main_menu():
    make_menu("What would you like to do?",["a", "d", "s", "p", "o", "m", "u", "t","v", "l","r","q"], ["Add Unit",
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
                                                                                                       "Quit"])
    

main()







