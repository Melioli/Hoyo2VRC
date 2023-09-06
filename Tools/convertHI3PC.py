import bpy
from bpy.types import Operator
import os


class ConvertHonkaiImpactPlayerCharacter(Operator):
    '''Convert Model'''
    bl_idname = 'hoyo2vrc.converthi3pc'
    bl_label = 'OperatorLabel'

    def execute(self, context):
        #Loli Boy Girl Male Lady
        blender_version = bpy.app.version
        Basetype = bpy.context.active_object.name


        def getKeyBlock(keyName):
            keyBlock=[ x for x in bpy.data.shape_keys if x.key_blocks.get(f'{keyName}')]
            if keyBlock:
                #print(keyBlock)
                return keyBlock[-1].name

        def ScaleModel():
            for ob in bpy.context.scene.objects:
                if ob.type in ['ARMATURE']:
                    ob.select_set(True)
                    bpy.ops.transform.resize(value=(100, 100, 100), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
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
                if obj.type == 'MESH' and obj.name in ['Weapon_L', 'Weapon_R']:
                    bpy.data.objects.remove(obj, do_unlink=True)

        def FixModelBoneView():
            bpy.context.scene.combine_mats = False
            bpy.ops.cats_armature.fix()
            bpy.context.object.display_type = 'WIRE'

        def GenShapekey():
           # Check if the required shape keys are present
            if getKeyBlock("Mouth_A01") is None or getKeyBlock("Mouth_O01") is None or getKeyBlock("Mouth_Angry02") is None:
                print("Required shape keys not found.")
                return

            # Generate A Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Body'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Body']
            bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 1.0
            bpy.data.objects['Body'].shape_key_add(name="A", from_mix=True)
            bpy.data.shape_keys[getKeyBlock("Mouth_A01")].key_blocks["Mouth_A01"].value = 0.0

            # Generate O Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Body'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Body']
            bpy.data.shape_keys[getKeyBlock("Mouth_O01")].key_blocks["Mouth_O01"].value = 1.0
            bpy.data.objects['Body'].shape_key_add(name="O", from_mix=True)
            bpy.data.shape_keys[getKeyBlock("Mouth_O01")].key_blocks["Mouth_O01"].value = 0.0

            # Generate CH Shape Key
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Body'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Body']
            bpy.data.shape_keys[getKeyBlock("Mouth_Angry02")].key_blocks["Mouth_Angry02"].value = 1.0
            bpy.data.objects['Body'].shape_key_add(name="I", from_mix=True)
            bpy.data.shape_keys[getKeyBlock("Mouth_Angry02")].key_blocks["Mouth_Angry02"].value = 0.0

            # Create viseme shape keys
            bpy.ops.cats_viseme.create()

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

            if "Eye_R_End" in armature.edit_bones:
                attacheyes('Eye_R_End', 'Head')
                move_eyebone(armature.edit_bones["Eye_R_End"])
                if blender_version >= (3, 6, 2):
                    bpy.ops.transform.translate(value=(0, 0.035, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=True, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
                else: # 3.3.0 - 3.6.1
                    bpy.ops.transform.translate(value=(0, 0.035, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=True, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

                bpy.ops.armature.select_all(action='DESELECT')
            else:
                print("Eye_R_End not found. Probably using an OldFace Model")

            if "Eye_L_End" in armature.edit_bones:
                attacheyes('Eye_L_End', 'Head')
                move_eyebone(armature.edit_bones["Eye_L_End"])
                if blender_version >= (3, 6, 2):
                    bpy.ops.transform.translate(value=(0, 0.035, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=True, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
                else: # 3.3.0 - 3.6.1
                    bpy.ops.transform.translate(value=(0, 0.035, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=True, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
                    
                bpy.ops.armature.select_all(action='DESELECT')
            else:
                print("Eye_L_End not found. Probably using an OldFace Model")

            # Get the armature object and enter edit mode
            armature_obj = bpy.data.objects['Armature']
            armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = armature_obj
            bpy.ops.object.mode_set(mode='EDIT')

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
        def FixSpine():
            ob = bpy.data.objects['Armature']
            armature = ob.data
            bpy.data.objects['Armature'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='DESELECT')
            def attachfeets(foot, toe):
                armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x
                armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
                armature.edit_bones[foot].tail.z = armature.edit_bones[toe].head.z
            
            attachfeets('Spine', 'Chest')
            bpy.ops.object.mode_set(mode='OBJECT')

        def RenameBones():
            # Define the bone names and new names
            bone_names = ["Eye_L_End", "Eye_R_End"]
            new_names = ["EyeBone_L_A02", "EyeBone_R_A02"]

            # Get the armature object
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE':
                    armature = obj
                    break

            # Rename the bones
            if armature is not None:
                for bone_name in bone_names:
                    if bone_name in armature.pose.bones:
                        bone = armature.pose.bones[bone_name]
                        index = bone_names.index(bone_name)
                        if index < len(new_names):
                            bone.name = new_names[index]
                        else:
                            print("New name not found for bone:", bone_name)
                    else:
                        print("Bone not found:", bone_name, "OldFace")
            else:
                print("Armature not found.")

        def ApplyTransforms():
            for ob in bpy.context.scene.objects:
                if ob.type in ['MESH', 'ARMATURE']:
                    ob.select_set(True)
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    ob.select_set(False)

        def Run():
            ScaleModel()
            RemoveEmpties()
            ClearRotations()
            CleanMeshes()
            FixModelBoneView()
            GenShapekey()
            FixEyes()
            FixSpine()
            RenameBones()
            ApplyTransforms()

        Run()
        
        return {'FINISHED'}
