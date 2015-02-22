import sys
"""

File to hold all the default config GLOBAL values

"""
#--------------------------------------------------------------
# Starting positions
#--------------------------------------------------------------


start_units = 1
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
main_hut_default_unit_cap = 10
hut_default_inv_cap = 30
hut_default_unit_cap = 4
hunger_per_cycle = 0.01
hunger_per_cycle_damage = 0.01
eat_speed = 0.01
food_pickup_amount = 2 #this can't be bigger than unit_default_inv_cap
if food_pickup_amount > Unit_default_inv_cap:
    print "CONFIG: food_pickup_amount can't be bigger than unit_default_inv_cap. Exiting"
    sys.exit()
food_hunger_value = 10

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
# Display
#--------------------------------------------------------------

#options are 'debug', 'normal'
display = 'debug'

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
