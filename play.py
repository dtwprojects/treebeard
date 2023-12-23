# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:37:14 2023

@author: Vincent.Bevilacqua
"""

import os
import time

for i in range(15):
    with open(f'.\\tframes\\{i}.txt','r') as fil:
        print(fil.read())
    time.sleep(.04)
    os.system('cls')

quit()
