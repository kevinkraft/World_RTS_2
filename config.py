import sys
"""

File to hold all the default config GLOBAL values

"""
#--------------------------------------------------------------
# Starting positions
#--------------------------------------------------------------


start_units = 0
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
Hut_default_unit_cap = 3
hunger_per_cycle = 0.01
hunger_per_cycle_damage = 0.01
eat_speed = 0.01
food_pickup_amount = 2 #this can't be bigger than unit_default_inv_cap
food_hunger_value = 10

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
