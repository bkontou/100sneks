import json
import os
import random

import time

import bottle
from bottle import HTTPResponse

try:
    from Queue import Queue
except:
    import queue as Queue
from copy import deepcopy as copy

import numpy as np
from collections import defaultdict

try:
    import app.graph as graph
    from app.graph import Loc
    import app.snake as snk
    from app.fsm import FSM
except:
    import graph as graph
    from graph import Loc
    import snake as snk
    from fsm import FSM


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

global dirs
dirs = {Loc(-1,0):'left',Loc(0,1):'down',Loc(1,0):'right',Loc(0,-1):'up'}
global H
global W
global G
global finite_snake_machine


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))
    
    global dirs
    dirs = {Loc(-1,0):'left',Loc(0,1):'down',Loc(1,0):'right',Loc(0,-1):'up'}
    global H
    global W
    global G
    global finite_snake_machine
    
    print(dirs)
    
    
    H, W = data["board"]["height"], data["board"]["width"]
    G = graph.Graph(W,H)
    
    finite_snake_machine = FSM()

    response = {"color": "#ffccff", "smile": "regular", "tailType": "round-bum"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    t = time.time()
    
    data = bottle.request.json

    # Choose a random direction to move in
    global dirs
    global H
    global W
    global finite_snake_machine
    H, W = data["board"]["height"], data["board"]["height"]
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
        
    me = snk.Snake(data['you'])
    snakes = build_snakes(data, me_id=me.id)
    
    food = to_loc_list(data["board"]["food"])

    G = graph.Graph(H,W)
    G.build_from_data(snakes, me)
    
    d = None
    #state parameters
    params = [0,0,0,0,0,0]
    
    #approaching wall
    forward = G.floodfill(me.head, me.head_direction)
    left = G.floodfill(me.head,me.head_direction.rotate_90())
    right = G.floodfill(me.head,me.head_direction.rotate_90(clockwise=True))
    
    for snake in snakes:
        if me.head.square_dist(snake.head) == 2:
            #snake head in the freaking way
            if finite_snake_machine.current_state.name != 'kill':
                params[5] = True
            if me.size > snake.size:
                #we can go head to freakin head
                d = G.Astar(me.head,snake.head)
                move = dirs[d[1]-d[0]]
                break
            
        
    #TODO: figure out how to get this to work: approaching wall shit
    if right+left+forward < 3*me.size:
        #go in direction of largest area
        if right >= left and right >= forward:
            d = me.head_direction.rotate_90(clockwise=True)
            move = dirs[d]
        elif left >= right and left >= forward:
            d = me.head_direction.rotate_90()
            move = dirs[d]
        elif forward >= right and forward >= left:
            d = me.head_direction
            move = dirs[d]
    else:
        if right < me.size and left < me.size:
            d = me.head_direction
            move = dirs[d]
        elif right < me.size and forward < me.size:
            d = me.head_direction.rotate_90()
            move = dirs[d]
        elif left < me.size and forward < me.size:
            d = me.head_direction.rotate_90(clockwise=True)
            move = dirs[d]
    
    if type(d) == type(None):
        #move based off state
        #d = G.Astar(me.head, food[0])
        
        #assess situation
        
        #TODO: how to check if hungry
        #Option 1: threshold hunger level; less computation
        #option 2: distance-based hunger; more computation
        
        #going with option 1 as a placeholder
        if me.health < 50:
            #me hungy
            params[0] = True
        else:
            params[0] = False
            
        to_kill = None
        if me.health >= 50:
            for snake in snakes:
                if G.floodfind(me.head,snake.head):
                    params[1] = True
                    to_kill = snake
        
        #food available
        params[2] = G.floodfind(me.head,food)
        #tail available
        params[3] = G.floodfind(me.head,me.tail)
        #other available
        params[4] = G.floodfind(me.head,[s.tail for s in snakes])
        
        
        #put into binary string
        params_bin = str(int(params[0]))+str(int(params[1]))+str(int(params[2]))+str(int(params[3]))+str(int(params[4]))+str(int(params[5]))
        #turn binary string into respective base 10 number
        print(params_bin)
        params_bin = int(params_bin,2)
        
        finite_snake_machine.next_state(params_bin)
        print(finite_snake_machine.current_state)
        
        #take action
        d = finite_snake_machine.current_state.action(G, snakes, me, food, to_kill)
        
        if d == None:
            #find tail
            d = G.Astar(me.head, me.tail)
    
        
        #TODO:
        #the first few turns the snake tries to chase its tail, but its tail
        #is inside its body, so it collides with itself
        if type(d) == type(None):
            move = dirs[me.head_direction]
        else:
            if len(d) <= 1:
                move = 'up'
            else:
                move = dirs[d[1]-d[0]]
    #TODO: handle if location is none
    


    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"
    
    print(time.time()-t)

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
