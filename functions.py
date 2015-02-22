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

def ReceiveInput(string, option = '', cancel_option = False, min_ = None, max_ = None):
    #get keyboard input, handle invalid choices
    while True:
        if cancel_option == True:
            print "type None to go back"
        try:
            val = input(str(string+' '))
        except NameError:
            print 'NameError'
            print 'invalid Choice'
            continue
        except SyntaxError:
            print 'SyntaxError'
            print 'invalid Choice'
            continue
        if cancel_option == True: #optional to have a cancel
            if val == None:
                val = None
                return val #cancel and go back
        else:
            if option == 'Number':
                if isinstance(val, (int, long, float)) == False:
                    print 'Choice must be a number'
                    continue
                if min_ != None:
                    if val < min_:
                        print 'Choice must be bigger than {}'.format(min_)
                        continue
                if max_ != None:
                    if val > max_:
                        print 'Choice must be smaller than {}'.format(max_)
                        continue
            elif option == 'String':
                if type(val) is not string:
                    print 'Choice must be a string'
                    continue
        return val

def XYInput(title):
    #user chooses an x,y point
    print title
    while 1: #keeps looping till valid choice made
        new_x = ReceiveInput('X-coordinate:', 'Number', True) #string, option, cancel_option
        if new_x == None:
            print 'Exited'
            return False
        new_y = ReceiveInput('Y-coordinate:', 'Number', True)
        if new_y == None:
            print 'Exited'
            return False
        break
    return [new_x, new_y]

#-------------------------------------------------------------------
# Menus
#-------------------------------------------------------------------

def make_menu_choice(*strs):
    #menu with built in choice. Pass a title string and a list of str choices
    print '-----------------------------------------'
    print strs[0]
    for i in range(0,len(strs[1])):
        print '{}) {}'.format(i+1, strs[1][i])
    print '{}) Go Back'.format(len(strs[1]) + 1) 
    print '----------------------------------------'
    choice = ReceiveInput('>', 'Number', False, 1, len(strs[1]) + 1)
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
    make_menu('What would you like to do?',['a', 's', 'm', 'u', 't', 'v', 'd','r','b','c','i', 'g', 'l', 'x', 'o', 'q'], ['Add Unit',
                                                                                                                          'Select Entity',
                                                                                                                          'Display Menu', 
                                                                                                                          'Unselect Entity',
                                                                                                                          'Display Time',
                                                                                                                          'Move Unit',
                                                                                                                          'Display Units',
                                                                                                                          'Display Resources',
                                                                                                                          'Display Buildings',
                                                                                                                          'Do Action',
                                                                                                                          'Display Items',
                                                                                                                          'Display Garrison',
                                                                                                                          'Display Actions',
                                                                                                                          'Cancel Actions',
                                                                                                                          'Show Constructions',
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

def make_name_type_list(Entity_list):
    #make list of entity names
    name_list = []
    for i in range(0, len(Entity_list)):
        name_list.append('{0} {1}'.format(type(Entity_list[i]).__name__, Entity_list[i].name))
    return name_list



    

