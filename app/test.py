#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:27:12 2020

@author: byron
"""

#%%

import snake as snk
import graph
from graph import Loc
import numpy as np
import time

def to_loc_list(locs):
    loc_list = []
    
    for l in locs:
        loc_list.append(Loc(l['x'],l['y']))
        
    return loc_list
    
def build_snakes(data, me_id='0'):
    snakelist = []
    for snake in data['board']['snakes']:
        if snake['id'] != me_id:
            snakelist.append(snk.Snake(snake))
        
    return snakelist

data = {'game': {'id': '66c14f72-bbb5-4228-9025-c6f843f13892'}, 'turn': 244, 'board': {'height': 15, 'width': 15, 'food': [{'x': 4, 'y': 13}, {'x': 1, 'y': 7}, {'x': 3, 'y': 0}, {'x': 12, 'y': 3}, {'x': 9, 'y': 3}, {'x': 6, 'y': 7}, {'x': 10, 'y': 9}, {'x': 12, 'y': 6}, {'x': 0, 'y': 14}, {'x': 8, 'y': 4}], 'snakes': [{'id': '491ee34a-020f-4b95-be77-33e23afc19d0', 'name': '', 'health': 75, 'body': [{'x': 10, 'y': 6}, {'x': 9, 'y': 6}, {'x': 8, 'y': 6}, {'x': 7, 'y': 6}, {'x': 6, 'y': 6}, {'x': 6, 'y': 5}, {'x': 6, 'y': 4}, {'x': 6, 'y': 3}, {'x': 5, 'y': 3}, {'x': 5, 'y': 2}, {'x': 5, 'y': 1}, {'x': 4, 'y': 1}, {'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}, {'x': 6, 'y': 1}, {'x': 7, 'y': 1}, {'x': 8, 'y': 1}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1}, {'x': 11, 'y': 1}, {'x': 11, 'y': 0}, {'x': 12, 'y': 0}, {'x': 13, 'y': 0}, {'x': 14, 'y': 0}]}, {'id': '3ed5075d-4314-4627-aea8-7059f1b3a240', 'name': '', 'health': 100, 'body': [{'x': 12, 'y': 10}, {'x': 12, 'y': 11}, {'x': 11, 'y': 11}, {'x': 10, 'y': 11}, {'x': 9, 'y': 11}, {'x': 8, 'y': 11}, {'x': 7, 'y': 11}, {'x': 6, 'y': 11}, {'x': 5, 'y': 11}, {'x': 4, 'y': 11}, {'x': 3, 'y': 11}, {'x': 3, 'y': 12}, {'x': 4, 'y': 12}, {'x': 5, 'y': 12}, {'x': 6, 'y': 12}, {'x': 7, 'y': 12}, {'x': 8, 'y': 12}, {'x': 9, 'y': 12}, {'x': 10, 'y': 12}, {'x': 11, 'y': 12}, {'x': 12, 'y': 12}, {'x': 13, 'y': 12}, {'x': 13, 'y': 11}, {'x': 13, 'y': 10}, {'x': 13, 'y': 9}, {'x': 13, 'y': 8}, {'x': 13, 'y': 7}, {'x': 12, 'y': 7}, {'x': 12, 'y': 8}, {'x': 11, 'y': 8}, {'x': 11, 'y': 7}, {'x': 10, 'y': 7}, {'x': 10, 'y': 7}]}]}, 'you': {'id': '3ed5075d-4314-4627-aea8-7059f1b3a240', 'name': '', 'health': 100, 'body': [{'x': 12, 'y': 10}, {'x': 12, 'y': 11}, {'x': 11, 'y': 11}, {'x': 10, 'y': 11}, {'x': 9, 'y': 11}, {'x': 8, 'y': 11}, {'x': 7, 'y': 11}, {'x': 6, 'y': 11}, {'x': 5, 'y': 11}, {'x': 4, 'y': 11}, {'x': 3, 'y': 11}, {'x': 3, 'y': 12}, {'x': 4, 'y': 12}, {'x': 5, 'y': 12}, {'x': 6, 'y': 12}, {'x': 7, 'y': 12}, {'x': 8, 'y': 12}, {'x': 9, 'y': 12}, {'x': 10, 'y': 12}, {'x': 11, 'y': 12}, {'x': 12, 'y': 12}, {'x': 13, 'y': 12}, {'x': 13, 'y': 11}, {'x': 13, 'y': 10}, {'x': 13, 'y': 9}, {'x': 13, 'y': 8}, {'x': 13, 'y': 7}, {'x': 12, 'y': 7}, {'x': 12, 'y': 8}, {'x': 11, 'y': 8}, {'x': 11, 'y': 7}, {'x': 10, 'y': 7}, {'x': 10, 'y': 7}]}}
H = data['board']['height']
W = data['board']['width']

dt = time.time()
me = snk.Snake(data['you'])
snakes = build_snakes(data, me_id=me.id)
G = graph.Graph(W,H)
G.build_from_data(snakes,me)
d = G.Astar(Loc(0,0), Loc(12,10))
#d = d[1]-d[0]
G._plot()
print(time.time()-dt)

#Loc(3,0) Loc(12,3)

#%%
right = 12
left = 13
forward = 15
size = 15

if right+left+forward <= size*3:
    print("oh no")

if right < size and left < size:
    print("go forward")
elif right < size and forward < size:
    print("go left")
elif left < size and forward < size:
    print("go right")
