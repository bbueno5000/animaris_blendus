import bpy
import bge
from random import random
from random import randrange


class AnimarisBlendus:

    def __init__(self):
        self.generation = 1
        self.n_survivors = 9
        self.pop_size = 10
        self.n_divisions = 3    # three for A. Blendus-Duo, four for A. Blendus-Tres

    def genetic_exchange(self):
        print("genetic_exchange start")
        cont = bge.logic.getCurrentController()
        scene = bge.logic.getCurrentScene()
        own = cont.owner
        survivors_file = open(bge.logic.expandPath("//survivors.csv"), 'w')
        gene_file_x = open(bge.logic.expandPath("//x.csv"), 'w')
        gene_file_y = open(bge.logic.expandPath("//y.csv"), 'w')
        num = 1
        object_list = []
        for i in range(self.n_survivors):
            o = scene.objects[i]
            prop_names = o.getPropertyNames()
            survivors_file.write(o.name + "\n")
            gene_file = open(bge.logic.expandPath("//Generation" + self.generation + "\\" + str(num) + ".csv"), 'w')
            gene_file_x.write(str(o[prop_names[0]]) + "\n")
            gene_file_x.write(str(o[prop_names[1]]) + "\n")
            gene_file_x.write(str(o[prop_names[2]]) + "\n")
            gene_file_y.write(str(o[prop_names[3]]) + "\n")
            gene_file_y.write(str(o[prop_names[4]]) + "\n")
            gene_file_y.write(str(o[prop_names[5]]) + "\n")
            for n in prop_names:
                gene_file.write(str(o[n]) + "\n")
                object_list.append(o[n])
            gene_file.close()
            num += 1
        survivors_file.close()
        for i in range(self.pop_size - self.n_survivors):    # for each object
            gene_file = open(bge.logic.expandPath("//Gen1\\" + str(num) + ".txt"), 'w')
            for _ in range(6):    # for each property
                if random() < 0.5:
                    x = randrange(-20, 20)
                    gene_file.write(str(x) + "\n")
                else:
                    x = randrange(0, len(object_list))
                    gene_file.write(str(object_list[x]) + "\n")
            gene_file.close()
            num += 1
        gene_file_x.close()
        gene_file_y.close()
        print("genetic_exchange end")

    def render_images(self, sub_species):
        print("render_images start")
        survivors_file = open(bpy.path.abspath("//Survivors.csv"), 'r')
        survivors_list = []
        for i in range(self.n_survivors):
            survivors_list.append(survivors_file.readline().strip())
        for i in range(1, (self.pop_size + 1)):
            name = "BezierCurve." + str(i)
            if name in survivors_list:
                bpy.data.worlds["World"].horizon_color = (0.7, 0.7, 0.7)
            else:
                bpy.data.worlds["World"].horizon_color = (0.0, 0.0, 0.0)
            bpy.data.objects["Sphere"].data = bpy.data.objects["BezierCurve." + str(i)].data
            bpy.context.scene.render.filepath = ("//" + sub_species + " 3D Population " +
                                                 self.pop_size +  " Generation " +
                                                 self.generation + " BezierCurve " +
                                                 str(i) + ".png")
            bpy.ops.render.render(animation=False,
                                  write_still=True,
                                  use_viewport=False,
                                  layer="10",
                                  scene="Scene")
        print("render_images end")

    def time_limit(self):
        print("time limit reached")
