# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:45:12 2019
@author: bkontou
"""

try:
    from app.graph import Loc
except:
    from graph import Loc

def to_loc_list(locs):
    loc_list = []
    
    for l in locs:
        loc_list.append(Loc(l['x'],l['y']))
        
    return loc_list

                
class Snake:
    def __init__(self, snake):
        self.id = snake['id']
        self.health = snake['health']
        
        self.body = to_loc_list(snake['body'])
        self.head = self.body[0]
        self.tail = self.body[len(self.body)-1]
        self.head_direction = self.head - self.body[1]
        
        self.size = len(self.body)
    
    def __len__(self):
        return len(self.body)
    
        
