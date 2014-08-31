import sys
import pygame
from pygame.locals import *
import all_names
from random import choice

"""

All game entities

"""

class Entity(object):
     """

     All game entities

     """
     def __init__(self, pos, intr_range = 2):        
          self.pos = pos
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          
     @staticmethod
     def random_name():
          #choose random name
          names = all_names.names
          return choice(names)

class Unit(Entity):
     """

     All movable entities. i.e. people

     """
     def __init__(self, pos, intr_range = 2, speed = 0.02): #speed is per cyle 60 cycl/s (not sure about this)         
          self.pos = pos
          self.name = Entity.random_name()
          self.intr_range = intr_range 
          self.speed = speed

     def move_unit(self, destination): #unit is a class instance
          #frontier = Queue()
          #frontier.put(start)
          #visited = {}
          #visited[start] = True
         # 
         # while not frontier.empty():
         #      current = frontier.get()
         #      for next in graph.neighbors(current):
         #           if next not in visited:
         #                frontier.put(next)
         #                visited[next] = True
