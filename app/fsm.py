#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 11:32:30 2020

@author: byron
"""

try:
    from app.graph import Loc
except:
    from graph import Loc

def chase_tail(G):
    print("ok")
    
def eat(G):
    print("boomer")

def chase_other(G):
    print("whatever you say")
    
def serpentine(G):
    print("boomer")
    
class State:
    def __init__(self):
        self.name = ""
    
    def choose(State):
        pass
    
    def action(self, G, snakes, me, food, to_kill):
        pass
        

class ChaseTail(State):
    
    def __init__(self):
        self.name = "chase_tail"
    
    def choose(self, params):
        if (params & 37) == 4 or (params & 45) == 36:
            #0xx1x0 or 1x01x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 39) == 2 or (params & 47) == 34:
            #0xx010 1x0010
            #next state: chase other
            return "chase_other"
        elif (params & 41) == 40:
            #1x1xx0
            #next state: eat
            return "eat"
        elif (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 49) == 16:
            #01xxx0
            return "kill"
    
    def action(self, G,snakes,me,food,to_kill):
        return G.Astar(me.head,me.tail)

class Eat(State):
    
    def __init__(self):
        self.name = "eat"
    
    def choose(self, params):
        if (params & 41) == 40:
            #1x1xx0
            return "eat"
        elif (params & 5) == 4  or (params & 61) == 36:
            #xxx1x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 23) == 2:
            #x0x010
            #next state: chase other
            return "chase_other"
        elif (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 17) == 16:
            #x1xxx0
            return "kill"
        
    def action(self, G,snakes,me,food,to_kill):
        minf = (None,1000)
        for f in food:
            d = G.Astar(me.head,f)
            try:
                if len(d) < minf[1]:
                    minf = (d,len(d))
            except:
                pass
        
        return minf[0]
        
class ChaseOther(State):
    
    def __init__(self):
        self.name = "chase_other"
    
    def choose(self, params):
        if (params & 7) == 2:
            #xxx010
            #next state: chase other
            return "chase_other"
        elif (params & 5) == 4:
            #xxx1x0 1001x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 41) == 40:
            #1x1xx0
            #next state: eat
            return "eat"
        elif (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 49) == 16:
            #01xxx0
            return "kill"
        
    def action(self, G,snakes,me,food,to_kill):
        mins = (None,1000)
        for snake in snakes:
            d = G.Astar(me.head,snake.tail)
            try:
                if len(d) < mins[1]:
                    mins = (d,len(d))
            except:
                pass
        
        return mins[0]
                
        
class Serpentine(State):
    
    def __init__(self):
        self.name = "serpentine"
    
    def choose(self, params):
        if (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 5) == 4:
            #xxx1x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 41) == 40:
            #1x1xx0
            #next state: eat
            return "eat"
        elif (params & 7) == 2:
            #xxx010
            #next state: chase_other
            return "chase_other"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 49) == 16:
            #01xxx0
            return "kill"
        
    def action(self, G,snakes,me,food):
        return G.Astar(me.head, me.tail,to_kill)
            
    
class Kill(State):
    
    def __init__(self):
        self.name = "kill"
        
    def choose(self, params):
        if (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 5) == 4:
            #xxx1x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 41) == 40:
            #1x1xx0
            #next state: eat
            return "eat"
        elif (params & 23) == 2:
            #x0x010
            #next state: chase_other
            return "chase_other"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 17) == 16:
            #x1xxx0
            return "kill"
        
        def action(self, G,snakes,me,food,to_kill):
            
            to_check = to_kill.head_direction.rotate_90()*2
            if to_check in G:
                return G.Astar(me.head, to_check)
            to_check += to_kill.head_direction
            if to_check in G:
                return G.Astar(me.head, to_check)
            to_check += to_kill.head_direction
            if to_check in G:
                return G.Astar(me.head, to_check)
            to_check = to_kill.head_direction.rotate_90() + to_kill.head_direction*2
            if to_check in G:
                return G.Astar(me.head, to_check)
            to_check = to_kill.head_direction*2
            if to_check in G:
                return G.Astar(me.head, to_check)
        

class Run(State):
    
    def __init__(self):
        self.name = "run"
    
    def choose(self, params):
        if (params & 7) == 0 or (params & 47) == 32:
            #xxx000 or 1x0000
            #next state: serpentine
            return "serpentine"
        elif (params & 5) == 4:
            #xxx1x0
            #next state: chase tail
            return "chase_tail"
        elif (params & 41) == 40:
            #1x1xx0
            #next state: eat
            return "eat"
        elif (params & 23) == 2:
            #x0x010
            #next state: chase_other
            return "chase_other"
        elif (params & 1) == 1:
            #xxxxxx1
            return "run"
        elif (params & 17) == 16:
            #x1xxx0
            return "kill"
        
    
    def action(self, G,snakes,me,food,to_kill):
        #find a safe place to *DUN DUN* RUN AWAY
        
        #TODO: make this better
        for snake in snakes:
            if me.head.square_dist(snake.head) == 2:
                #direction away from snake
                d = me.head - snake.head
        
        d = G.Astar(me.head, me.head + d)

class FSM:
    """
    FSM class hard coded for my snake. ssss.
    """
    def __init__(self):
        self.states = {"serpentine":Serpentine(),
                       "chase_tail":ChaseTail(),
                       "chase_other":ChaseOther(),
                       "eat":Eat(),
                       "kill":Kill(),
                       "run":Run()}
        
        #initialize state
        self.current_state = self.states["chase_tail"]
        
    def next_state(self, params):
        self.current_state = self.states[self.current_state.choose(params)]

#%%

#test case 
if __name__=='__main__':
    import itertools
    #test for chase_tail
    fsm = FSM()
    fsm.current_state = fsm.states['run']
    
    lst = list(itertools.product([0, 1], repeat=6))
    
    errors = []
    
    for i in range(64):
        resp = fsm.current_state.choose(i)
        if type(resp) == type(None):
            errors.append(bin(i))
# =============================================================================
#     import time
# 
# #%%
#     #0x1x
#     params = (False,False,True,True)
# 
#     dt = time.time()
#     
#     if not params[0] and params[2]:
#         pass
#     elif not params[0] and not params[4]:
#         pass
#     elif not params[0] and params[2]:
#         print(time.time()-dt)
#  
# #%%       
#     params = int('0011',2)
# 
#     dt = time.time()
#     if not(params & 1) and (params & 2):
#         pass
#     elif (params & 8) and not(params & 1):
#         pass
#     elif not(params & 8) and (params & 2):
#         print(time.time()-dt)
#         
#     
#     
# =============================================================================
    