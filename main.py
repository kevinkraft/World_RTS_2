#World RTS 2
#Version: 0.0
#
#Kevin MAguire
#11/08/14
#
#Notes:
# Interface will be multiple choice in terminal menus for now. Tables in ASCII if there are any.
# The game will have continuous coordinates and will not be based on a grid
# Every entity will have a positive grid coordinate(x,y) which increases right for x and down for y, as in pygame.
# Entities will include everything, units, buildings, resources. Except Terrain, which will be based on ranges. 
#
#Add:
# Select Entity(done)
# default menu function(done)
# Display entity atributes(done)
#  Add More atributes
# Modify atrributes


import sys
import entities


def main():

    entity_list = []

    #Event loop
    while 1:

        #main menu
        choice = make_menu("What would you like to do?",["Add Entity", "Display Entities", "Select Entity", "Quit"])
        if choice == 1:
            #add entity
            entity = entities.entity([0,0])
            entity_list.append(entity)
            print entity
        elif choice == 2:
            #display entities
            if len(entity_list) == 0:
                print "There are no entites"
                continue
            print entity_list
        elif choice == 3:
            #select entity
            if len(entity_list) == 0:
                print "There are no entites"
                continue
            choice = make_menu("Select an entity", entity_list)
            selection = entity_list[choice-1]
            while 1:
                choice = make_menu("Available Actions", ["Display Atributes", "Modify Atributes", "Back"])
                if choice == 1:
                    #display entity atributes
                    print "Entity position is:"
                    print selection.pos
                elif choice == 2:
                    #modify atributes
                    print "coming soon"
                    #new_x = input("New x-coordinat> ")
                    
                    
                elif choice == 3:
                    #Go Back
                    break
                else:
                    print "Not a valid option"
                    continue
        elif choice == 4:
            #exit
            sys.exit()
        else:
            print "Not a valid option"
            continue



def make_menu(*strs):
    print "-----------------------------------------"
    print strs[0]
    for i in range(0,len(strs[1])):
        print "{}) {}".format(i+1, strs[1][i])
    print "----------------------------------------"
    choice = input("> ")
    return choice

main()







