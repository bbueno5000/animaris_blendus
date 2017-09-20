import bpy
import random

N_DIMENSIONS = 2

print("reset start")

for o in bpy.data.objects:
    if o.type == 'MESH':
         if o.name != "Plane" and o.name != "Plane.001" and o.name != "Plane.002":
           o.location.x = random.randrange(0, 200)
           o.location.y = random.randrange(-100, 100)

           if N_DIMENSIONS == 3:
               o.location.z = random.randrange(0, 200)

print("reset end")
