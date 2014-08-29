import sys
import pygame
from pygame.locals import *

"""

Terrain will be defined by a top left corner position of a square of a certain length

"""

class Terrain(object):
     """

     All terrains

     """
     def __init__(self, pos, terr_type, length = 10, name = 'default', pointlist = []):        
        self.pos = pos
        self.terr_type = terr_type
        self.length = length
        self.name = name
        self.pointlist = pointlist

#        def get_terr_name(terr):
#             #water
#             if self.type == 1:
 #                 name = 'Water'
 ##            #mountains
 #            if self.type == 2:
  #                name = 'Mountain'
  ##           self.name = name#
#
#        def get_speed_multi(terr):
##             #speed changes due to terrain: coming soon
#             self.speed_multi = 1
#
##        def get_pointlist(ter):
#             #list of terrain square corners
 #            point2 = [self.pos[0] + length, self.pos[1]]
 #            point3 = [self.pos[0] + length, self.pos[1] + length]
 ##            point4 = [self.pos[0] , self.pos[1] + length]
 #            self.pointlist =  [self.pos, point2, point3, point4]
