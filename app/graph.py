#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 14:48:59 2019

@author: byron
"""

try:
    from Queue import Queue
except:
    import queue as Queue
from copy import deepcopy as copy

import numpy as np
#import matplotlib.pyplot as plt
from collections import defaultdict


class Loc:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def update_x(self,n):
        return Loc(self.x + n, self.y)
    
    def update_y(self,n):
        return Loc(self.x, self.y + n)
    
    def dist(self):
        return self.x**2 + self.y**2
    
    def rotate_90(self,clockwise=False):
        if clockwise:
            n = -1
        else:
            n = 1
        
        return Loc(-n*self.y,n*self.x)

    
    def __add__(self, L):
        return Loc(self.x + L.x, self.y + L.y)
    
    def __sub__(self, L):
        return Loc(self.x - L.x, self.y - L.y)
    
    def __str__(self):
        return("Loc(%d,%d)"%(self.x,self.y))

    def __eq__(self, L):
        if self.x == L.x and self.y == L.y:
            return True
        else:
            return False
    
    def __gt__(self,L):
        if self.dist() > L.dist():
            return True
        else:
            return False
    
    def __ls__(self,L):
        if self.dist() < L.dist():
            return True
        else:
            return False
    
    def __gte__(self,L):
        if self.dist() >= L.dist():
            return True
        else:
            return False
    
    def __lse__(self,L):
        if self.dist() <= L.dist():
            return True
        else:
            return False
        
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        return hash((self.x,self.y))

class Graph:
    def __init__(self, W, H, *args, **kwargs):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.width = W
        self.height = H
        """
        give it a matrix representing the map
        """
        
        try:
            if type(args[0]) == np.ndarray:
                self.build(args[0])
            
            if type(kwargs['map']) == np.ndarray:
                self.build(kwargs['map'])
            
        except:
            pass
    
    def add_node(self, node):
        self.nodes.add(node)
    
    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
    
    def add_node_plus_edges(self,node):
        self.nodes.add(node)
        if node.y + 1 < self.height:
            self.add_edge(node,node+Loc(0,1))
        if node.y - 1 >= 0:
            self.add_edge(node,node-Loc(0,1))
        if node.x + 1 < self.width:
            self.add_edge(node,node+Loc(1,0))
        if node.x -1 >= 0:
            self.add_edge(node,node-Loc(1,0))
    
    def remove_edge(self, from_node, to_node):
        removed = copy(self)
        try:
            del removed.edges[from_node]
            del removed.edges[to_node]
        except:
            pass
            #print("edge does not exist")
        return removed
        
    def remove_node_copy(self, node):
        removed = copy(self)
        for E in self.edges[node]:
            removed = removed.remove_edge(node,E)
        try:
            removed.nodes.remove(node)
        except:
            pass
            #print("node does not exist")
        
        return removed
    
    def delete_node(self,node):
        try:
            self.edges[node].clear()
        except:
            print("nodes does not exist")
            pass
            
        try:
            self.nodes.remove(node)
        except:
            pass
            #print("edges do not exist")
        
        try:
            self.edges[node+Loc(0,1)].remove(node)
        except:
            pass
            #print("node %s is not in edges" % node)
            
        try:
            self.edges[node+Loc(0,-1)].remove(node)
        except:
            pass
            #print("node %s is not in edges" % node)
        
        try:
            self.edges[node+Loc(1,0)].remove(node)
        except:
            pass
            #print("node %s is not in edges" % node)
        
        try:
            self.edges[node+Loc(-1,0)].remove(node)
        except:
            pass
            #print("node %s is not in edges" % node)
            
        
    def build_from_map(self,M):
    
        for i, I in enumerate(M):
            for j, J in enumerate(I):
                if M[i,j] != 1:
                    self.add_node(Loc(i,j))
                
        for N in self.nodes:
            i = N.x
            j = N.y
            try:
                if M[i+1,j] != 1:
                    self.add_edge(Loc(i,j),Loc(i+1,j))
            except:
                pass
            
            try:
                if M[i,j+1] != 1:
                    self.add_edge(Loc(i,j),Loc(i,j+1))
            except:
                pass
                
    def build_from_data(self,snakes,me):
        self._zero()
        
        for snake in snakes:
            bodyset = set(snake.body)
            for point in bodyset:
                if point != snake.tail:
                    self.delete_node(point)
                    
            self.delete_node(snake.head+Loc(1,0))
            self.delete_node(snake.head-Loc(1,0))
            self.delete_node(snake.head+Loc(0,1))
            self.delete_node(snake.head-Loc(0,1))
        
        for point in set(me.body):
            if point != me.head and point != me.tail:
                self.delete_node(point)
            
        try: 
            self.edges[me.head].remove(me.tail)
            self.edges[me.tail].remove(me.head)
        except:
            pass

    def floodfind(self, From, L, lis=False):
        Q = Queue.Queue()
        
        if type(L) == type(list()):
            lis = True
        
        if lis:
            if From not in self:
                return False
            for loc in L:
                if loc not in self:
                    return False
        else:
            if From not in self or L not in self:
                return False
    
        Q.put(From)
        to_visit = [From]
        
        while not Q.empty():
            N = Q.get()
            if lis:
                if N in L:
                    return True
            else:
                if N == L:
                    return True
            
            for E in self.edges[N]:
                if E not in to_visit:
                    to_visit.append(E)
                    Q.put(E)
                
        return False
    
    
    def floodfill(self, H, side):
        Q = Queue.Queue()
    
        if H not in self:
            return 0
        
        Q.put(H+side)
        to_visit = [H, H+side]
        n = 0
        
        while not Q.empty():
            N = Q.get()
            n+=1
            
            for E in self.edges[N]:
                if E not in to_visit:
                    to_visit.append(E)
                    Q.put(E)
                
        return n - 1    
    
    def Astar(self, start, end):
        i = 0
        openList = []
        closedList = []
        
        startNode = Node(start.x,start.y)
        
        openList.append(startNode)
        
        while len(openList) > 0:
            i += 1
            if i > (self.width*self.height):
                print("overflow")
                return None
            current = openList[0]
            c_index = 0
            for index, item in enumerate(openList):
                if item.f < current.f:
                    current = item
                    c_index = index
            
            openList.pop(c_index)
            closedList.append(current)
            
            
            if current == end:
                #get path
                path = []
                c = current
                while c is not None:
                    path.append(Loc(c.x,c.y))
                    c = c.parent
                return path[::-1]
            
            children = []
            for node in self.edges[current]:
                children.append(Node(node.x,node.y,parent=current))
            
            for child in children:
                if child in closedList:
                    continue
                
                child.g = current.g + 1
                child.h = (end - child).dist()
                child.f = child.g + child.h
                
                if child in openList:
                    if child.g > openList[openList.index(child)].g:
                        continue
                
                openList.append(child)
        
    def _zero(self):

        for w in range(self.width):
            for h in range(self.height):
                self.add_node(Loc(w,h))
                
        for N in self.nodes:
            if N.x + 1 < self.width:
                self.add_edge(N,N+Loc(1,0))
            if N.y + 1 < self.height:
                self.add_edge(N,N+Loc(0,1))

        
# =============================================================================
#     def _plot(self):
#         nlistx = []
#         nlisty = []
#         for N in self.nodes:
#             nlistx.append(N.x)
#             nlisty.append(self.height - N.y)
#             
#         for N in self.edges:
#             for E in self.edges[N]:
#                 plt.plot([N.x,E.x],[self.height - N.y, self.height - E.y],c='b')
#                 
#         
#         plt.scatter(nlistx,nlisty,c='b')
# =============================================================================

        
    def __contains__(self,L):
        return L in self.nodes
            


class Node(Loc):
    def __init__(self,x,y,parent=None):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        