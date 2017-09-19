import bge

scene = bge.logic.getCurrentScene()

plane = scene.objects["Plane"]
plane1 = scene.objects["Plane.001"]
plane2 = scene.objects["Plane.002"]

cont = bge.logic.getCurrentController()

own = cont.owner

if own.sensors["Ray"].positive:
    if own.sensors["Collision"].hitObject != plane and own.sensors["Collision"].hitObject != plane1 and own.sensors["Collision"].hitObject != plane2:
        bge.render.drawLine(own.worldPosition, own.sensors["Ray"].hitPosition, (255, 0, 0))
        print("detection")

if own.sensors["Ray"].positive and own.sensors["Collision"].positive:
    if own.sensors["Collision"].hitObject != plane and own.sensors["Collision"].hitObject != plane1 and own.sensors["Collision"].hitObject != plane2:
        print(own.sensors["Collision"].hitObject.name)
        own.sensors["Collision"].hitObject.endObject()
        plane["survivors"] -= 1
        print("collision"
