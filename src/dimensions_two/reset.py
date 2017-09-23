"""
    2-Dimensional
"""
import bpy
import random

print("reset start")

for o in bpy.data.objects:
    if o.type == 'MESH':
         if o.name != "Plane":
           o.location.x = random.randrange(-100, 100)
           o.location.y = random.randrange(-100, 100)

print("reset end")
