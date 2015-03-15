
import sys
import pygame
from pygame.locals import *
from functions import *
from entities import *

"""

Contains the game manager and (will contain)nation manager classes

"""

class GameManager():
    """
    
    Will contain pointers to all entity lists, screen and nation managers when finished
    Changing any of the lists should also change the list atribute of the GameManager as it just contains pointers

    Problem: Chnaging the lists doesnt always change the GM bacause if you redefine the list name if wont update the pointer
             if just makes a new one
    
    """
    def __init__(self, screenSet, Entity_list, Unit_list, selection, terr_list, Resource_list, Building_list, Entity_HP_list,
                 Entity_Action_list, Construction_list, building_type_names, res_type_names):        
        self.screenSet = screenSet
        self.Entity_list = Entity_list
        self.Unit_list = Unit_list
        self.selection = selection
        self.terr_list = terr_list
        self.Resource_list = Resource_list
        self.Building_list = Building_list
        self.Entity_HP_list = Entity_HP_list
        self.Entity_Action_list = Entity_Action_list
        self.Construction_list = Construction_list
        self.building_type_names = building_type_names
        self.res_type_names = res_type_names

    def update(self, screenSet, Entity_list, Unit_list, selection, terr_list, Resource_list, Building_list, Entity_HP_list,
               Entity_Action_list, Construction_list, building_type_names, res_type_names):        
        #update the GM, this is only temporary I need to implement the GM so that this is not necessary
        self.screenSet = screenSet
        self.Entity_list = Entity_list
        self.Unit_list = Unit_list
        self.selection = selection
        self.terr_list = terr_list
        self.Resource_list = Resource_list
        self.Building_list = Building_list
        self.Entity_HP_list = Entity_HP_list
        self.Entity_Action_list = Entity_Action_list
        self.Construction_list = Construction_list
        self.building_type_names = building_type_names
        self.res_type_names = res_type_names
        self.checkLists()
                
    def checkLists(self):
        #checks all the GM lists to make sure nothing is 
        #left out and everything makes sense. This is for debugging
        
        units = []
        entity_HPS = []
        all_entities = []
        entity_actions = []
        buildings = []
        resources = []
        constructions = []
        for entity_ in self.Entity_list:
            if isinstance(entity_, Entity):
                all_entities.append(entity_)
                if isinstance(entity_, Entity_HP):
                    entity_HPS.append(entity_)
                    if isinstance(entity_, Entity_Action):
                        entity_actions.append(entity_)
                        if isinstance(entity_, Building):
                            buildings.append(entity_)
                        elif isinstance(entity_, Unit):
                            units.append(entity_)
                    else:
                        if isinstance(entity_, Construction):
                            constructions.append(entity_)
                        else:
                            Info('An element in the Entity HP list is not an Entity Action or a Construction', 'debug')
                else:
                    if isinstance(entity_, Resource):
                        resources.append(entity_)
                    else:
                        Info('An element in the Entity list is not an Entity HP or a Resource', 'debug')
            else:
                Info('An element in the GameManager Entity list is not an entity', 'debug')

        #now check the lengths
        lists = [units, entity_HPS, all_entities, entity_actions, buildings, resources, constructions]
        GMlists = [self.Unit_list, self.Entity_HP_list, self.Entity_list, self.Entity_Action_list, self.Building_list,
                   self.Resource_list, self.Construction_list]
        debugname = ['units', 'entity_HPS', 'all_entities', 'entity_actions', 'buildings', 'resources', 'constructions']
        for i in range(0, len(lists)):
            if len(lists[i]) != len(GMlists[i]):
                Info('ERROR: {0} and GM list are not the same'.format(debugname[i]), 'debug')
                print GMlists[i]
                print lists[i]
                print len(GMlists[i])
                print len(lists[i])
                return
   



        
    
