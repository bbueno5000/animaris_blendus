# MIT License
#
# Copyright (c) 2017 Benjamin Bueno (bbueno5000)

""" 2-Dimensional"""

import random
import bpy

print("reset start")

for o in bpy.data.objects:
    if o.type == 'MESH':
         if o.name != "Plane":
           o.location.x = random.randrange(-100, 100)
           o.location.y = random.randrange(-100, 100)

print("reset end")
