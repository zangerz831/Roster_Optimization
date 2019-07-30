# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 00:03:32 2019

@author: zachz
"""

from pulp import *
import numpy as np
import pandas as pd

"D:2020_hitters.csv"
"/Volumes/NO NAME/2020_hitters.csv"
""" CREATE DATA SET """
hitters = pd.read_csv("D:2020_hitters.csv", index_col = 'name')
hitters = pd.DataFrame(hitters)
hitters = hitters.to_dict('dict')
hitter_names=list(hitters.keys())

""" VALUES FOR ANALYSIS """
hitter_names=list(hitters.keys())

woba_values = [name['woba'] for name in hitters.values()]
for i in range(0, len(woba_values)): 
    woba_values[i] = float(woba_values[i])

position_values = list([name['pos'] for name in hitters.values()])
 
xbh_values = [name['XBH%'] for name in hitters.values()]
for i in range(0, len(xbh_values)): 
    xbh_values[i] = float(xbh_values[i])

conference_rating_values = [name['Conference Rating'] for name in hitters.values()]
for i in range(0, len(conference_rating_values)): 
    conference_rating_values[i] = float(conference_rating_values[i])

obp_values = [name['obp'] for name in hitters.values()]
for i in range(0, len(obp_values)): 
    obp_values[i] = float(obp_values[i])

""" CREATE DICTIONARIES FROM VALUES """
woba_dict = dict(zip(hitter_names,woba_values))
xbh_dict = dict(zip(hitter_names,xbh_values))
conference_rating_dict = dict(zip(hitter_names,conference_rating_values))
obp_dict = dict(zip(hitter_names,obp_values))
position_dict = dict(zip(hitter_names,position_values))


""" SET UP WEIGHTS """
woba_weight = float(.20)
xbh_weight = float(.20)
conference_rating_weight = float(.50)
obp_weight = float(.60)


""" INITIALIZE THE MODEL """
roster_problem = LpProblem("roster_problem", LpMaximize)

""" DEFINE DECISION VARIABLES """
unique_position_values = ['1B' '2B' 'C' 'INF' 'OF' 'P' 'UT' 'rf' 'ss']
key = ((n) for n in hitter_names)
hitter_status = LpVariable.dicts("Hitter_Status",key, cat = 'Binary')

""" DEFINE POSITION LISTS """
outfielder_list = list()
infielder_list = list()
utility_list = list()
catcher_list = list()
first_basemen_list = list()

for n in hitter_status:
    if position_dict[n]=='OF':
        outfielder_list.append(n)

for n in hitter_status:
    if position_dict[n]=='INF':
        infielder_list.append(n)

for n in hitter_status:
    if position_dict[n]=='UT':
        utility_list.append(n)

for n in hitter_status:
    if position_dict[n]=='C':
        catcher_list.append(n)

for n in hitter_status:
    if position_dict[n]=='1B':
        first_basemen_list.append(n)


""" DEFINE OBJECTIVE FUNCTION """
roster_problem += lpSum((obp_dict[n]*obp_weight*hitter_status[n])
                        +(woba_dict[n]*woba_weight*hitter_status[n])
                        +(xbh_dict[n]*xbh_weight*hitter_status[n])
                        +(conference_rating_dict[n]*conference_rating_weight*hitter_status[n])for n in hitter_status)

"""CONSTRAINTS"""
roster_problem += lpSum(hitter_status[n] for n in hitter_status) <= 25
roster_problem += lpSum(hitter_status[n] for n in outfielder_list) >= 5
roster_problem += lpSum(hitter_status[n] for n in infielder_list) >= 5
roster_problem += lpSum(hitter_status[n] for n in utility_list) >= 7
roster_problem += lpSum(hitter_status[n] for n in catcher_list) >= 4
roster_problem += lpSum(hitter_status[n] for n in first_basemen_list) >= 3

""" SOLVE THE PROBLEM """
roster_problem.solve()


print("Status:", LpStatus[roster_problem.status])
for n in hitter_status:
    if hitter_status[n].varValue == 1.0: 
        print("{} {}".format(n, position_dict[n]))

