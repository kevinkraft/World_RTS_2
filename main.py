#World RTS 2
#Version: 0.0
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
# Modify atrributes
#
#Problem:
# You have to click into the pygame window to make the keyp resses work. Kinda ruins the whole point. If you make it really small it can't be
#  seen(fixed)

import sys
import entities
import pygame
from pygame.locals import *
import names

def main():

    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    Entity_list = []
    select_coords = False
    selection = []

    #main game loop
    while 1:

        #main menu
        make_menu("What would you like to do?",["Add Entity", "Display Entities", "Select Entity", "Display entity atributes"
                                                ,"Modify Entity Atributes","Display Menu","Unselect Entity","Quit"])

        while 1:

            #event loop
            for event in pygame.event.get():
                #quit game
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                    #button press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        #add Entity
                        entity = entities.Entity([0,0])
                        Entity_list.append(entity)
                        print "{} created".format(entity.name)
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
                        print "Entity position is:"
                        print selection.pos
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
                        make_menu("What would you like to do?",["Add Entity", "Display Entities", "Select Entity", "Display entity atributes"
                                                                ,"Modify Entity Atributes","Display Menu","Quit"])
                    if event.key == pygame.K_7:
                        #unselect entity
                        selection = []
                        print "Deselected"
                    if event.key == pygame.K_8:
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


main()







