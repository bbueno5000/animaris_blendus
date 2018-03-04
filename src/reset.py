# Copyright 2018 Benjamin Bueno (bbueno5000) All Rights Reserved.

import random
import bpy


class Reset2D:

    def __init__(self):
        print("reset start")
        for o in bpy.data.objects:
            if o.type == 'MESH':
                if o.name != "Plane":
                o.location.x = random.randrange(-100, 100)
                o.location.y = random.randrange(-100, 100)
        print("reset end")


class Reset3D:

    def __init__(self):
        print("reset start")
        for o in bpy.data.objects:
            if o.type == 'MESH':
                if o.name != "Plane" and o.name != "Plane.001" and o.name != "Plane.002":
                o.location.x = random.randrange(0, 200)
                o.location.y = random.randrange(-100, 100)
                o.location.z = random.randrange(0, 200)
        print("reset end")
