#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:01:47 2020

@author: byron
"""


#%%

import numpy as np
import matplotlib.pyplot as plt

G = 1.5555555
B = 0.992844
Z = 0.11942
W = 8326.9
T = (180/np.pi)*83.141370863

t = np.linspace(0,0.01,5000)

a = G*(1-(1/B)*np.exp(-1*Z*W*t)*np.sin(W*B*t+T))

plt.grid(True)
plt.plot(t,a,c='k')
plt.xlabel('t (s)')
plt.ylabel('a(t)')