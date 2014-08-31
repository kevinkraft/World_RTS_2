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
# Resources
# Terrain(donr)
#  Will be based on ranges(done)
#  will be defined by a matrix(done)
# Expand entity class
# Movement
#  each unit will have a move list, each cycle the unit will be moved to the next point on its list of moves,
#  or wont be moved at all if its list is empty. No need to use classes for a move.
#  Need to write algorithm to pick best route

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
    order_list = []
    terr_list = []
   
    #vals
    start_units = 0

    #clock
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    #initial terrain
    for i in range(0, len(current_map)):
        current_row = current_map[i]
        for j in range(0, len(current_row)):
            terr = terrains.terrain([i*10, j*10],current_map[i][j], terr_length)
            terr.set_terr_parameters()
            terr_list.append(terr)
    

#######################################################################
#old Broken method
########################################################################
 #   #initial terrain
 #   terr_pos = [0, 0]
 #   for row in current_map:
 #       #print make_type_list(terr_list)
 #       #print terr_list
 #       terr_pos[0] = 0
 #       for terr_type in row:
 #           terr = terrains.terrain(terr_pos, terr_type, terr_length)
 #           terr.set_terr_parameters()
 #           terr_list.append(terr)
 #           #print terr.type
 #           terr_pos[0] = terr_pos[0] + terr_length
 #       terr_pos[1] = terr_pos[1] + terr_length
###########################################################################

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
        
    #main game loop
    while 1:

        #main menu
        main_menu()


        while 1:

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
            milliseconds += clock.tick_busy_loop() #returns time since the last call, limits the frame rate to 60FPS

            #event loop
            for event in pygame.event.get():
                #quit game
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                    #button press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        #add Unit
                        unit = entities.Unit([0,0])
                        Entity_list.append(unit)
                        Unit_list.append(entity)
                        print "{} created".format(unit.name)
                    if event.key == pygame.K_2:
                        #display entities
                        if len(Entity_list) == 0:
                            print "There are no entites"
                            break
                        print "Entity List:"
                        print make_name_list(Entity_list)
                    if event.key == pygame.K_3:
                        #select entity
                        if len(Entity_list) == 0:
                            print "There are no entites"
                            break
                        else:
                            name_list = make_name_list(Entity_list)
                            choice = make_menu_choice("Select an entity", name_list)
                            selection = Entity_list[choice-1]
                            print "{} selected".format(selection.name)
                    if event.key == pygame.K_4:
                        #display entity atributes
                        if selection == []:
                            print "No Entity Selected"
                            break
                        print "{}'s position is {}".format(selection.name, selection.pos)
                    if event.key == pygame.K_5:
                        #modify atributes
                        if selection == []:
                            print "No Entity Selected"
                            break
                        new_x = input("New x-coordinate:  ")
                        new_y = input("New y-coordinate:  ")
                        selection.pos = [new_x, new_y]
                    if event.key == pygame.K_6:
                        #reprint main menu
                        main_menu()
                    if event.key == pygame.K_7:
                        #unselect entity
                        selection = []
                        print "Deselected"
                    if event.key == pygame.K_8:
                        #display time
                        print "{}:{}".format(minutes, seconds)
                    if event.key == pygame.K_9:
                        #movement
                        if selection == []:
                            print "No Unit Selected"
                            break
                        new_x = input("New x-coordinate:  ")
                        new_y = input("New y-coordinate:  ")
                        selection.move_unit([new_x,new_y]) #([destination])
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
    #menu with no built in choice
    print "-----------------------------------------"
    print strs[0]
    for i in range(0,len(strs[1])):
        print "{}) {}".format(i+1, strs[1][i])
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
    #make list of entity positionss
    type_list = []
    for i in range(0, len(Entity_list)):
        type_list.append(Entity_list[i].type)
    return type_list

def main_menu():
    make_menu("What would you like to do?",["Add Unit", "Display Entities", "Select Entity", "Display entity atributes"
                                            ,"Modify Entity Atributes","Display Menu","Unselect Entity","Display Time","Move Unit","Q: Quit"])



main()







