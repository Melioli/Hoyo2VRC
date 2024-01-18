import bpy
from bpy.types import Operator
import os
import math
import re


class ConvertHonkaiStarRailPlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.converthsrpc"
    bl_label = "OperatorLabel"

    def execute(self, context):
        blender_version = bpy.app.version

        def GetOrientations(armature):
                x_cord = 0
                y_cord = 1
                z_cord = 2
                fbx = False
                return x_cord, y_cord, z_cord, fbx    

        def ScaleModel():
            for ob in bpy.context.scene.objects:
                if ob.type == 'ARMATURE':
                    ob.select_set(True)
                    
                    # Get the dimensions of the armature
                    dimensions = ob.dimensions

                    # Check the Z dimension and scale accordingly
                    if dimensions.z > 100:
                        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
                    elif dimensions.z > 10:
                        bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
                    elif 1 < dimensions.z < 3:
                        pass  # Do nothing
                    elif dimensions.z < 1:
                        bpy.ops.transform.resize(value=(100, 100, 100))

                    ob.select_set(False)

        def RemoveEmpties():
            for ob in bpy.context.scene.objects:
                if ob.type == "EMPTY":
                    ob.select_set(True)
                    Empties = ob
                    bpy.data.objects.remove(Empties, do_unlink=True)

        def GenerateShapeKeys():
            def get_shapekey(object_name, shape_name):
                bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
                if bpy.context.object.data.shape_keys == None:
                    return None
                for shape_key in bpy.context.object.data.shape_keys.key_blocks:
                    if shape_key.name == shape_name:
                        return shape_key

            def reset_pose(root_object):
                bpy.context.view_layer.objects.active = root_object
                bpy.ops.object.posemode_toggle()
                bpy.ops.pose.select_all(action="SELECT")
                bpy.ops.pose.transforms_clear()
                bpy.ops.object.posemode_toggle()

            root = bpy.context.active_object
            face_obj = bpy.data.objects["Face"]
            
            if root.type != 'ARMATURE':
                # If it's not, look for an armature among its children
                for child in root.children:
                    if child.type == 'ARMATURE':
                        root = child
                        break
                else:
                    # If no armature is found, print a message and return
                    print("No armature found in the selected object or its children.")
                    return

            if "Avatar" not in root.name and "Player" not in root.name:
                # The condition is incomplete, so I'm assuming you want to return if the condition is met
                return

            # Check if there are any actions
            if not bpy.data.actions:
                print("No Animations Found.")
                return  # Stop the execution of GenerateShapeKeys function

            # convert animation to shapekey
            for action in bpy.data.actions:
                if ".00" in action.name or "Emo_" not in action.name:
                    continue

                print(action.name)
                arr = action.name.split("_")
                shapekey_name = "_".join(arr[2:])

                # apply animation
                if root is not None and action is not None:
                    root.animation_data.action = action
                    bpy.ops.object.visual_transform_apply()

                # convert shapekay
                bpy.context.view_layer.objects.active = face_obj
                bpy.ops.object.modifier_apply_as_shapekey(
                    keep_modifier=True, modifier=face_obj.modifiers[0].name
                )
                shapekey = get_shapekey(face_obj.name, face_obj.modifiers[0].name)
                shapekey.name = shapekey_name

                # reset transform
                reset_pose(root)

        def ClearAnimations():
            obj = bpy.context.object
            if obj is not None:
                # Remove all animation data
                obj.animation_data_clear()

                # Remove all animations
                for action in bpy.data.actions:
                    if action.users == 0:
                        bpy.data.actions.remove(action)

        def ClearRotations():
            for ob in bpy.context.scene.objects:
                if ob.type == "ARMATURE":
                    ob.select_set(True)
                    ob.rotation_euler = [0, 0, 0]
                    ob.select_set(False)

        def CleanMeshes():
            for obj in bpy.data.objects:
                if obj.type == "MESH" and obj.name in ["EffectMesh", "EyeStar"]:
                    bpy.data.objects.remove(obj, do_unlink=True)

        def FaceMask():
            maskObj = bpy.context.scene.objects["Face_Mask"]
            maskObj.vertex_groups.new(name="Head")
            for vertex in maskObj.data.vertices:
                vertList = []
                vertList.append(vertex.index)
                try:
                    headGroup = maskObj.vertex_groups["Head"]
                    headGroup.add(vertList, 1.0, "REPLACE")
                except:
                    continue

        def RenameBones():
            # Define the bone names and new names
            bone_names = [
                "Root_M",
                "Hip_L",
                "Hip_R",
                "HipPart1_R",
                "HipPart1_L",
                "Spine1_M",
                "Spine2_M",
                "Chest_M",
                "Shoulder_L",
                "Shoulder_R",
                "Scapula_R",
                "Scapula_L",
                "Neck_M",
                "Head_M",
                "face",
                "Knee_L",
                "Knee_R",
                "Ankle_L",
                "Ankle_R",
                "Toes_L",
                "Toes_R",
                "Elbow_L",
                "Elbow_R",
                "Wrist_L",
                "Wrist_R",
            ]
            new_names = [
                "Hips",
                "Left leg",
                "Right leg",
                "Right leg twist R",
                "Left leg twist L",
                "Spine",
                "Chest",
                "Upper Chest",
                "Left arm",
                "Right arm",
                "Right shoulder",
                "Left shoulder",
                "Neck",
                "Head",
                "Face",
                "Left knee",
                "Right knee",
                "Left ankle",
                "Right ankle",
                "Left toe",
                "Right toe",
                "Left elbow",
                "Right elbow",
                "Left wrist",
                "Right wrist",
            ]
            starts_with = [
                ('_', ''),
                ('ValveBiped_', ''),
                ('Valvebiped_', ''),
                ('Bip1_', 'Bip_'),
                ('Bip01_', 'Bip_'),
                ('Bip001_', 'Bip_'),
                ('Bip01', ''),
                ('Bip02_', 'Bip_'),
                ('Character1_', ''),
                ('HLP_', ''),
                ('JD_', ''),
                ('JU_', ''),
                ('Armature|', ''),
                ('Bone_', ''),
                ('C_', ''),
                ('Cf_S_', ''),
                ('Cf_J_', ''),
                ('G_', ''),
                ('Joint_', ''),
                ('Def_C_', ''),
                ('Def_', ''),
                ('DEF_', ''),
                ('Chr_', ''),
                ('Chr_', ''),
                ('B_', ''),
            ]
            ends_with = [
                ('_Bone', ''),
                ('_Bn', ''),
                ('_Le', '_L'),
                ('_Ri', '_R'),
                ('_', ''),
            ]
            replaces = [
                (' ', '_'),
                ('-', '_'),
                ('.', '_'),
                (':', '_'),
                ('____', '_'),
                ('___', '_'),
                ('__', '_'),
                ('_Le_', '_L_'),
                ('_l', '_L'),
                ('_Ri_', '_R_'),
                ('_r', '_R'),
                ('_m', '_M'),
                ('LEFT', 'Left'),
                ('RIGHT', 'Right'),
                ('all', 'All'),
                ('finger', 'Finger'),
                ('part', 'Part'),
                
            ]
            
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == "ARMATURE":
                    armature = obj
                    break
                
            if armature is not None:
                for bone in armature.pose.bones:
                    bone.name = re.sub(r"(?<=\w)([A-Z])", r" \1", bone.name).title().replace(' ', '')

                    for old, new in starts_with:
                        if bone.name.startswith(old):
                            bone.name = bone.name.replace(old, new, 1)
                    for old, new in ends_with:
                        if bone.name.endswith(old):
                            bone.name = bone.name[:len(bone.name)-len(old)] + new
                    for old, new in replaces:
                        bone.name = bone.name.replace(old, new)

                    if bone.name in bone_names:
                        bone.name = new_names[bone_names.index(bone.name)]
                        
        def CleanBones():
            # Define the bone names to remove
            bone_names = ["Skin_GRP", "Main"]

            # Get the armature object
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == "ARMATURE":
                    armature = obj
                    break

            # Set the active object in the context
            bpy.context.view_layer.objects.active = armature

            # Switch to edit mode
            bpy.ops.object.mode_set(mode="EDIT")

            # Remove the bones
            if armature is not None:
                # Create a list of bones to remove
                bones_to_remove = [bone for bone in armature.data.edit_bones if bone.name in bone_names]

                # Remove the bones
                for bone in bones_to_remove:
                    armature.data.edit_bones.remove(bone)

            # Switch back to pose mode
            bpy.ops.object.mode_set(mode="OBJECT")

        def SetupArmature():
                           
            # Iterate over all objects in the scene
            for obj in bpy.data.objects:
                # Check if the object is an armature
                if obj.type == 'ARMATURE':
                    # Rename the armature
                    obj.name = "Armature"
                    armature = obj  # Save the armature object for later use
                    
                    
            x_cord, y_cord, z_cord, fbx = GetOrientations(armature)
            
            bpy.context.object.display_type = "WIRE"
            bpy.context.object.show_in_front = True
                
            # Switch to edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Check if the first bone in the hierarchy is 'Hips'
            if armature.data.edit_bones[0].name != 'Hips':
                # Rename the first bone to 'Hips'
                armature.data.edit_bones[0].name = 'Hips'

            # Make Hips top parent and reparent other top bones to hips
            if 'Hips' in armature.data.edit_bones:
                hips = armature.data.edit_bones.get('Hips')
                hips.parent = None
                for bone in armature.data.edit_bones:
                    if bone.parent is None:
                        bone.parent = hips
                        
            # Find all spines
            spines = [bone for bone in armature.data.edit_bones if 'spine' in bone.name.lower()]

            # Rename spines based on the number of spines
            if len(spines) == 1:
                spines[0].name = 'Spine'
            elif len(spines) == 2:
                spines[0].name = 'Spine'
                spines[1].name = 'Chest'
            elif len(spines) == 3:
                spines[0].name = 'Spine'
                spines[1].name = 'Chest'
                spines[2].name = 'Upper Chest'
            
            # Hips bone should be fixed as per specification from the SDK code
            if 'Hips' in armature.data.edit_bones:
                if 'Spine' in armature.data.edit_bones:
                    if 'Chest' in armature.data.edit_bones:
                        if 'Left leg' in armature.data.edit_bones:
                            if 'Right leg' in armature.data.edit_bones:
                                hips = armature.data.edit_bones.get('Hips')
                                spine = armature.data.edit_bones.get('Spine')
                                chest = armature.data.edit_bones.get('Chest')
                                upperchest = armature.data.edit_bones.get('Upper Chest')
                                left_leg = armature.data.edit_bones.get('Left leg')
                                right_leg = armature.data.edit_bones.get('Right leg')
                                left_knee = armature.data.edit_bones.get('Left knee')
                                right_knee = armature.data.edit_bones.get('Right knee')
                                

                                # Fixing the hips

                                # Put Hips in the center of the leg bones
                                hips.head[x_cord] = (right_leg.head[x_cord] + left_leg.head[x_cord]) / 2

                                # Adjust the y-coordinate of the hip bone
                                hips.head[y_cord] = (right_leg.head[y_cord] + left_leg.head[y_cord]) / 2

                                # Put Hips at 33% between spine and legs
                                hips.head[z_cord] = left_leg.head[z_cord] + (spine.head[z_cord] - left_leg.head[z_cord]) * 0.33

                                # If Hips are below or at the leg bones, put them above
                                if hips.head[z_cord] <= right_leg.head[z_cord]:
                                    hips.head[z_cord] = right_leg.head[z_cord] + 0.1

                                # Make Hips point straight up
                                hips.tail[x_cord] = hips.head[x_cord]
                                hips.tail[y_cord] = hips.head[y_cord]
                                hips.tail[z_cord] = spine.head[z_cord]

                                if hips.tail[z_cord] < hips.head[z_cord]:
                                    hips.tail[z_cord] = hips.tail[z_cord] + 0.1
                                
                                # Fixing Spine    
                                spine.head[x_cord] = hips.tail[x_cord]
                                spine.head[y_cord] = hips.tail[y_cord]
                                spine.head[z_cord] = hips.tail[z_cord]

                                # Make Spine point straight up
                                spine.tail[x_cord] = spine.head[x_cord]
                                spine.tail[y_cord] = spine.head[y_cord]  # Align tail with head on y-axis
                                spine.tail[z_cord] = spine.head[z_cord] + 0.065  # Adjust this value as needed

                                # Fixing Chest
                                chest.head[x_cord] = spine.tail[x_cord]
                                chest.head[y_cord] = spine.tail[y_cord]
                                chest.head[z_cord] = spine.tail[z_cord]

                                # Make Chest point straight up
                                chest.tail[x_cord] = chest.head[x_cord]
                                chest.tail[y_cord] = chest.head[y_cord]  # Align tail with head on y-axis
                                chest.tail[z_cord] = chest.head[z_cord] + 0.065  # Adjust this value as needed

                                # Fixing UpperChest
                                upperchest.head[x_cord] = chest.tail[x_cord]
                                upperchest.head[y_cord] = chest.tail[y_cord]
                                upperchest.head[z_cord] = chest.tail[z_cord]

                                # Make UpperChest point straight up
                                upperchest.tail[x_cord] = upperchest.head[x_cord]
                                upperchest.tail[y_cord] = upperchest.head[y_cord]  # Align tail with head on y-axis
                                upperchest.tail[z_cord] = upperchest.head[z_cord] + 0.1  # Adjust this value as needed
                                
                                
                                # Make legs bend very slightly forward
                                print (f"Before: {left_leg.tail[y_cord]}")
                                left_leg.tail[y_cord] += -0.015  # Move tail of leg forward
                                left_knee.head[y_cord] += -0.015  # Move head of knee forward
                                print (f"After: {left_knee.head[y_cord]}")
                                
                                print(f"Before: {right_knee.head[y_cord]}")
                                right_leg.tail[y_cord] += -0.015  # Move tail of leg forward
                                right_knee.head[y_cord] += -0.015  # Move head of knee forward
                                print(f"After: {right_knee.head[y_cord]}")
                                    
            # Straighten up the head bone
            if 'Head' in armature.data.edit_bones:
                head = armature.data.edit_bones.get('Head')
                head.tail[x_cord] = head.head[x_cord]
                head.tail[y_cord] = head.head[y_cord]
                if head.tail[z_cord] < head.head[z_cord]:
                    head.tail[z_cord] = head.head[z_cord] + 0.1
                    
            # Fix missing neck
            if 'Neck' not in armature.data.edit_bones:
                if 'Chest' in armature.data.edit_bones:
                    if 'Head' in armature.data.edit_bones:
                        neck = armature.data.edit_bones.new('Neck')
                        chest = armature.data.edit_bones.get('Chest')
                        head = armature.data.edit_bones.get('Head')
                        neck.head = chest.tail
                        neck.tail = head.head

                        if neck.head[z_cord] == neck.tail[z_cord]:
                            neck.tail[z_cord] += 0.1
                            
            
            # Iterate over all bones in the armature
            for bone in armature.data.edit_bones:
                # Set the roll of the bone to 0
                bone.roll = 0
            
            # Switch back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')        

        def FixVRCLite():
            ob = bpy.data.objects["Armature"]
            armature = ob.data
            bpy.data.objects["Armature"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            def attachfeets(foot, toe):
                foot_bone = next(bone for bone in bpy.context.object.data.bones if foot in bone.name)
                toe_bone = next(bone for bone in bpy.context.object.data.bones if toe in bone.name)
                armature.edit_bones[foot_bone.name].tail.x = armature.edit_bones[toe_bone.name].head.x
                armature.edit_bones[foot_bone.name].tail.y = armature.edit_bones[toe_bone.name].head.y
                armature.edit_bones[foot_bone.name].tail.z = armature.edit_bones[toe_bone.name].head.z
                            
            def ContainsName(name):
                return any(name in bone.name for bone in bpy.context.object.data.bones)
                  
            if bpy.context.scene.connect_chest_to_neck:
                attachfeets("Chest", "Neck")
            else:
                attachfeets("Upper Chest", "Neck")
            
            attachfeets("Left leg", "Left knee")
            attachfeets("Right leg", "Right knee")
            attachfeets("Right arm", "Right elbow")
            attachfeets("Left arm", "Left elbow")
            attachfeets("Left elbow", "Left wrist")
            attachfeets("Right elbow", "Right wrist")
            attachfeets("Neck", "Head")
            bpy.ops.object.mode_set(mode="OBJECT")

        def FixEyes():
            ob = bpy.data.objects["Armature"]
            armature = ob.data
            bpy.data.objects["Armature"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            def attacheyes(foot, toe):
                armature.edit_bones[foot].tail.z = (
                    armature.edit_bones[toe].head.z - armature.edit_bones[foot].tail.y
                )
                armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
                armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x

            attacheyes("Eye_L", "Eye_All_L")
            attacheyes("Eye_R", "Eye_All_R")

            # Get the armature object and enter edit mode
            armature_obj = bpy.data.objects["Armature"]
            armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = armature_obj
            bpy.ops.object.mode_set(mode="EDIT")

            # Get the Eye_L and Eye_R bones
            eye_l_bone = armature_obj.data.edit_bones.get("Eye_L")
            eye_r_bone = armature_obj.data.edit_bones.get("Eye_R")
            face_bone = armature_obj.data.edit_bones.get("Face")

            # Get the Head bone
            head_bone = armature_obj.data.edit_bones.get("Head")

            # Reparent the Eye_L and Eye_R bones to the Head bone
            if eye_l_bone and eye_r_bone and face_bone and head_bone:
                eye_l_bone.parent = head_bone
                eye_r_bone.parent = head_bone
                face_bone.parent = head_bone

            # Exit edit mode
            bpy.ops.object.mode_set(mode="OBJECT")

        def RequestMeshMerge():
            if bpy.context.scene.merge_all_meshes:
                # User checked "Merge All Meshes", so merge all meshes

                # Deselect all objects
                bpy.ops.object.select_all(action='DESELECT')

                # Select all mesh objects
                mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
                for obj in mesh_objects:
                    obj.select_set(True)

                # Set the active object to "Body" if it exists, otherwise use the first mesh object
                body_object = bpy.data.objects.get("Body")
                if body_object is not None:
                    bpy.context.view_layer.objects.active = body_object
                elif mesh_objects:
                    bpy.context.view_layer.objects.active = mesh_objects[0]

                # Join the selected objects into the active object
                bpy.ops.object.join()

                # Rename the active object to "Body"
                bpy.context.active_object.name = "Body"
            else:
                # User unchecked "Merge All Meshes", so do nothing
                pass
        
        def Run():
            RemoveEmpties()
            ScaleModel()
            GenerateShapeKeys()
            ClearAnimations()
            ClearRotations()
            ScaleModel()
            CleanMeshes()
            FaceMask()
            RenameBones()
            CleanBones()
            SetupArmature()
            FixVRCLite()
            FixEyes()
            RequestMeshMerge()

        Run()

        return {"FINISHED"}
