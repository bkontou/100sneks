#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 11:32:30 2020

@author: byron
"""
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
    
    def action(self, G, snakes, me, food):
        pass
        

class ChaseTail(State):
    
    def __init__(self):
        self.name = "chase_tail"
    
    def choose(self, params):
        if (params & 10) == 2 or (params & 14) == 10:
            #0x1x or 101x
            #next state: chase tail
            return "chase_tail"
        elif (params & 7) == 1 or (params & 15) == 5:
            #x001 0101
            #next state: chase other
            return "chase_other"
        elif (params & 12) == 12:
            #11xx
            #next state: eat
            return "eat"
        elif (params & 11) == 0 or (params & 7) == 0:
            #0x00 or x000
            #next state: serpentine
            return "serpentine"
    
    def action(self, G,snakes,me,food):
        return G.Astar(me.head,me.tail)

class Eat(State):
    
    def __init__(self):
        self.name = "eat"
    
    def choose(self, params):
        if (params & 12) == 12:
            #11xx
            #next state: eat
            return "eat"
        if (params & 10) == 2 or (params & 14) == 10:
            #0x1x or 101x
            #next state: chase tail
            return "chase_tail"
        if (params & 11) == 1 or (params & 15) == 9:
            #0x01 1001
            #next state: chase other
            return "chase_other"
        if (params & 11) == 0 or (params & 7) == 0:
            #0x00 or x000
            #next state: serpentine
            return "serpentine"
        
    def action(self, G,snakes,me,food):
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
        if (params & 11) == 1 or (params & 15) == 9:
            #0x01 or 1001
            #next state: chase other
            return "chase_other"
        if (params & 3) == 2 or (params & 11) == 3 or (params & 15) == 11:
            #xx10 or 0x11 or 1011
            #next state: chase tail
            return "chase_tail"
        if (params & 12) == 12:
            #11xx
            #next state: eat
            return "eat"
        if (params & 11) == 0 or (params & 7) == 0:
            #0x00 or x000
            #next state: serpentine
            return "serpentine"
        
    def action(self, G,snakes,me,food):
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
        if (params & 11) == 0 or (params & 7) == 0:
            #0x00 or x000
            #next state: serpentine
            return "serpentine"
        if (params & 10) == 2 or (params & 15) == 9 or (params & 14) == 10:
            #0x1x 1001 101x
            #next state: chase tail
            return "chase_tail"
        if (params & 12) == 12:
            #11xx 
            #next state: eat
            return "eat"
        if (params & 11) == 1 or (params & 7) == 1:
            #0x01 x001
            #next state: chase_other
            return "chase_other"
        
    def action(self, G,snakes,me,food):
        return G.Astar(me.head, me.tail)
            
class FSM:
    """
    FSM class hard coded for my snake. ssss.
    """
    def __init__(self):
        self.states = {"serpentine":Serpentine(),
                       "chase_tail":ChaseTail(),
                       "chase_other":ChaseOther(),
                       "eat":Eat()}
        
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
    fsm.current_state = fsm.states['chase_tail']
    
    lst = list(itertools.product([0, 1], repeat=4))
    
    errors = []
    
    for i in range(16):
        resp = fsm.current_state.choose(i)
        print(i)
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
    