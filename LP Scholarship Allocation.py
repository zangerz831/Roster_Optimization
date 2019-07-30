# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:53:00 2019

@author: zachz
"""

from pulp import *
import numpy as np
import pandas as pd

###DEFINE RECRUIT VALUES###

player_a_attributes = {'Power': '55', 'Hit': '40', 'Glove': '45', 'Speed': '45', 'Arm': '50', 'Position': 'corner_infielder'}
player_b_attributes = {'Power': '60', 'Hit': '30', 'Glove': '40', 'Speed': '50', 'Arm': '40', 'Position': 'outfielder'}
player_c_attributes = {'Power': '45', 'Hit': '60', 'Glove': '60', 'Speed': '65', 'Arm': '35', 'Position': 'catcher'}

###DEFINE POSITION UTILITY WEIGHTS***
position_dict = {'catcher': '75', 'corner_infielder': '25', 'shortstop': '75', 'middle_infielder': '30', 'outfielder': '80'}

###CALCULATE UTILITIES###

def utility(power_weight, hit_weight, speed_weight, glove_weight, arm_weight):
    ###PLAYER A UTILITY CALC###
    player_a_power_utility=int(player_a_attributes.get('Power'))*int(power_weight) 
    player_a_hit_utility=int(player_a_attributes.get('Hit'))*int(hit_weight)
    player_a_speed_utility=int(player_a_attributes.get('Speed'))*int(speed_weight)
    player_a_glove_utility=int(player_a_attributes.get('Glove'))*int(glove_weight)
    player_a_arm_utility=int(player_a_attributes.get('Arm'))*int(arm_weight)
    if player_a_attributes.get('Position') == 'catcher':
        player_a_position_utility = int(position_dict.get('catcher'))
    elif player_a_attributes.get('Position') == 'corner_infielder':                                
        player_a_position_utility = int(position_dict.get('corner_infielder'))
    elif player_a_attributes.get('Position') == 'shortstop':
        player_a_position_utility = int(position_dict.get('middle_infielder'))
    elif player_a_attributes.get('Position') == 'outfielder':
        player_a_position_utility = int(position_dict.get('outfielder'))
    
    player_a_utility=(player_a_position_utility+player_a_power_utility+player_a_hit_utility+player_a_speed_utility+player_a_glove_utility+player_a_arm_utility)
    
    ###PLAYER B UTILITY CALC###
    player_b_power_utility=int(player_b_attributes.get('Power'))*int(power_weight) 
    player_b_hit_utility=int(player_b_attributes.get('Hit'))*int(hit_weight)
    player_b_speed_utility=int(player_b_attributes.get('Speed'))*int(speed_weight)
    player_b_glove_utility=int(player_b_attributes.get('Glove'))*int(glove_weight)
    player_b_arm_utility=int(player_b_attributes.get('Arm'))*int(arm_weight)
    if player_b_attributes.get('Position') == 'catcher':
        player_b_position_utility = int(position_dict.get('catcher'))
    elif player_b_attributes.get('Position') == 'corner_infielder':                                
        player_b_position_utility = int(position_dict.get('corner_infielder'))
    elif player_b_attributes.get('Position') == 'shortstop':
        player_b_position_utility = int(position_dict.get('middle_infielder'))
    elif player_b_attributes.get('Position') == 'outfielder':
        player_b_position_utility = int(position_dict.get('outfielder'))
    
    player_b_utility=(player_b_position_utility+player_b_power_utility+player_b_hit_utility+player_b_speed_utility+player_b_glove_utility+player_b_arm_utility)
    
    ###PLAYER C UTILITY CALC###
    player_c_power_utility=int(player_c_attributes.get('Power'))*int(power_weight) 
    player_c_hit_utility=int(player_c_attributes.get('Hit'))*int(hit_weight)
    player_c_speed_utility=int(player_c_attributes.get('Speed'))*int(speed_weight)
    player_c_glove_utility=int(player_c_attributes.get('Glove'))*int(glove_weight)
    player_c_arm_utility=int(player_c_attributes.get('Arm'))*int(arm_weight)
    if player_c_attributes.get('Position') == 'catcher':
        player_c_position_utility = int(position_dict.get('catcher'))
    elif player_c_attributes.get('Position') == 'corner_infielder':                                
        player_c_position_utility = int(position_dict.get('corner_infielder'))
    elif player_c_attributes.get('Position') == 'shortstop':
        player_c_position_utility = int(position_dict.get('middle_infielder'))
    elif player_c_attributes.get('Position') == 'outfielder':
        player_c_position_utility = int(position_dict.get('outfielder'))
    
    player_c_utility=(player_c_position_utility+player_c_power_utility+player_c_hit_utility+player_c_speed_utility+player_c_glove_utility+player_c_arm_utility)
    
    ###BEGIN OPTIMIZATION###
    model = LpProblem(name = "Scholarship Work", sense=LpMaximize)

    ###DEFINE DECISION VARIABLES###
    player_a=LpVariable('A', lowBound=0, cat = 'Continuous')
    player_b=LpVariable('B', lowBound=0, cat = 'Continuous')
    player_c=LpVariable('C', lowBound=0, cat = 'Continuous')
    
    ###DEFINE OBJECTIVE FUNCTION###
    model += (player_a_utility * (1+player_a)) + (player_b_utility * (1+player_b)) + (player_c_utility * (1+player_c))

    ###DEFINE CONSTRAINTS###
    model += player_a + player_b + player_c <=1
    model += player_a >= .15
    model += player_b >= .35
    model += player_c >= .15
    model += player_a <= .80
    model += player_b <= .80    
    model += player_c <= .80
    
    ###SOLVE MODEL###
    model.solve()
    print("Allocate {} Scholarship to Player A".format(player_a.varValue))
    print("Allocate {} Scholarship to Player B".format(player_b.varValue))
    print("Allocate {} Scholarship to Player C".format(player_c.varValue))
    print(player_a_utility, player_b_utility, player_c_utility)
utility(40,20,35,15,10)



""" DEFINE OBJECTIVE FUNCTION """
roster_problem += lpSum([xbh_dict[i]*hitter_vars[i] for i in hitter_names]) 

""" CONSTRAINTS """
roster_problem.solve()

roster_problem += lpSum([woba_dict[i] * hitter_vars[i] for i in hitter_names]) 



