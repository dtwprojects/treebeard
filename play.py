# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:37:14 2023

@author: Vincent.Bevilacqua
"""

import os

for i in range(123):
    with open(f'..\\tframes\\{i}.txt','r') as fil:
        print(fil.read())
    os.system('cls')

quit()
