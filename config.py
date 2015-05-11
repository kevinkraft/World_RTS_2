import sys
"""

File to hold all the default config GLOBAL values

"""
#--------------------------------------------------------------
# Starting positions
#--------------------------------------------------------------

start_units = 3
start_food_resources = 4
start_random_map_resources = 3
res_dist_factor = 4
unit_dist_from_you = 2
res_dist_from_you = 10
building_dist_from_you = 2

#--------------------------------------------------------------
# Entity Atributes
#--------------------------------------------------------------

Unit_default_inv_cap = 5
Unit_default_intr_range = 1
main_hut_default_unit_cap = 10
hut_default_inv_cap = 30
hut_default_unit_cap = 4
#hunger_per_cycle = 0.1
hunger_per_cycle = 0.006
#hunger_per_cycle = 0.05
hunger_per_cycle_damage = 0.01
eat_speed = 0.01
food_pickup_amount = 2 #this can't be bigger than unit_default_inv_cap
if food_pickup_amount > Unit_default_inv_cap:
    print "CONFIG: food_pickup_amount can't be bigger than unit_default_inv_cap. Exiting"
    sys.exit()
food_hunger_value = 10

#--------------------------------------------------------------
# Screen
#--------------------------------------------------------------

screen_width = 480
screen_height = 480
terminal_width = 90
terminal_height = 40
scroll_amount = 100.0

#--------------------------------------------------------------
# Building materials needed
#--------------------------------------------------------------

main_hut_wood = 200
main_hut_stone = 10
storage_pile_wood = 50
storage_pile_stone = 5
hut_wood = 75
hut_stone = 0
materials_type0 = {0:0, 1:main_hut_wood, 2:main_hut_stone} 
materials_type1 = {0:0, 1:storage_pile_wood, 2:storage_pile_stone} #food,wood,stone, type:amount
materials_type2 = {0:0, 1:hut_wood, 2:hut_stone} 
materials_types = [materials_type0, materials_type1, materials_type2]
construct_work0 = 400
construct_work1 = 100
construct_work2 = 200

#--------------------------------------------------------------
# Colours
#--------------------------------------------------------------

OLIVE = (107, 142, 35)
BLACK = (0, 0, 0)
BLUE = (0, 0, 205)
GREY = (105, 105, 105)
HIGHLIGHT_BLUE = (0, 191, 255)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#--------------------------------------------------------------
# Display
#--------------------------------------------------------------

#options are 'debug', 'normal'
display = 'debug'
cross_size = 5
cross_line_width = 3
square_length = 10
unit_colour = BLUE
building_colour = BLACK
construction_colour = YELLOW
resource_colour = BROWN

#--------------------------------------------------------------
# Map
#--------------------------------------------------------------

simple_map = [[2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 1, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 1, 1, 1],
              [2, 2, 0, 0, 1, 0, 1, 0, 1, 1],
              [2, 2, 0, 0, 0, 1, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1],
              [2, 2, 0, 0, 0, 0, 0, 0, 1, 1]]
terr_length = 10
current_map = simple_map
