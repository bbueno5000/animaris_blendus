# MIT License
#
# Copyright (c) 2017 Benjamin Bueno (bbueno5000)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import bpy
import bge
from animaris_blendus import AnimarisBlendus
from random import randrange


class AnimarisBlendusTres(AnimarisBlendus):

    def __init__(self):
        super(AnimarisBlendusTres, self).__init__()
        self.n_divisions = 4
        self.sub_species = "Tres"
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
                                 mirror=False,
                                 proportional='DISABLED',
                                 proportional_edit_falloff='SMOOTH',
                                 proportional_size=1)
        mat_plane = bpy.data.materials.new(name="Material")
        mat_plane.diffuse_color = (0.3, 0.3, 0.6)
        bpy.data.objects["Plane.002"].data.materials.append(mat_plane)
        # create curves
        for i in range(1, (self.pop_size + 1)):
            x = randrange(0, 200)
            y = randrange(-100, 100)
            z = randrange(0, 200)
            bpy.ops.curve.primitive_bezier_curve_add(radius=15,
                                                     view_align=False,
                                                     enter_editmode=True,
                                                     location=(x, y, z),
                                                     layers=(True, False, False, False, False,
                                                             False, False, False, False, False,
                                                             False, False, False, False, False,
                                                             False, False, False, False, False))
            bpy.ops.curve.subdivide(number_cuts=(self.n_divisions - 2))
            for j in range(self.n_divisions):
                bpy.ops.object.game_property_new(type='INT', name="geneX" + str(j))
                bpy.ops.object.game_property_new(type='INT', name="geneY" + str(j))
                # set property values
                x = randrange(-20, 20)
                y = randrange(-20, 20)
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
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object.name = "BezierCurve." + str(i)
            bpy.context.object.data.bevel_object = bpy.data.objects["BezierCircle"]
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.object.convert(target='MESH')
            bpy.context.active_object.data.materials.append(self.mat_object)
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
            for j in range(12):
                sensors[j].use_pulse_true_level = True
                sensors[j].tick_skip = randrange(0, 100)
                sensors[j].seed = randrange(0, 100)
            # linear velocity
            actuators["Motion"].linear_velocity[0] = -25
            actuators["Motion.001"].linear_velocity[0] = 25
            actuators["Motion.002"].linear_velocity[1] = -25
            actuators["Motion.003"].linear_velocity[1] = 25
            actuators["Motion.004"].linear_velocity[2] = -25
            actuators["Motion.005"].linear_velocity[2] = 25
            # angular velocity
            actuators["Motion.006"].angular_velocity[0] = -10
            actuators["Motion.007"].angular_velocity[0] = 10
            actuators["Motion.008"].angular_velocity[1] = -10
            actuators["Motion.009"].angular_velocity[1] = 10
            actuators["Motion.010"].angular_velocity[2] = -10
            actuators["Motion.011"].angular_velocity[2] = 10
            # connect logic bricks
            for j in range(12):
                sensors[j].link(controllers[j])
                actuators[j].link(controllers[j])
            # add logic bricks
            bpy.ops.logic.sensor_add(type='ALWAYS')
            bpy.ops.logic.controller_add(type='LOGIC_AND')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            # set logic bricks
            actuators["Constraint"].limit = 'LOCX'
            actuators["Constraint"].limit_min = 0
            actuators["Constraint"].limit_max = 200
            actuators["Constraint.001"].limit = 'LOCY'
            actuators["Constraint.001"].limit_min = -100
            actuators["Constraint.001"].limit_max = 100
            actuators["Constraint.002"].limit = 'LOCZ'
            actuators["Constraint.002"].limit_min = 0
            actuators["Constraint.002"].limit_max = 200
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
        print("initialization end")

    def collision(self):
        scene = bge.logic.getCurrentScene()
        plane = scene.objects["Plane"]
        plane1 = scene.objects["Plane.001"]
        plane2 = scene.objects["Plane.002"]
        cont = bge.logic.getCurrentController()
        own = cont.owner
        if own.sensors["Ray"].positive:
            if (own.sensors["Collision"].hitObject != plane and
                own.sensors["Collision"].hitObject != plane1 and
                own.sensors["Collision"].hitObject != plane2):
                bge.render.drawLine(own.worldPosition,
                                    own.sensors["Ray"].hitPosition,
                                    (255, 0, 0))
                print("detection")
        if own.sensors["Ray"].positive and own.sensors["Collision"].positive:
            if (own.sensors["Collision"].hitObject != plane and
                own.sensors["Collision"].hitObject != plane1 and
                own.sensors["Collision"].hitObject != plane2):
                print(own.sensors["Collision"].hitObject.name)
                own.sensors["Collision"].hitObject.endObject()
                plane["survivors"] -= 1
                print("collision")

    def reset(self):
        print("reset start")
        for o in bpy.data.objects:
            if o.type == 'MESH':
                if o.name != "Plane" and o.name != "Plane.001" and o.name != "Plane.002":
                    o.location.x = randrange(0, 200)
                    o.location.y = randrange(-100, 100)
                    o.location.z = randrange(0, 200)
        print("reset end")
