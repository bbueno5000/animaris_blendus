import bpy

GENERATION = 1
POP_SIZE = 10
N_SURVIVORS = 4

print("render_images start")

survivorsFile = open(bpy.path.abspath("//Survivors.csv"), 'r')

survivorsList = []

for i in range(0, N_SURVIVORS):
     survivorsList.append(survivorsFile.readline().strip())

for i in range(1, (POP_SIZE + 1)):

    name = "Beziercurve." + str(i)

    if name in survivorsList:
        bpy.data.worlds["World"].horizon_color = (0.7, 0.7, 0.7)
    else:
        bpy.data.worlds["World"].horizon_color = (0.0, 0.0, 0.0)


    bpy.data.objects["Sphere"].data = bpy.data.objects["Beziercurve." + str(i)].data

    bpy.context.scene.render.filepath = "//Duo 3D Population " + POP_SIZE +  " Generation " + \
                                         GENERATION + " Beziercurve " + str(i) + ".png"

    bpy.ops.render.render(animation=False,
                          write_still=True,
                          use_viewport=False,
                          layer="10",
                          scene="Scene")

print("render_images end")
