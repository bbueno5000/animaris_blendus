"""
    2-Dimensional
"""
import bge

scene = bge.logic.getCurrentScene()
plane = scene.objects["Plane"]
cont = bge.logic.getCurrentController()
own = cont.owner

if own.sensors["Ray"].positive:
    if own.sensors["Collision"].hitObject != plane:
        bge.render.drawLine(own.worldPosition, own.sensors["Ray"].hitPosition, (255, 0, 0))
        print("detection")

if own.sensors["Ray"].positive and own.sensors["Collision"].positive:
    if own.sensors["Collision"].hitObject != plane:
        print(own.sensors["Collision"].hitObject.name)
        own.sensors["Collision"].hitObject.endObject()
        plane["survivors"] -= 1
        print("collision")
