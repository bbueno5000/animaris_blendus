import bpy
import random

print("reset start")

for o in bpy.data.objects:
    if o.type == 'MESH':
         if o.name != "Plane" and o.name != "Plane.001" and o.name != "Plane.002":
           o.location.x = random.randrange(0, 200)
           o.location.y = random.randrange(-100, 100)
           o.location.z = random.randrange(0, 200)

print("reset end")
