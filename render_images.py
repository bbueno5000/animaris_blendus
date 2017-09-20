import bpy

generation = 1  # change generation
pop_size = 10
survivors = 4

print("render_images start")

survivorsFile = open(bpy.path.abspath("//Survivors.csv"), 'r')

survivorsList = []

for i in range(0, survivors):
     survivorsList.append(survivorsFile.readline().strip())

for i in range(1, (pop_size + 1)):

    name = "Beziercurve." + str(i)

    if name in survivorsList:
        bpy.data.worlds["World"].horizon_color = (0.7, 0.7, 0.7)
    else:
        bpy.data.worlds["World"].horizon_color = (0.0, 0.0, 0.0)


    bpy.data.objects["Sphere"].data = bpy.data.objects["Beziercurve." + str(i)].data

    bpy.context.scene.render.filepath = "//Duo 3D Population " + pop_size +  " Generation " + \
                                         generation + " Beziercurve " + str(i) + ".png"

    bpy.ops.render.render(animation=False,
                          write_still=True,
                          use_viewport=False,
                          layer="10",
                          scene="Scene")

print("render_images end")
