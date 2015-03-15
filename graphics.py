import sys
import pygame
from pygame.locals import *
from config import *
from functions import *
#from items import *
#from actions import *

"""

contains functions that update the graphical map

"""

class ScreenSet(object):
    """
    
    Class which defines the make up of the screen and graphics
    defined by a pygame surface, a pos which is the top left corner of the screen in game coords
    and an x and y length which will define the zoom of the screen as the length of the screen in game coords
    
    """
    def __init__(self, screen, topleft, xlength, ylength):
        self.screen = screen
        self.topleft = topleft
        self.xlength = xlength
        self.ylength = ylength

def MakeScreen():
    #makes and returns ScreenSet class

    screen = pygame.display.set_mode((screen_width, screen_height))    
    pygame.FULLSCREEN#pygame.display.set_mode((screen_width, screen_height_toolbar))                                                          
    pygame.display.set_caption('World RTS 2')
    pygame.display.toggle_fullscreen
    screen.fill(OLIVE)
    pygame.display.flip()
    topleft = [-screen_width/2, -screen_height/2]
    xlength = screen_width
    ylength = screen_height
    SSet = ScreenSet(screen, topleft, xlength, ylength)
    return SSet

def makeCrossPointlist(pos):
    #returns a list of points that define a cross (plus) shape

    pointlist = []
    pointlist.append([pos[0] - cross_size, pos[1]])
    pointlist.append([pos[0] + cross_size, pos[1]])
    pointlist.append([pos[0], pos[1]])
    pointlist.append([pos[0], pos[1] + cross_size])
    pointlist.append([pos[0], pos[1] - cross_size])
    return pointlist

def PosGametoScreen(gamepos, screenSet):
    #give a position in the game coordinates and returns a pos in the screen coords
    screenpos = [0 ,0]
    topleft = screenSet.topleft
    #scroll and zoom
    screenpos[0] = (gamepos[0] - topleft[0])*(screen_width/screenSet.xlength)
    screenpos[1] = (gamepos[1] - topleft[1])*(screen_height/screenSet.ylength)
    return screenpos
    
    
def UpdateScreen(GM):
    #update the game screen for each cycle, GM is GameManager

    #check that the GM lists all make sense
    GM.checkLists()

    screen = GM.screenSet.screen
    screen.fill(OLIVE)
    #resource with filled squares
    for res in GM.Resource_list:
        screenpos = PosGametoScreen(res.pos, GM.screenSet)
        pygame.draw.rect(screen, resource_colour, (screenpos[0], screenpos[1], square_length, square_length))
    #construction with filled squares
    for constr in GM.Construction_list:
        screenpos = PosGametoScreen(constr.pos, GM.screenSet)
        pygame.draw.rect(screen, construction_colour, (screenpos[0], screenpos[1], square_length, square_length))
    #buildings with filled squares
    for build in GM.Building_list:
        screenpos = PosGametoScreen(build.pos, GM.screenSet)
        pygame.draw.rect(screen, building_colour, (screenpos[0], screenpos[1], square_length, square_length))
    #entities with crosses
    for unit in GM.Unit_list:
        pointlist = makeCrossPointlist(PosGametoScreen(unit.pos, GM.screenSet))
        pygame.draw.lines(screen, unit_colour, False, pointlist, cross_line_width) #surface, colour, closed, points, width    


    pygame.display.flip()
    return

def Zoom(screenSet, inout):
    #changes topleft and x(y)length of screen set to do zoom

    xlength_old = screenSet.xlength
    ylength_old = screenSet.ylength
    if inout == 'out':
        xlen = screenSet.xlength*2 
        ylen = screenSet.ylength*2
        if xlen > 1.5*screen_width or ylen > 1.5*screen_height:
            Info("Can't zoom out anymore", 'normal')
            return
        else:
            screenSet.xlength = xlen
            screenSet.ylength = ylen
            Info('Zoomed Out', 'normal')
    elif inout == 'in':
        xlen = screenSet.xlength/2 
        ylen = screenSet.ylength/2
        if xlen < 5 or ylen < 5:
            Info("Can't zoom in anymore", 'normal')
            return
        else:
            screenSet.xlength = xlen
            screenSet.ylength = ylen
            Info('Zoomed In', 'normal')
    #change topleft so we zoom centrally
    screenSet.topleft[0] = screenSet.topleft[0] + (xlength_old - screenSet.xlength)/2 
    screenSet.topleft[1] = screenSet.topleft[1] + (ylength_old - screenSet.ylength)/2
    return

