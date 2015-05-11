import sys, os
import pygame
from pygame.locals import *
from config import *
from entities import *
from terrains import *
from random import randint
from graphics import *
from managers import *

"""

Contains function to set up the initial game parameters

"""

def Initialize():

    #initialize pygame
    pygame.init()

    #set terminal size
    os.system('resize -s {1} {0}'.format(terminal_width, terminal_height))

    #initialise screen
    screenSet = MakeScreen()

    #Initialise containers
    Entity_list = []
    Unit_list = []
    selection = []
    terr_list = []
    Resource_list = []
    Building_list = []
    Entity_HP_list = [] #this is filled in each loop
    
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
    #unit_you.pos = [randint(0,100),randint(0,100)]
    #unit_you.pos = [screen_width/2, screen_height/2]
    unit_you.pos = [0, 0] #game coords
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
    building_type_names = set_entity_type_names(3) #set random name for each type
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

    #initial resources in stockpile
    initial_wood = Item(1,75) #type, amount
    initial_wood.set_item_atributes(res_type_names)
    Building_list[1].inventory = [initial_wood]

    #construction list is empty at this stage
    Entity_Action_list = Unit_list + Building_list
    Construction_list = []

    #make game manager
    GM = GameManager(screenSet, Entity_list, Unit_list, selection, terr_list, Resource_list, Building_list, Entity_HP_list,
                     Entity_Action_list, Construction_list, building_type_names, res_type_names)

    #update the screen
    UpdateScreen(GM, []) #GM, selection

    return screenSet, Entity_list, Unit_list, selection, terr_list, Resource_list, Building_list, Entity_HP_list, Entity_Action_list, Construction_list, building_type_names, res_type_names, GM

def StartClock():
    #clock
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    return clock, minutes, seconds, milliseconds

