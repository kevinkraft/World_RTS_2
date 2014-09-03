import sys
import pygame
from pygame.locals import *
from class_test_module import *

def main():
    c = NewClass()
    m = ModClass()
    
    print "c"
    print c
    print "------------------------------------------------------"
    print "type(c)"
    print type(c)
    print "------------------------------------------------------"
    print "NewClass"
    print NewClass
    print "------------------------------------------------------"
    print "type(NewClass)"
    print type(NewClass)
    print "------------------------------------------------------"
    print "------------------------------------------------------"
    print "m"
    print m
    print "------------------------------------------------------"
    print "type(m)"
    print type(m)
    print "------------------------------------------------------"
    print "ModClass"
    print ModClass
    print "------------------------------------------------------"
    print "type(ModClass)"
    print type(ModClass)
    print "------------------------------------------------------"
    print "------------------------------------------------------"
    print "type(c) is NewClass"
    print type(c) is NewClass
    print "------------------------------------------------------"
    print "type(m) is ModClass"
    print type(m) is ModClass
    print "------------------------------------------------------"
    print "------------------------------------------------------"
    print "c is NewClass"
    print c is NewClass
    print "------------------------------------------------------"
    print "m is ModClass"
    print m is ModClass
    print "------------------------------------------------------"
    print "------------------------------------------------------"
    print "isinstance(c, NewClass)"
    print isinstance(c, NewClass)
    print "------------------------------------------------------"
    print "isinstance(m, ModClass)"
    print isinstance(m, ModClass)
    print "------------------------------------------------------"
    print "------------------------------------------------------"

class NewClass(object):
    def __init__(self):
        pass

main()
