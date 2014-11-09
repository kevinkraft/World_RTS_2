import sys
import pygame
from pygame.locals import *
from math import sqrt, pow

"""

Some useful functions for all parts of the game

"""

#-------------------------------------------------------------------
# Inputs
#-------------------------------------------------------------------

def ReceiveInput(string, option = '', min_ = False, max_ = False):
    #get keyboard input, handle invalid choices
    while True:
        try:
            val = input(str(string+' '))
        except NameError:
            print 'invalid Choice'
            continue
        except SyntaxError:
            print 'invalid Choice'
            continue
        if option == 'Number':
            if isinstance(val, (int, long, float)) == False:
                print 'Choice must be a number'
                continue
            if min_ != False:
                if val < min_:
                    print 'Choice must be bigger than {}'.format(min_)
                    continue
            if max_ != False:
                if val > max_:
                    print 'Choice must be smaller than {}'.format(max_)
                    continue
        elif option == 'String':
            if type(val) is not string:
                print 'Choice must be a string'
                continue
        return val

#-------------------------------------------------------------------
# Menus
#-------------------------------------------------------------------

def make_menu_choice(*strs):
    #menu with built in choice
    print '-----------------------------------------'
    print strs[0]
    for i in range(0,len(strs[1])):
        print '{}) {}'.format(i+1, strs[1][i])
    print '{}) Cancel'.format(len(strs[1]) + 1) 
    print '----------------------------------------'
    choice = ReceiveInput('>', 'Number', 1, len(strs[1]) + 1)
    if choice == len(strs[1]) + 1:
        return False
    else:
        return choice
   
def make_menu(*strs):
    #menu with no built in choice and specified associated keys
    print '-----------------------------------------'
    print strs[0]
    for i in range(0,len(strs[1])):
        print '{}) {}'.format(strs[1][i], strs[2][i])
    print '----------------------------------------'

def main_menu():
    make_menu('What would you like to do?',['a', 'd', 's', 'o', 'm', 'u', 't','v', 'l','r','b','c','j','q'], ['Add Unit',
                                                                                                              'Display Entities',
                                                                                                              'Select Entity',
                                                                                                              'Modify Entity Atributes',
                                                                                                              'Display Menu', 
                                                                                                              'Unselect Entity',
                                                                                                              'Display Time',
                                                                                                              'Move Unit',
                                                                                                              'Display List',
                                                                                                              'Display Resources',
                                                                                                              'Display Buildings',
                                                                                                              'Do Action',
                                                                                                              'Display Items',
                                                                                                              'Quit'])
    
#-------------------------------------------------------------------
# Maths
#-------------------------------------------------------------------

def get_dist_between(entity1, entity2):
    dist_between = sqrt(pow(entity1.pos[0] - entity2.pos[0], 2) + pow(entity1.pos[1] - entity2.pos[1], 2))
    return dist_between

#-------------------------------------------------------------------
# Others
#-------------------------------------------------------------------

def make_name_list(Entity_list):
    #make list of entity names
    name_list = []
    for i in range(0, len(Entity_list)):
        name_list.append(Entity_list[i].name)
    return name_list



    

