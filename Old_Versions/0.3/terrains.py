import sys
import pygame
from pygame.locals import *

"""

Terrain will be defined by a top left corner position of a square of a certain length

"""

class terrain(object):
     """

     All terrains

     """
     def __init__(self, pos, terr_type, length, name = 'default', pointlist = [], passable = True):        
          self.pos = pos
          self.type_ = terr_type
          self.length = length
          self.name = name
          self.pointlist = pointlist
          self.passable = passable
          
     def set_terr_parameters(self):
          #grassland
          if self.type_ == 0 :
               name = 'Grassland'
               self.passable = True
          #water
          if self.type_ == 1:
               name = 'Water'
               self.passable = False
          #mountains
          if self.type_ == 2:
               name = 'Mountain'
               self.passable = False
          self.name = name
          self.speed_multi = 1 #all the same for now
                         
          #list of terrain square corners
          point2 = [self.pos[0] + self.length, self.pos[1]]
          point3 = [self.pos[0] + self.length, self.pos[1] + self.length]
          point4 = [self.pos[0] , self.pos[1] + self.length]
          self.pointlist =  [self.pos, point2, point3, point4]
     
