""" change gen number """
import bpy

print("render_images start")

gen = 1

survivorsFile = open(bpy.path.abspath("//survivors.csv"), 'r')

survivorsList = []

for i in range(0, 9):
     survivorsList.append(survivorsFile.readline().strip())

for i in range(1, 21):

    name = "BezierCurve." + str(i)

    if name in survivorsList:
        bpy.data.worlds["World"].horizon_color = (0.7, 0.7, 0.7)
    else:
        bpy.data.worlds["World"].horizon_color = (0, 0, 0)

    bpy.data.objects["Sphere"].data = bpy.data.objects["BezierCurve." + str(i)].data

    bpy.context.scene.render.filepath = "//duo_3d_pop-20_it-1_gen-" + str(gen) + "_beziercurve-" + str(i) + ".png"

    bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer="10", scene="Scene")

print("render_images end")
