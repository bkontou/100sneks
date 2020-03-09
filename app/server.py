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

import app.graph as graph
from app.graph import Loc
import app.snake as snk
from app.fsm import FSM


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
    
    #approaching wall
    if me.head + me.head_direction not in G:
        #choose better path
        #print("")
        #print("%s %s %s" % (me.head, me.head_direction.rotate_90(), me.head_direction.rotate_90(clockwise=True)))
        side1 = G.floodfill(me.head,me.head_direction.rotate_90())
        side2 = G.floodfill(me.head,me.head_direction.rotate_90(clockwise=True))
        #print("%s %s" % (side1,side2))
        if side1 < side2:
            #print("two")
            d = me.head_direction.rotate_90(clockwise=True)
            #d.y = -d.y
            move = dirs[d]
        else:
            #print("one")
            d = me.head_direction.rotate_90()
            #d.y = -d.y
            move = dirs[d]
    else:
        #move based off state
        #d = G.Astar(me.head, food[0])
        
        #assess situation
        params = [0,0,0,0]
        
        #TODO: how to check if hungry
        #Option 1: threshold hunger level; less computation
        #option 2: distance-based hunger; more computation
        
        #going with option 1 as a placeholder
        if me.health < 50:
            #me hungy
            params[0] = True
        else:
            params[0] = False
        
        #food available
        params[1] = G.floodfind(me.head,food)
        #tail available
        params[2] = G.floodfind(me.head,me.tail)
        #other available
        params[3] = G.floodfind(me.head,[s.tail for s in snakes])
        
        #put into binary string
        params_bin = str(int(params[0]))+str(int(params[1]))+str(int(params[2]))+str(int(params[3]))
        #turn binary string into respective base 10 number
        params_bin = int(params_bin,2)
        
        finite_snake_machine.next_state(params_bin)
        d = finite_snake_machine.current_state.action(G, snakes, me, food)
        
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
