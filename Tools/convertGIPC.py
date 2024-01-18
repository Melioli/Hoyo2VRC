import bpy
from bpy.types import Operator
import bmesh
import math
import os
import re

class ConvertGenshinPlayerCharacter(Operator):
    '''Convert Model'''
    bl_idname = 'hoyo2vrc.convertgpc'
    bl_label = 'OperatorLabel'

    def execute(self, context):
        #Loli Boy Girl Male Lady
        blender_version = bpy.app.version
        Basetype = bpy.context.active_object.name

        def GetOrientations(armature):
                x_cord = 0
                y_cord = 1
                z_cord = 2
                fbx = False
                return x_cord, y_cord, z_cord, fbx    

        def getKeyBlock(keyName):
            keyBlock=[ x for x in bpy.data.shape_keys if x.key_blocks.get(f'{keyName}')]
            if keyBlock:
                #print(keyBlock)
                return keyBlock[-1].name
            
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
                if ob.type == 'EMPTY':
                    ob.select_set(True)
                    Empties = ob
                    bpy.data.objects.remove(Empties, do_unlink=True)
            
        def ClearRotations():
            for ob in bpy.context.scene.objects:
                if ob.type =='ARMATURE':
                    ob.select_set(True) 
                    ob.rotation_euler = [0, 0, 0]
                    ob.select_set(False)

        def CleanMeshes():
            for obj in bpy.data.objects:
                if obj.type == 'MESH' and obj.name in ['EffectMesh', 'EyeStar']:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    
        def RenameBones():
            # Define the bone names and new names
            bone_names = [
                "Pelvis",
                "LThigh",
                "RThigh",
                "LCalf",
                "RCalf",
                "LFoot",
                "RFoot",
                "LToe0",
                "RToe0",
                "LClavicle",
                "RClavicle",
                "LUpperArm",
                "RUpperArm",
                "LForearm",
                "RForearm",
                "LHand",
                "RHand",
                "LFinger0",
                "LFinger01",
                "LFinger02",
                "LFinger1",
                "LFinger11",
                "LFinger12",
                "LFinger2",
                "LFinger21",
                "LFinger22",
                "LFinger3",
                "LFinger31",
                "LFinger32",
                "LFinger4",
                "LFinger41",
                "LFinger42",
                "RFinger0",
                "RFinger01",
                "RFinger02",
                "RFinger1",
                "RFinger11",
                "RFinger12",
                "RFinger2",
                "RFinger21",
                "RFinger22",
                "RFinger3",
                "RFinger31",
                "RFinger32",
                "RFinger4",
                "RFinger41",
                "RFinger42",
                
            ]
            new_names = [
                "Spine",
                "Left leg",
                "Right leg",
                "Left knee",
                "Right knee",
                "Left foot",
                "Right foot",
                "Left toe",
                "Right toe",
                "Left shoulder",
                "Right shoulder",
                "Left arm",
                "Right arm",
                "Left elbow",
                "Right elbow",
                "Left wrist",
                "Right wrist",
                "Thumb1_L",
                "Thumb2_L",
                "Thumb3_L",
                "IndexFinger1_L",
                "IndexFinger2_L",
                "IndexFinger3_L", 
                "MiddleFinger1_L",
                "MiddleFinger2_L",
                "MiddleFinger3_L",
                "RingFinger1_L",
                "RingFinger2_L",
                "RingFinger3_L",
                "LittleFinger1_L",
                "LittleFinger2_L",
                "LittleFinger3_L",
                "Thumb1_R",
                "Thumb2_R",
                "Thumb3_R",
                "IndexFinger1_R",
                "IndexFinger2_R",
                "IndexFinger3_R", 
                "MiddleFinger1_R",
                "MiddleFinger2_R",
                "MiddleFinger3_R",
                "RingFinger1_R",
                "RingFinger2_R",
                "RingFinger3_R",
                "LittleFinger1_R",
                "LittleFinger2_R",
                "LittleFinger3_R",
                
            ]
            starts_with = [
                ('_', ''),
                ('ValveBiped_', ''),
                ('Valvebiped_', ''),
                ('Bip1_', 'Bip_'),
                ('Bip01_', 'Bip_'),
                ('_', 'Bip_'),
                ('Bip01', ''),
                ('Bip001', ''),
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
            bone_names = ["Bip001 Pelvis", "+EyeBone L A01", "+EyeBone R A01"]

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
                armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x
                armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
                armature.edit_bones[foot].tail.z = armature.edit_bones[toe].head.z
            
            attachfeets("+PelvisTwistCFA01", "Hips")    
                  
            if bpy.context.scene.connect_chest_to_neck:
                attachfeets("Chest", "Neck")
            else:
                attachfeets("Upper Chest", "Neck")
                
            attachfeets("Right arm", "Right elbow")
            attachfeets("Left arm", "Left elbow")
            attachfeets("Neck", "Head")
            attachfeets("+UpperArmTwistRA01", "+UpperArmTwistRA02")
            attachfeets("+UpperArmTwistLA01", "+UpperArmTwistLA02")
            bpy.ops.object.mode_set(mode="OBJECT")
            
        def GenShapekey():
            #Generate A Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Face'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Face']
            if getKeyBlock("Mouth_A01") is not None:
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 1.0
                bpy.data.objects['Face'].shape_key_add(name="A", from_mix=True)
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.0


            #Generate O Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Face'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Face']
            if getKeyBlock("Mouth_Fury01") is not None and getKeyBlock("Mouth_A01") is not None:
                bpy.data.shape_keys[getKeyBlock("Mouth_Fury01")].key_blocks["Mouth_Fury01"].value = 0.25
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.5
                bpy.data.objects['Face'].shape_key_add(name="O", from_mix=True)
                bpy.data.shape_keys[getKeyBlock("Mouth_Fury01")].key_blocks["Mouth_Fury01"].value = 0.0
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.0
            elif getKeyBlock("Mouth_Open01") is not None and getKeyBlock("Mouth_A01") is not None:
                bpy.data.shape_keys[getKeyBlock("Mouth_Open01")].key_blocks["Mouth_Open01"].value = 0.5
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.5
                bpy.data.objects['Face'].shape_key_add(name="O", from_mix=True)
                bpy.data.shape_keys[getKeyBlock("Mouth_Open01")].key_blocks["Mouth_Open01"].value = 0.0
                bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.0


            #Generate CH Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Face'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Face']
            if getKeyBlock("Mouth_Angry02") is not None:
                bpy.data.shape_keys[getKeyBlock("Mouth_Angry02")].key_blocks["Mouth_Angry02"].value = 1.0
                bpy.data.objects['Face'].shape_key_add(name="I", from_mix=True)
                bpy.data.shape_keys[getKeyBlock("Mouth_Angry02")].key_blocks["Mouth_Angry02"].value = 0.0
                
            # Generate additional shape keys
            shapekey_data = {
                'vrc.v_aa': [('A', 0.9998)],
                'vrc.v_ch': [('CH', 0.9996)],
                'vrc.v_dd': [('A', 0.3), ('CH', 0.7)],
                'vrc.v_e': [('CH', 0.7), ('O', 0.3)],
                'vrc.v_ff': [('A', 0.2), ('CH', 0.4)],
                'vrc.v_ih': [('A', 0.5), ('CH', 0.2)],
                'vrc.v_kk': [('A', 0.7), ('CH', 0.4)],
                'vrc.v_nn': [('A', 0.2), ('CH', 0.7)],
                'vrc.v_oh': [('A', 0.2), ('O', 0.8)],
                'vrc.v_ou': [('O', 0.9994)],
                'vrc.v_pp': [('A', 0.0004), ('O', 0.0004)],
                'vrc.v_rr': [('CH', 0.5), ('O', 0.3)],
                'vrc.v_sil': [('A', 0.0002), ('CH', 0.0002)],
                'vrc.v_ss': [('CH', 0.8)],
                'vrc.v_th': [('A', 0.4), ('O', 0.15)],
            }

            for shapekey_name, mix in shapekey_data.items():
                # Reset all shape keys
                for key in bpy.data.objects['Face'].data.shape_keys.key_blocks:
                    key.value = 0

                # Set the value of the shape keys in the mix
                for key_name, value in mix:
                    if getKeyBlock(key_name) is not None:
                        bpy.data.shape_keys[getKeyBlock(key_name)].key_blocks[key_name].value = value

                # Add a new shape key from the mix
                bpy.data.objects['Face'].shape_key_add(name=shapekey_name, from_mix=True)
                for key_name, _ in mix:
                    if getKeyBlock(key_name) is not None:
                        bpy.data.shape_keys[getKeyBlock(key_name)].key_blocks[key_name].value = 0

            bpy.ops.object.select_all(action='DESELECT')

        def FixEyes():
            ob = bpy.data.objects['Armature']
            armature = ob.data
            bpy.data.objects['Armature'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='DESELECT')

            def attacheyes(foot, toe):
                if foot in armature.edit_bones and toe in armature.edit_bones:
                    foot_head = armature.edit_bones[foot].head
                    toe_head = armature.edit_bones[toe].head
                    foot_tail = armature.edit_bones[foot].tail

                    foot_tail.x = foot_head.x
                    foot_tail.y = foot_head.y
                    foot_tail.z = toe_head.z + 0.12

            def move_eyebone(bone):
                bone.select = True
                bone.select_head = True
                bone.select_tail = True

            if "+EyeBoneLA02" in armature.edit_bones:
                attacheyes('+EyeBoneLA02', 'Head')
                move_eyebone(armature.edit_bones["+EyeBoneLA02"])
                if blender_version >= (3, 6, 2):
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                else: # 3.3.0 - 3.5.0
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                bpy.ops.armature.select_all(action='DESELECT')

            if "+EyeBoneRA02" in armature.edit_bones:
                attacheyes('+EyeBoneRA02', 'Head')
                move_eyebone(armature.edit_bones["+EyeBoneRA02"])
                if blender_version >= (3, 6, 2):
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                else: # 3.3.0 - 3.5.0
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                bpy.ops.armature.select_all(action='DESELECT')

            # Get the armature object and enter edit mode
            armature_obj = bpy.data.objects['Armature']
            armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = armature_obj

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
 
        def MergeFaceByDistance():
            # Get the "Face" mesh
            face_obj = bpy.data.objects.get("Face")
            if face_obj is None:
                print("Face mesh not found")
                return

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select the meshes to merge
            meshes_to_merge = ["Face_Eye", "Brow"]
            for obj_name in meshes_to_merge:
                obj = bpy.data.objects.get(obj_name)
                if obj is not None:
                    obj.select_set(True)
                else:
                    print(f"Object {obj_name} not found")

            # Also select "Face" because it's the mesh we want to join into
            face_obj.select_set(True)

            # Set the active object to "Face"
            bpy.context.view_layer.objects.active = face_obj

            # Join the selected objects into the active object
            bpy.ops.object.join()

            # Ensure we're in object mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Select the "Face" mesh
            bpy.ops.object.select_all(action='DESELECT')
            face_obj.select_set(True)

            # Set the active object to "Face"
            bpy.context.view_layer.objects.active = face_obj

            # Switch to edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Select all vertices
            bpy.ops.mesh.select_all(action='SELECT')

            # Merge vertices by distance
            bpy.ops.mesh.remove_doubles(threshold=0.00001)  # Reduce the merge distance
            
            bpy.ops.mesh.select_all(action='DESELECT')

            # Switch back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')

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
            ClearRotations()
            ScaleModel()
            CleanMeshes()
            CleanBones()
            RenameBones()
            SetupArmature()
            FixVRCLite()
            GenShapekey()
            FixEyes()
            MergeFaceByDistance()
            RequestMeshMerge()
       
        Run()
        
        return {'FINISHED'}
