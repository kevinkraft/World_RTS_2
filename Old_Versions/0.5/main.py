#World RTS 2
#Version: 0.5
#
#Kevin Maguire
#7/12/14
#
#Add:
#Action:
# * Need to select which type of action you want to do before showing list if possible actions as its too big if there are lots of units
#   * Could solve this by only printing the boring stuff related to the unit you have selected, not sure how to implement
#Orders
# * Section to allow You to give orders
#Add build building
# * First make a new simple building, hut (done)
# * Will need a class for building which is being built (done, called Construction)
# * Will need an action for building, called Construct, partly done(done)
#    * This action will involve going to stockpile to get resources, and increasing the comppletion of the building(done)
#    * For now the materials have to be collected first, then the constructor starts to increase the completion(done)
#    * Have to take into account that the units can only carry so much at once (done)
#    * Have to make a distinction between a "new construction", "construction" and "construct"(done)
#      * A new constrction will make a Construction and who ever started it will work on it (done)
#      * A constrution is an entity which is a Building which is currently being built, more than one unit can work on it
#      * a construct is an action that a unit has, two units will have different constructs but can be working on the same construction
# * The Setup command for a Construct and a New Construct will have to be different, but the action_ itself will be the same type of class
#AutomaticExchange
# * I can probably put AutomaticFood and Automatic Construct exchange together
#Procreate
# * This action creates a baby which must be cared for by someone unless it dies and must also be brought food
#
#Stockpile
# * There's nothing to say that the stockpile is full, 
# * when 2(or whatever) space left and you want to put in 5(or whatever) it gives error and puts in none, fix this.
#DropInventory:
# * Give Items a pos atribute so that they can be dropped by entities. 
#
#Problem:
# * I've noticed that units eventually stop collecting if they were ordered to do so, something to do with eating action interrupting them,
#   * FIXED
#   they stop collecting because they are more than their intr_range away from the resource, maybe theres a MoveTo missing after some
#   automatic action
#   * Interesting, if you move the unit back to the food resource, they automatically restart collecting. So yes, the action is still at the
#     head of their queue but they can't do it because they are too far away. If you add a clause to collect to make them move to the
#     resource if they are too far away it should fix this
#     * No, this isn't true, may just have been a coincidence that he started collecting again becuse he was hungry.  
#   * I added a clause that makes the unit return to the resource if they are too far away. This will probably solve the problem
# * When the units inventory is full they cant eat, make them get rid of some of their inventory if this is the case(fixed)
# * Every second time the unit goes back to get materials when they are constructing they collect 0 resources for some reason  (fixed)
#   * There are two "move exchange move"s added to the action list for some reason.they should be added one at a time, after the unit
#     has come back to the construction with the resources and transferred them to the construction
#     * this is caused by the DumpInventory() command, I will move it, its unrelated to the about bug tho.
#   * FIXED: A for loop was endind after the unit transferred resources to the construction. It was then going on to give the next
#     DoConstruct command when it should have been returning. So I added a return statement, so the cycle ends instead of adding in the
#     next DoConstruct cycle a cycle too soon
# * There was a bug related to eating and collecting at the same time, but I can't reproduce it. 

import sys
import pygame
from pygame.locals import *
from config import *
from entities import *
from actions import *
from terrains import *
from items import *
import all_names
from functions import *
from initialize import * 
from game_loop import *
"""

Main fuction. Do python main.py to run game

"""

def main():

    #Initialize
    screen, Entity_list, Unit_list, selection, terr_list, Resource_list, Building_list, Entity_HP_list, building_type_names, res_type_names = Initialize()
    Construction_list = []
    clock, minutes, seconds, milliseconds = StartClock()

    #main menu
    main_menu()

    #main game loop
    while 1:

        #control hunger
        #Decrease Hunger, take damage if hunger is zero
        for unit in Unit_list:
            unit.hunger = unit.hunger - hunger_per_cycle
            if unit.hunger <= 0:
                unit.hunger = 0
                unit.HP = unit.HP - hunger_per_cycle_damage
                if int(unit.HP) % 5 == 0: #print when HP on even number
                    print '{0} {1} is starving to death'.format(type(unit).__name__, unit.name)
            if unit.hunger <= 50:
                eat_order = False
                for action_ in unit.action: #if the unit already has an eat order then dont add one
                    if isinstance(action_, Eat):
                        eat_order = True
                if eat_order == False:
                    eat_ = Eat(unit) #go and eat
                    unit.action.insert(0, eat_)
            
        #kill dead entities/remove depleted resources. Entities are marked as dead here but
        #not removed till the end of the loop so actions involving them are not interupted
        for entity in Entity_list:
            if isinstance(entity, Unit):
                if entity.HP <= 0:
                    entity.dead = True
                    print '{0} {1} died, they will not be forgotten'.format(type(entity).__name__, entity.name)
            if isinstance(entity, Building):
                if entity.HP <= 0:
                    entity.dead = True
                    print '{0} {1} was destroyed, we must rebuild'.format(type(entity).__name__, entity.name)
            elif isinstance(entity, Resource):
                if entity.amount <= 0:
                    entity.dead = True
                    print
                
        #remake container lists
        Entity_HP_list = []
        Entity_HP_list = Unit_list + Building_list

        #do actions
        for entity in Entity_HP_list:
            if entity.action == []:
                continue
            action_ = entity.action[0] #takes the first action, which is the current order 
            #attack
            if isinstance(action_, Attack):
                attack_ = action_
                attack_result = attack_.DoAttack()
                if attack_result == False: #target moved away
                    entity.MoveTo(attack_.target.pos, True) #pos, option. True means the action_list will be prepended not overidden
                elif attack_result == True: #target dead, delete attack
                    attack_.DeleteAction()
                else:
                    continue #attack cycle complete
            #collect
            elif isinstance(action_, Collect):
                collect_ = action_
                collect_result = collect_.DoCollect(res_type_names)
                if  collect_result == True: #true if inventory full
                    if collect_.return_to_stockpile == True:
                        #go back to stockpile when inventory full
                        #Note: I could use dump inventory here, but for later additions(weapons) its best not to
                        entity.MoveTo(collect_.target.pos, True) #add return to target to keep collecting
                        collect_.AutomaticCollectExchange() #add exchange with stockpile
                        entity.MoveTo(entity.stockpile.pos, True) #add move to stockpile
                        continue
                    else: #dont return to stockpile for whatever reason
                        collect_.DeleteAction()
                #elif collect_result == None: #out of range #depricated, delete
                #    collect_.DeleteAction()
                #    continue
            #movement
            elif isinstance(action_, Movement): 
                move_ = action_
                if move_.DoMove() == True: #do movement, true is destination reached
                    move_.DeleteAction()
            #exchange
            elif isinstance(action_, Exchange):
                exchange_ = action_
                exchange_.MakeOrderExchange()
            #Enter
            elif isinstance(action_, Enter):
                enter_ = action_
                enter_.DoEnter()
            #Procreate
            elif isinstance(action_, Procreate):
                procreate_ = action_
                new_entity = procreate_.DoProcreate()
                Entity_list.append(new_entity)
                Unit_list.append(new_entity)
            #Eat
            elif isinstance(action_, Eat):
                eat_ = action_
                eat_.DoEat(Resource_list)
            #Construct
            elif isinstance(action_, Construct):
                construct_ = action_
                construct_.DoConstruct()
            else:
                print type(action_)
                print 'That action isnt implemented yet'
                action_.DeleteAction()

        #consolidate unit inventories, remove empty items
        ConsolidateInventories(Entity_HP_list)
                                        
        #timing
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds > 60:
            minutes += 1
            seconds -= 60
        #text = time_font.render(('{}:{}'.format(minutes, seconds)), 1, BLACK) #text,antialiasing,colour
        #textpos = text.get_rect()
        #textpos.centerx = time_xpos
        #textpos.centery = time_ypos
        #screen.blit(text, textpos)
        milliseconds += clock.tick(60) #returns time since the last call, limits the frame rate to 60FPS

        #event loop
        for event in pygame.event.get():
            #quit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #button press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    #add Unit
                    unit = Unit([0,0])
                    Entity_list.append(unit)
                    Unit_list.append(unit)
                    print '{} created'.format(unit.name)
                if event.key == pygame.K_s:
                    #select entity
                    selection = SelectEntity(Entity_HP_list)
                if event.key == pygame.K_m:
                     #reprint main menu
                    main_menu()
                if event.key == pygame.K_u:
                    #unselect entity
                    selection = []
                    print 'Deselected'
                if event.key == pygame.K_t:
                    #display time
                    print '{}:{}'.format(minutes, seconds)
                if event.key == pygame.K_v:
                    #movement
                    ChooseMovement(selection)
                if event.key == pygame.K_d:
                    #list unit properties
                    display_unit_atributes(Unit_list)
                if event.key == pygame.K_r:
                    #list resource properties
                    display_resource_atributes(Resource_list)
                if event.key == pygame.K_b:
                    #list building properties
                    display_building_atributes(Building_list)
                if event.key == pygame.K_c:
                    #possible actions for unit 
                    ChooseAction(selection, Entity_list, building_type_names, Construction_list)
                if event.key == pygame.K_h:     
                    #print unit inventories
                    for i in range(0, len(Unit_list)):
                        print i
                        print unit.inventory
                if event.key == pygame.K_i:     
                    #print selections inventory
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    display_inventory_atributes(selection)
                if event.key == pygame.K_g:     
                    #print selected buildings unit inventory
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    if not isinstance(selection, Building):
                        print 'Only buildings can have garrisons'
                        continue
                    selection.DisplayGarrison()
                if event.key == pygame.K_l:
                    #display actions
                    if selection == []:
                        pass
                    else:
                        Info(['selection.action:', selection.action], 'debug')
                        #print 'selection.action:'
                        #print selection.action
                    print "--------------------------------------------------------------------"
                    for unit in Unit_list: 
                        unit.DisplayEntityAction()
                    print "--------------------------------------------------------------------"
                if event.key == pygame.K_x:
                    #cancel action
                    if selection == []:
                        print 'No Entity Selected'
                        continue
                    for action_ in selection.action:
                        action_.DeleteAction()
                    selection.action = []
                    print 'All {0} {1} actions cancelled'.format(type(selection).__name__, selection.name)
                if event.key == pygame.K_o:
                    #show construction
                    display_construction_atributes(Construction_list)
                if event.key == pygame.K_q:
                    #exit
                    pygame.quit()
                    sys.exit()
        
        #remove dead entities
        for entity in Entity_list:
            if entity.dead == True:
                Entity_list.remove(entity)
                if isinstance(entity, Building):
                    Building_list.remove(entity)
                if isinstance(entity, Unit):
                    Unit_list.remove(entity)
                if isinstance(entity, Resource):
                    Resource_list.remove(entity)

        #make buildings for completed constructions
        for construction_ in Construction_list:
            if construction_.work <= 0:
                building_ = Building(construction_.pos, construction_.type_)
                building_.set_building_atributes(building_type_names)
                Building_list.append(building_)
                Construction_list.remove(construction_)
                Info('{0} {1} at [{2:.2f}, {3:.2f}] has been completed'.format(type(building_), building_.name, building_.pos[0],
                                                                               building_.pos[1]),'normal')
                del construction_

main()







