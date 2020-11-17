#Library
import bpy
bl_info = {
     "name": "UPBGE_Character_Setup_Addon", 
     "category": "Object", 
     "author": "Shaun Kulesa and Shihab Al-Den", 
     "blender": (2,91,0), 
     }
#Location
class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Character"

class Movement(bpy.types.Operator):
    bl_idname = ".movement"
    bl_label = "Minimal Operator"
    #Function
    def execute(self, context):
        play = bpy.context.object
        play.name = 'Character'
        
        #Keyboard_Sensors
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Forward',object=play.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Backward',object=play.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Left',object=play.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Right',object=play.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Jump',object=play.name)
        
        #Sensor_Keys
        play.game.sensors['Forward'].key = 'W'
        play.game.sensors['Backward'].key = 'S'
        play.game.sensors['Left'].key = 'A'
        play.game.sensors['Right'].key = 'D'
        play.game.sensors['Jump'].key = 'SPACE'

        #Sensor_Collision
        bpy.ops.logic.sensor_add(type="COLLISION",name='Collision',object=play.name)
        
        #Sensor_Property
        play.game.sensors['Collision'].property = ''
        
        #Mouse_Sensor
        bpy.ops.logic.sensor_add(type="MOUSE",name='Look',object=play.name)
        play.game.sensors['Look'].mouse_event = "MOVEMENT"
        
        #And_Controllers
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="F-And", object=play.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="B-And", object=play.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="L-And", object=play.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="R-And", object=play.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="J-And", object=play.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="LO-And", object=play.name)
        
        #Motion_Actuators
        bpy.ops.logic.actuator_add(type="MOTION", name="F-Movement", object=play.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="B-Movement", object=play.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="L-Movement", object=play.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="R-Movement", object=play.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="J-Movement", object=play.name)
        
        #Mouse_Actuator
        bpy.ops.logic.actuator_add(type="MOUSE", name="LO-Look", object=play.name)
        play.game.actuators['LO-Look'].mode = "LOOK"
        play.game.actuators['LO-Look'].use_axis_y = False
        play.game.actuators['LO-Look'].sensitivity_x = 1.6
        
        #Motion_Location
        play.game.actuators['F-Movement'].offset_location = (0, 0.1, 0)
        play.game.actuators['B-Movement'].offset_location = (0, -0.1, 0)
        play.game.actuators['L-Movement'].offset_location = (-0.1, 0, 0)
        play.game.actuators['R-Movement'].offset_location = (0.1, 0, 0)
        
        #Motion_Force
        play.game.actuators['J-Movement'].force = (0, 0, 100)
        
        #Expand_False
        for sensor in play.game.sensors:
            sensor.show_expanded = False
        for controller in play.game.controllers:
            controller.show_expanded = False
        for actuator in play.game.actuators:
            actuator.show_expanded = False
        
        #Sensors_To_Controllers
        play.game.sensors['Forward'].link(play.game.controllers['F-And'])
        play.game.sensors['Backward'].link(play.game.controllers['B-And'])
        play.game.sensors['Left'].link(play.game.controllers['L-And'])
        play.game.sensors['Right'].link(play.game.controllers['R-And'])
        play.game.sensors['Jump'].link(play.game.controllers['J-And'])
        play.game.sensors['Collision'].link(play.game.controllers['J-And'])
        play.game.sensors['Look'].link(play.game.controllers['LO-And'])
        
        #Controllers_To_Actuators
        play.game.actuators["F-Movement"].link(play.game.controllers['F-And'])
        play.game.actuators["B-Movement"].link(play.game.controllers['B-And'])
        play.game.actuators["L-Movement"].link(play.game.controllers['L-And'])
        play.game.actuators["R-Movement"].link(play.game.controllers['R-And'])
        play.game.actuators["J-Movement"].link(play.game.controllers['J-And'])
        play.game.actuators["LO-Look"].link(play.game.controllers['LO-And'])
        return {"FINISHED"}

class FirstPersonCamera(bpy.types.Operator):
    bl_idname = ".first_person_camera"
    bl_label = "Minimal Operator"
    def execute(self, context):
        bpy.ops.object.camera_add()
        cam = bpy.context.object
        cam.rotation_euler = (7.84, 0, 0)
        cam.name = 'Camera_First_Person'
        cam.data.lens = (20)
        bpy.context.scene.camera = cam
        
        #Mouse_Sensor
        bpy.ops.logic.sensor_add(type="MOUSE",name='Look',object=cam.name)
        cam.game.sensors['Look'].mouse_event = "MOVEMENT"

        #Mouse_And
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="LO-And", object=cam.name)

        #Mouse_Actuator
        bpy.ops.logic.actuator_add(type="MOUSE", name="LO-Look", object=cam.name)
        cam.game.actuators['LO-Look'].mode = "LOOK"
        cam.game.actuators['LO-Look'].use_axis_x = False
        cam.game.actuators['LO-Look'].sensitivity_y = 1.6

        #Show_Expanded_False
        cam.game.sensors['Look'].show_expanded = False
        cam.game.controllers['LO-And'].show_expanded = False
        cam.game.actuators['LO-Look'].show_expanded = False

        #Link
        cam.game.sensors['Look'].link(cam.game.controllers['LO-And'])
        cam.game.actuators["LO-Look"].link(cam.game.controllers['LO-And'])
        return {"FINISHED"}
            
class CharacterShell(bpy.types.Operator):
    bl_idname = ".character_shell"
    bl_label = "Minimal Operator"
    def execute(self, context):
        bpy.ops.object.camera_add()
        cam = bpy.context.object
        cam.rotation_euler = (7.84, 0, 0)
        cam.name = 'Camera_First_Person'
        cam.data.lens = (20)
        bpy.context.scene.camera = cam
        cam.location = (0, 1, 0.5)

        #Mouse_Sensor
        bpy.ops.logic.sensor_add(type="MOUSE",name='Look',object=cam.name)
        cam.game.sensors['Look'].mouse_event = "MOVEMENT"

        #Mouse_And
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="LO-And", object=cam.name)

        #Mouse_Actuator
        bpy.ops.logic.actuator_add(type="MOUSE", name="LO-Look", object=cam.name)
        cam.game.actuators['LO-Look'].mode = "LOOK"
        cam.game.actuators['LO-Look'].use_axis_x = False
        cam.game.actuators['LO-Look'].sensitivity_y = 1.6

        #Show_Expanded_False
        cam.game.sensors['Look'].show_expanded = False
        cam.game.controllers['LO-And'].show_expanded = False
        cam.game.actuators['LO-Look'].show_expanded = False

        #Link
        cam.game.sensors['Look'].link(cam.game.controllers['LO-And'])
        cam.game.actuators["LO-Look"].link(cam.game.controllers['LO-And'])

        bpy.ops.mesh.primitive_cube_add()
        player = bpy.context.object
        player.display_type = 'WIRE'
        player.name = 'Player_Shell'

        player.game.physics_type = "RIGID_BODY"
        player.game.use_collision_bounds = True

        #Keyboard_Sensors
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Forward',object=player.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Backward',object=player.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Left',object=player.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Right',object=player.name)
        bpy.ops.logic.sensor_add(type="KEYBOARD",name='Jump',object=player.name)

        #Sensor_Keys
        player.game.sensors['Forward'].key = 'W'
        player.game.sensors['Backward'].key = 'S'
        player.game.sensors['Left'].key = 'A'
        player.game.sensors['Right'].key = 'D'
        player.game.sensors['Jump'].key = 'SPACE'

        #Sensor_Collision
        bpy.ops.logic.sensor_add(type="COLLISION",name='Collision',object=player.name)

        #Sensor_Property
        player.game.sensors['Collision'].property = ''

        #Mouse_Sensor
        bpy.ops.logic.sensor_add(type="MOUSE",name='Look',object=player.name)
        player.game.sensors['Look'].mouse_event = "MOVEMENT"

        #And_Controllers
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="F-And", object=player.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="B-And", object=player.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="L-And", object=player.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="R-And", object=player.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="J-And", object=player.name)
        bpy.ops.logic.controller_add(type="LOGIC_AND", name="LO-And", object=player.name)

        #Motion_Actuators
        bpy.ops.logic.actuator_add(type="MOTION", name="F-Movement", object=player.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="B-Movement", object=player.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="L-Movement", object=player.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="R-Movement", object=player.name)
        bpy.ops.logic.actuator_add(type="MOTION", name="J-Movement", object=player.name)

        #Mouse_Actuator
        bpy.ops.logic.actuator_add(type="MOUSE", name="LO-Look", object=player.name)
        player.game.actuators['LO-Look'].mode = "LOOK"
        player.game.actuators['LO-Look'].use_axis_y = False
        player.game.actuators['LO-Look'].sensitivity_x = 1.6

        #Motion_Location
        player.game.actuators['F-Movement'].offset_location = (0, 0.1, 0)
        player.game.actuators['B-Movement'].offset_location = (0, -0.1, 0)
        player.game.actuators['L-Movement'].offset_location = (-0.1, 0, 0)
        player.game.actuators['R-Movement'].offset_location = (0.1, 0, 0)

        #Motion_Force
        player.game.actuators['J-Movement'].force = (0, 0, 100)

        #Expand_False
        for sensor in player.game.sensors:
            sensor.show_expanded = False
        for controller in player.game.controllers:
            controller.show_expanded = False
        for actuator in player.game.actuators:
            actuator.show_expanded = False

        #Sensors_To_Controllers
        player.game.sensors['Forward'].link(player.game.controllers['F-And'])
        player.game.sensors['Backward'].link(player.game.controllers['B-And'])
        player.game.sensors['Left'].link(player.game.controllers['L-And'])
        player.game.sensors['Right'].link(player.game.controllers['R-And'])
        player.game.sensors['Jump'].link(player.game.controllers['J-And'])
        player.game.sensors['Collision'].link(player.game.controllers['J-And'])
        player.game.sensors['Look'].link(player.game.controllers['LO-And'])

        #Controllers_To_Actuators
        player.game.actuators["F-Movement"].link(player.game.controllers['F-And'])
        player.game.actuators["B-Movement"].link(player.game.controllers['B-And'])
        player.game.actuators["L-Movement"].link(player.game.controllers['L-And'])
        player.game.actuators["R-Movement"].link(player.game.controllers['R-And'])
        player.game.actuators["J-Movement"].link(player.game.controllers['J-And'])
        player.game.actuators["LO-Look"].link(player.game.controllers['LO-And'])

        cam.parent = player
        player.scale = (1, 1, 2)
        return {"FINISHED"}

        
        
class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_1"
    bl_label = "Character Setup"
    #All_of_the_stuff 
    def draw(self, context):
        layout = self.layout
        #First_Person_Label
        layout.label(text="Character Movement:")
        row = layout.row()
        row.scale_y = 1.0
        #Basic_Movement_Button_Logic_Bricks
        row.operator(".movement", text="Movement")
        row = layout.row()
        row.scale_y = 1.0
        #First_Person_Label
        layout.label(text="Camera:")
        row = layout.row()
        row.scale_y = 1.0
        #camera
        row.operator(".first_person_camera", text="First Person Camera")
        row = layout.row()
        row.scale_y = 1.0
        
        #Character Label
        layout.label(text="Character:")
        row = layout.row()
        row.scale_y = 1.0
        #camera
        row.operator(".character_shell", text="Character Collision Shell")
        row = layout.row()
        row.scale_y = 1.0
#Register_Panel
bpy.utils.register_class(PanelOne)

def register():
    bpy.utils.register_class(Movement)
    bpy.utils.register_class(FirstPersonCamera)
    bpy.utils.register_class(CharacterShell)

def unregister():
    bpy.utils.unregister_class(Movement)
    bpy.utils.unregister_class(FirstPersonCamera)
    bpy.utils.unregister_class(CharacterShell)



