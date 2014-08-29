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
# Terain
#  Will be based on ranges
# Expand entity class

import sys
import entities
import terrain
import pygame
from pygame.locals import *
import all_names
from random import randint

def main():

    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    #Initialise
    Entity_list = []
    selection = []
    order_list = []
    
    #vals
    start_entities = 3

    #clock
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    #initial terrain
    terr = terrain.Terrain([10, 10], 1)
    

    #initial entities
    #you
    entity_you = entities.Entity([0,0])
    entity_you.name = 'You'
    entity_you.pos = [randint(0,100),randint(0,100)]
    Entity_list.append(entity_you)
    #j others
    for i in range(0, start_entities):
        #randomly placed aroung 'you'
        entity = entities.Entity([entity_you.pos[0] + randint(-10, 10), entity_you.pos[0] + randint(-10, 10)])
        Entity_list.append(entity)
        
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

def main_menu():
    make_menu("What would you like to do?",["Add Entity", "Display Entities", "Select Entity", "Display entity atributes"
                                            ,"Modify Entity Atributes","Display Menu","Unselect Entity","Display Time","Quit"])



main()







