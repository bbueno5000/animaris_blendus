import bpy
import bge
from random import random
from random import randrange


class AnimarisBlendus:

    def __init__(self):
        self.generation = 1
        self.n_survivors = 9
        self.pop_size = 10
        print("initialization start")
        # set horizon color
        bpy.data.worlds["World"].horizon_color = (0.25, 0.25, 0.25)
        bpy.context.scene.game_settings.physics_gravity = 0
        # construct plane
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                         view_align=False,
                                         enter_editmode=False,
                                         location=(100, 0, 0),
                                         layers=(True, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False))
        mat_plane = bpy.data.materials.new(name="Material")
        mat_plane.diffuse_color = (0.6, 0.3, 0.3)
        bpy.data.objects["Plane"].data.materials.append(mat_plane)
        # add survivors property
        bpy.ops.object.game_property_new(type='INT', name="survivors")
        bpy.context.active_object.game.properties["survivors"].value = self.pop_size
        bpy.context.active_object.game.properties["survivors"].show_debug = True
        # add timer property
        bpy.ops.object.game_property_new(type='TIMER', name='timer')
        bpy.context.active_object.game.properties["timer"].show_debug = True
        # access logic bricks
        sensors =  bpy.context.object.game.sensors
        controllers =  bpy.context.object.game.controllers
        actuators =  bpy.context.object.game.actuators
        # add logic bricks
        bpy.ops.logic.sensor_add(type='PROPERTY')
        bpy.ops.logic.controller_add(type='PYTHON')
        bpy.ops.logic.controller_add(type='LOGIC_AND')
        bpy.ops.logic.actuator_add(type='GAME')
        # set logic bricks
        sensors["Property"].evaluation_type = 'PROPGREATERTHAN'
        sensors["Property"].property = "timer"
        sensors["Property"].value = "120"
        controllers["Python"].text = bpy.data.texts["time_limit.py"]
        actuators["Game"].mode = 'QUIT'
        # connect logic bricks
        sensors["Property"].link(controllers["Python"])
        sensors["Property"].link(controllers["And"])
        actuators["Game"].link(controllers["And"])
        # add logic bricks
        bpy.ops.logic.sensor_add(type='PROPERTY')
        bpy.ops.logic.controller_add(type='PYTHON')
        bpy.ops.logic.controller_add(type='LOGIC_AND')
        # set logic bricks
        sensors["Property.001"].evaluation_type = 'PROPLESSTHAN'
        sensors["Property.001"].property = "survivors"
        sensors["Property.001"].value = self.n_survivors + 1
        controllers["Python.001"].text = bpy.data.texts["genetic_exchange.py"]
        # connect logic bricks
        sensors["Property.001"].link(controllers["Python.001"])
        sensors["Property.001"].link(controllers["And.001"])
        actuators["Game"].link(controllers["And.001"])
        # create extra curve to satisfy naming scheme
        bpy.ops.curve.primitive_bezier_circle_add(view_align=False,
                                                  enter_editmode=False,
                                                  location=(0, 0, 0),
                                                  layers=(True, False, False, False, False,
                                                          False, False, False, False, False,
                                                          False, False, False, False, False,
                                                          False, False, False, False, False))
        bpy.ops.curve.primitive_bezier_curve_add(view_align=False,
                                                 enter_editmode=False,
                                                 location=(0, 0, -10),
                                                 layers=(True, False, False, False, False,
                                                         False, False, False, False, False,
                                                         False, False, False, False, False,
                                                         False, False, False, False, False))

        # create object material
        mat_object = bpy.data.materials.new(name="Material")
        mat_object.diffuse_color = (0.03, 0.03, 0.03)

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

    def reproduction(self):
        print("reproduction start")
        # set horizon color
        bpy.data.worlds["World"].horizon_color = (0.55, 0.55, 0.55)
        bpy.context.scene.game_settings.physics_gravity = 0
        # construct plane
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                         view_align=False,
                                         enter_editmode=False,
                                         location=(100, 0, 0),
                                         layers=(True, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False))
        mat_plane = bpy.data.materials.new(name="Material")
        mat_plane.diffuse_color = (0.6, 0.3, 0.3)
        bpy.data.objects["Plane"].data.materials.append(mat_plane)
        # add survivors property
        bpy.ops.object.game_property_new(type='INT',name="survivors")
        bpy.context.active_object.game.properties["survivors"].value = self.n_survivors
        bpy.context.active_object.game.properties["survivors"].show_debug = True
        # add timer property
        bpy.ops.object.game_property_new(type='TIMER',name="timer")
        bpy.context.active_object.game.properties["timer"].show_debug = True
        # access logic bricks
        sensors =  bpy.context.object.game.sensors
        controllers =  bpy.context.object.game.controllers
        actuators =  bpy.context.object.game.actuators
        # add logic bricks
        bpy.ops.logic.sensor_add(type='PROPERTY')
        bpy.ops.logic.controller_add(type='PYTHON')
        bpy.ops.logic.controller_add(type='LOGIC_AND')
        bpy.ops.logic.actuator_add(type='GAME')
        # set logic bricks
        sensors["Property"].evaluation_type = 'PROPGREATERTHAN'
        sensors["Property"].property = "timer"
        sensors["Property"].value = "120"
        controllers["Python"].text = bpy.data.texts["time_limit.py"]
        actuators["Game"].mode = 'QUIT'
        # connect logic bricks
        sensors["Property"].link(controllers["Python"])
        sensors["Property"].link(controllers["And"])
        actuators["Game"].link(controllers["And"])
        # add logic bricks
        bpy.ops.logic.sensor_add(type='PROPERTY')
        bpy.ops.logic.controller_add(type='PYTHON')
        bpy.ops.logic.controller_add(type='LOGIC_AND')
        # set logic bricks
        sensors["Property.001"].evaluation_type = 'PROPLESSTHAN'
        sensors["Property.001"].property = "survivors"
        sensors["Property.001"].value = self.n_survivors + 1
        controllers["Python.001"].text = bpy.data.texts["genetic_exchange.py"]
        # connect logic bricks
        sensors["Property.001"].link(controllers["Python.001"])
        sensors["Property.001"].link(controllers["And.001"])
        actuators["Game"].link(controllers["And.001"])
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                         view_align=False,
                                         enter_editmode=False,
                                         location=(0, 0, 100),
                                         layers=(True, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False))
        bpy.ops.transform.rotate(value=1.5708,
                                 axis=(0, 1, 0),
                                 constraint_axis=(False, True, False),
                                 constraint_orientation='GLOBAL',
                                 mirror=False,
                                 proportional='DISABLED',
                                 proportional_edit_falloff='SMOOTH',
                                 proportional_size=1)
        mat_plane = bpy.data.materials.new(name="Material")
        mat_plane.diffuse_color = (0.3, 0.6, 0.3)
        bpy.data.objects["Plane.001"].data.materials.append(mat_plane)
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                         view_align=False,
                                         enter_editmode=False,
                                         location=(100, 100, 100),
                                         layers=(True, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False,
                                                 False, False, False, False, False))
        bpy.ops.transform.rotate(value=1.5708,
                                 axis=(1, 0, 0),
                                 constraint_axis=(True, False, False),
                                 constraint_orientation='GLOBAL',
                                 mirror=False, proportional='DISABLED',
                                 proportional_edit_falloff='SMOOTH',
                                 proportional_size=1)
        mat_plane = bpy.data.materials.new(name="Material")
        mat_plane.diffuse_color = (0.3, 0.3, 0.6)
        bpy.data.objects["Plane.002"].data.materials.append(mat_plane)
        # create extra curve to satisfy naming scheme
        bpy.ops.curve.primitive_bezier_circle_add(view_align=False,
                                                  enter_editmode=False,
                                                  location=(0, 0, 0),
                                                  layers=(True, False, False, False, False,
                                                          False, False, False, False, False,
                                                          False, False, False, False, False,
                                                          False, False, False, False, False))
        bpy.ops.curve.primitive_bezier_curve_add(view_align=False,
                                                 enter_editmode=False,
                                                 location=(0, 0, -10),
                                                 layers=(True, False, False, False, False,
                                                         False, False, False, False, False,
                                                         False, False, False, False, False,
                                                         False, False, False, False, False))
        # create object material
        mat_object = bpy.data.materials.new(name="Material")
        mat_object.diffuse_color = (0.03, 0.03, 0.03)
        # create curves
        for i in range(1, (self.pop_size + 1)):
            x = randrange(0, 200)
            y = randrange(-100, 100)
            bpy.ops.curve.primitive_bezier_curve_add(radius=15,
                                                     view_align=False,
                                                     enter_editmode=True,
                                                     location=(x, y, 0),
                                                     layers=(True, False, False, False, False,
                                                             False, False, False, False, False,
                                                             False, False, False, False, False,
                                                             False, False, False, False, False))
            bpy.ops.curve.subdivide(number_cuts=(self.n_divisions - 2))
            file = open(bpy.path.abspath("//" + str(i) + ".txt"), 'r')
            for j in range(self.n_divisions):
                bpy.ops.object.game_property_new(type='INT', name="geneX" + str(j))
                bpy.ops.object.game_property_new(type='INT', name="geneY" + str(j))
                # set property values
                x = int(file.readline())
                y = int(file.readline())
                bpy.context.active_object.game.properties["geneX" + str(j)].value = x
                bpy.context.active_object.game.properties["geneY" + str(j)].value = y
                # set coordinate values for bezier points
                bpy.context.active_object.data.splines[0].bezier_points[j].select_control_point = True
                bpy.ops.transform.translate(value=(x, y, 0),
                                            constraint_axis=(True, True, False),
                                            constraint_orientation='GLOBAL',
                                            mirror=False,
                                            proportional='DISABLED',
                                            proportional_edit_falloff='SMOOTH',
                                            proportional_size=1)
                bpy.context.active_object.data.splines[0].bezier_points[j].select_control_point = False
            file.close()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object.name = "BezierCurve." + str(i)
            bpy.context.object.data.bevel_object = bpy.data.objects["BezierCircle"]
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.object.convert(target='MESH')
            bpy.context.active_object.data.materials.append(mat_object)
            bpy.context.object.game.physics_type = 'DYNAMIC'
            bpy.context.object.game.use_collision_bounds = True
            bpy.context.object.game.collision_bounds_type = 'CONVEX_HULL'
            bpy.data.objects["BezierCurve." + str(i)].select = False
            # access logic bricks
            sensors =  bpy.context.object.game.sensors
            controllers =  bpy.context.object.game.controllers
            actuators =  bpy.context.object.game.actuators
            # add logic bricks
            for j in range(12):
                bpy.ops.logic.sensor_add(type='RANDOM')
                bpy.ops.logic.controller_add(type='LOGIC_AND')
                bpy.ops.logic.actuator_add(type='MOTION')
            # set logic bricks
            for j in range(8):
                sensors[j].use_pulse_true_level = True
                sensors[j].tick_skip = randrange(0, 100)
                sensors[j].seed = randrange(0, 100)
            # linear velocity
            actuators["Motion"].linear_velocity[0] = -25
            actuators["Motion.001"].linear_velocity[0] = 25
            actuators["Motion.002"].linear_velocity[1] = -25
            actuators["Motion.003"].linear_velocity[1] = 25
            # angular velocity
            actuators["Motion.004"].angular_velocity[0] = -10
            actuators["Motion.005"].angular_velocity[0] = 10
            actuators["Motion.006"].angular_velocity[1] = -10
            actuators["Motion.007"].angular_velocity[1] = 10
            # connect logic bricks
            for j in range(8):
                sensors[j].link(controllers[j])
                actuators[j].link(controllers[j])
            # add logic bricks
            bpy.ops.logic.sensor_add(type='ALWAYS')
            bpy.ops.logic.controller_add(type='LOGIC_AND')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')    # set logic bricks
            actuators["Constraint"].limit = 'LOCX'
            actuators["Constraint"].limit_min = -100
            actuators["Constraint"].limit_max = 100
            actuators["Constraint.001"].limit = 'LOCY'
            actuators["Constraint.001"].limit_min = -100
            actuators["Constraint.001"].limit_max = 100
            # connect logic bricks
            sensors["Always"].link(controllers["And.012"])
            actuators["Constraint"].link(controllers["And.012"])
            actuators["Constraint.001"].link(controllers["And.012"])
            actuators["Constraint.002"].link(controllers["And.012"])
            # add logic bricks
            bpy.ops.logic.sensor_add(type='COLLISION')
            bpy.ops.logic.sensor_add(type='RAY')
            bpy.ops.logic.sensor_add(type='RAY')
            bpy.ops.logic.controller_add(type='PYTHON')
            # set logic bricks
            sensors["Ray"].axis = 'XAXIS'
            sensors["Ray"].range = 30
            sensors["Ray.001"].axis = 'NEGXAXIS'
            sensors["Ray.001"].range = 30
            controllers["Python"].text = bpy.data.texts["collision.py"]
            # connect logic bricks
            sensors["Collision"].link(controllers["Python"])
            sensors["Ray"].link(controllers["Python"])
            sensors["Ray.001"].link(controllers["Python"])
        # delete extra curve
        bpy.data.objects["BezierCurve"].select = True
        bpy.ops.object.delete(use_global=False)
        print("reproduction end")

    def time_limit(self):
        print("time limit reached")
