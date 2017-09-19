import bpy
    
print("render_images start") 

gen = 1  # change generation

survivorsFile = open(bpy.path.abspath("//survivors.txt"), 'r')   

survivorsList = []

for i in range(0, 4):
     survivorsList.append(survivorsFile.readline().strip())
        
for i in range(1, 11):     
    name = "BezierCurve." + str(i)     
    
    if name in survivorsList:
        bpy.data.worlds["World"].horizon_color = (0.7, 0.7, 0.7)
    else: 
        bpy.data.worlds["World"].horizon_color = (0, 0, 0)     
                  
    bpy.data.objects["Sphere"].data = bpy.data.objects["BezierCurve." + str(i)].data
    
    bpy.context.scene.render.filepath = "//Duo 3D Pop10 Gen0 Bezier Curve " + str(i) + ".png"

    bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer="10", scene="Scene")

print("render_images end")
