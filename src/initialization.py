# Copyright 2018 Benjamin Bueno (bbueno5000) All Rights Reserved.

import random
import bpy


N_DIVISIONS = 3  # three for A. Blendus-Duo, four for A. Blendus-Tres
N_SURVIVORS = 9
POP_SIZE = 20


class initialization2D:

    def __init__(self):
        print("initialization start")
        # set horizon color
        bpy.data.worlds["World"].horizon_color = (0.25, 0.25, 0.25)
        bpy.context.scene.game_settings.physics_gravity = 0
        # construct plane
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                        view_align=False,
                                        enter_editmode=False,
                                        location=(100, 0, 0),
                                        layers=(True, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False,
                                                False, False, False, False, False, False))

        matPlane = bpy.data.materials.new(name="Material")
        matPlane.diffuse_color = (0.6, 0.3, 0.3)
        bpy.data.objects["Plane"].data.materials.append(matPlane)
        # add survivors property
        bpy.ops.object.game_property_new(type='INT',name="survivors")
        bpy.context.active_object.game.properties["survivors"].value = POP_SIZE
        bpy.context.active_object.game.properties["survivors"].show_debug = True
        # add timer property
        bpy.ops.object.game_property_new(type='INT',name='timer')
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
        sensors["Property.001"].value = N_SURVIVORS + 1
        controllers["Python.001"].text = bpy.data.texts["genetic_exchange.py"]
        # connect logic bricks
        sensors["Property.001"].link(controllers["Python.001"])
        sensors["Property.001"].link(controllers["And.001"])
        actuators["Game"].link(controllers["And.001"])

        # create extra curve to satisfy naming scheme
        bpy.ops.curve.primitive_bezier_circle_add(view_align=False,
                                                enter_editmode=False,
                                                location=(0, 0, 0),
                                                layers=(True, False, False, False, False, False, False, False,
                                                        False, False, False, False, False, False, False, False,
                                                        False, False, False, False))

        bpy.ops.curve.primitive_bezier_curve_add(view_align=False,
                                                enter_editmode=False,
                                                location=(0, 0, -10),
                                                layers=(True, False, False, False, False, False, False, False,
                                                        False, False, False, False, False, False, False, False,
                                                        False, False, False, False))
        # create object material
        matObject = bpy.data.materials.new(name="Material")
        matObject.diffuse_color = (0.03, 0.03, 0.03)
        # create curves
        for i in range(1, (POP_SIZE + 1)):
            x = random.randrange(-100, 100)
            y = random.randrange(-100, 100)
            bpy.ops.curve.primitive_bezier_curve_add(radius=15,
                                                    view_align=False,
                                                    enter_editmode=True,
                                                    location=(x, y, 0),
                                                    layers=(True, False, False, False, False, False, False, False,
                                                            False, False, False, False, False, False, False, False,
                                                            False, False, False, False))

            bpy.ops.curve.subdivide(number_cuts=(N_DIVISIONS - 2))

            for j in range(0, N_DIVISIONS):
                bpy.ops.object.game_property_new(type='INT',name="geneX" + str(j))
                bpy.ops.object.game_property_new(type='INT',name="geneY" + str(j))
                # set property values
                x = random.randrange(-20, 20)
                y = random.randrange(-20, 20)
                bpy.context.active_object.game.properties['geneX' + str(j)].value = x
                bpy.context.active_object.game.properties['geneY' + str(j)].value = y
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
            bpy.context.active_object.data.materials.append(matObject)
            bpy.context.object.game.physics_type = 'DYNAMIC'
            bpy.context.object.game.use_collision_bounds = True
            bpy.context.object.game.collision_bounds_type = 'CONVEX_HULL'
            bpy.data.objects["BezierCurve." + str(i)].select = False
            # access logic bricks
            sensors =  bpy.context.object.game.sensors
            controllers =  bpy.context.object.game.controllers
            actuators =  bpy.context.object.game.actuators
            # add logic bricks
            for j in range(0, 12):
                bpy.ops.logic.sensor_add(type='RANDOM')
                bpy.ops.logic.controller_add(type='LOGIC_AND')
                bpy.ops.logic.actuator_add(type='MOTION')
            # set logic bricks
            for j in range(0, 8):
                sensors[j].use_pulse_true_level = True
                sensors[j].tick_skip = random.randrange(0, 100)
                sensors[j].seed = random.randrange(0, 100)
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
            for j in range(0, 8):
                sensors[j].link(controllers[j])
                actuators[j].link(controllers[j])
            # add logic bricks
            bpy.ops.logic.sensor_add(type='ALWAYS')
            bpy.ops.logic.controller_add(type='LOGIC_AND')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            # set logic bricks
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


class Initialization3D:

    def __init__(self):
        print("initialization start")
        # set horizon color
        bpy.data.worlds["World"].horizon_color = (0.25, 0.25, 0.25)
        bpy.context.scene.game_settings.physics_gravity = 0
        # construct plane
        bpy.ops.mesh.primitive_plane_add(radius=100,
                                        view_align=False,
                                        enter_editmode=False,
                                        location=(100, 0, 0),
                                        layers=(True, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False,
                                                False, False, False, False, False, False))

        matPlane = bpy.data.materials.new(name="Material")
        matPlane.diffuse_color = (0.6, 0.3, 0.3)
        bpy.data.objects["Plane"].data.materials.append(matPlane)
        # add survivors property
        bpy.ops.object.game_property_new(type='INT',name="survivors")
        bpy.context.active_object.game.properties["survivors"].value = POP_SIZE
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
        sensors["Property.001"].value = N_SURVIVORS + 1
        controllers["Python.001"].text = bpy.data.texts["genetic_exchange.py"]
        # connect logic bricks
        sensors["Property.001"].link(controllers["Python.001"])
        sensors["Property.001"].link(controllers["And.001"])
        actuators["Game"].link(controllers["And.001"])

        bpy.ops.mesh.primitive_plane_add(radius=100,
                                        view_align=False,
                                        enter_editmode=False,
                                        location=(0, 0, 100),
                                        layers=(True, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False,
                                                False, False, False, False, False, False))
        bpy.ops.transform.rotate(value=1.5708,
                                axis=(0, 1, 0),
                                constraint_axis=(False, True, False),
                                constraint_orientation='GLOBAL',
                                mirror=False,
                                proportional='DISABLED',
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=1)

        matPlane = bpy.data.materials.new(name="Material")
        matPlane.diffuse_color = (0.3, 0.6, 0.3)
        bpy.data.objects["Plane.001"].data.materials.append(matPlane)

        bpy.ops.mesh.primitive_plane_add(radius=100,
                                        view_align=False,
                                        enter_editmode=False,
                                        location=(100, 100, 100),
                                        layers=(True, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False,
                                                False, False, False, False, False, False))

        bpy.ops.transform.rotate(value=1.5708,
                                axis=(1, 0, 0),
                                constraint_axis=(True, False, False),
                                constraint_orientation='GLOBAL',
                                mirror=False,
                                proportional='DISABLED',
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=1)

        matPlane = bpy.data.materials.new(name="Material")
        matPlane.diffuse_color = (0.3, 0.3, 0.6)
        bpy.data.objects["Plane.002"].data.materials.append(matPlane)

        # create extra curve to satisfy naming scheme
        bpy.ops.curve.primitive_bezier_circle_add(view_align=False,
                                                enter_editmode=False,
                                                location=(0, 0, 0),
                                                layers=(True, False, False, False, False, False, False,
                                                        False, False, False, False, False, False, False,
                                                        False, False, False, False, False, False))
        bpy.ops.curve.primitive_bezier_curve_add(view_align=False,
                                                enter_editmode=False,
                                                location=(0, 0, -10),
                                                layers=(True, False, False, False, False, False, False,
                                                        False, False, False, False, False, False, False,
                                                        False, False, False, False, False, False))
        # create object material
        matObject = bpy.data.materials.new(name="Material")
        matObject.diffuse_color = (0.03, 0.03, 0.03)
        # create curves
        for i in range(1, (POP_SIZE + 1)):
            x = random.randrange(0, 200)
            y = random.randrange(-100, 100)
            z = random.randrange(0, 200)
            bpy.ops.curve.primitive_bezier_curve_add(radius=15,
                                                    view_align=False,
                                                    enter_editmode=True,
                                                    location=(x, y, z),
                                                    layers=(True, False, False, False, False, False, False,
                                                            False, False, False, False, False, False, False,
                                                            False, False, False, False, False, False))

            bpy.ops.curve.subdivide(number_cuts=(N_DIVISIONS - 2))

            for j in range(0, N_DIVISIONS):
                bpy.ops.object.game_property_new(type='INT',name="geneX" + str(j))
                bpy.ops.object.game_property_new(type='INT',name="geneY" + str(j))
                # set property values
                x = random.randrange(-20, 20)
                y = random.randrange(-20, 20)
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
            bpy.context.active_object.data.materials.append(matObject)
            bpy.context.object.game.physics_type = 'DYNAMIC'
            bpy.context.object.game.use_collision_bounds = True
            bpy.context.object.game.collision_bounds_type = 'CONVEX_HULL'
            bpy.data.objects["BezierCurve." + str(i)].select = False
            # access logic bricks
            sensors =  bpy.context.object.game.sensors
            controllers =  bpy.context.object.game.controllers
            actuators =  bpy.context.object.game.actuators
            # add logic bricks
            for j in range(0, 12):
                bpy.ops.logic.sensor_add(type='RANDOM')
                bpy.ops.logic.controller_add(type='LOGIC_AND')
                bpy.ops.logic.actuator_add(type='MOTION')
            # set logic bricks
            for j in range(0, 12):
                sensors[j].use_pulse_true_level = True
                sensors[j].tick_skip = random.randrange(0, 100)
                sensors[j].seed = random.randrange(0, 100)
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
            for j in range(0, 12):
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
