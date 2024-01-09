import bpy
from bpy.types import Operator
import bmesh
import math
import os


class ConvertGenshinPlayerCharacter(Operator):
    '''Convert Model'''
    bl_idname = 'hoyo2vrc.convertgpc'
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
                    
        def FixModelBoneView():
            bpy.context.scene.combine_mats = False
            bpy.context.scene.join_meshes = False
            bpy.ops.cats_armature.fix()
            bpy.context.object.display_type = 'WIRE'

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
                
            bpy.context.scene.mesh_name_viseme = 'Face'
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

            if "+EyeBone_L_A02" in armature.edit_bones:
                attacheyes('+EyeBone_L_A02', 'Head')
                move_eyebone(armature.edit_bones["+EyeBone_L_A02"])
                if blender_version >= (3, 6, 2):
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                else: # 3.3.0 - 3.5.0
                    bpy.ops.transform.translate(value=(0, 0.025, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
                bpy.ops.armature.select_all(action='DESELECT')

            if "+EyeBone_R_A02" in armature.edit_bones:
                attacheyes('+EyeBone_R_A02', 'Head')
                move_eyebone(armature.edit_bones["+EyeBone_R_A02"])
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

        def ApplyTransforms():
            for ob in bpy.context.scene.objects:
                if ob.type in ['MESH', 'ARMATURE']:
                    ob.select_set(True)
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    ob.select_set(False)
 
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
            bpy.ops.mesh.remove_doubles()

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
         
        def RotateKnees():
            # Get the armature object
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE':
                    armature = obj
                    break

            # Check if an armature was found
            if armature is None:
                print("No armature found in the scene")
                return

            # Select the armature and set it as the active object
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature

            # Go into pose mode
            bpy.ops.object.mode_set(mode='POSE')

            # Get the left and right knee bones
            left_knee = armature.pose.bones.get('Left knee')  # Replace 'LeftKnee' with the name of your left knee bone
            right_knee = armature.pose.bones.get('Right knee')  # Replace 'RightKnee' with the name of your right knee bone

            # Check if the knee bones were found
            if left_knee is None or right_knee is None:
                print("Could not find the knee bones")
                return

            # Rotate the left knee on the X axis by 3 degrees
            left_knee.rotation_euler.x += math.radians(3)
            
            # Rotate the right knee on the X axis by 3 degrees
            right_knee.rotation_euler.x += math.radians(3)
            
            # Apply the current pose as the rest pose
            bpy.ops.pose.armature_apply()
            
            # Update the scene
            bpy.context.view_layer.update()

            # Go back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')
                
        def Run():
            RemoveEmpties()
            ScaleModel()
            ClearRotations()
            ScaleModel()
            CleanMeshes()
            FixModelBoneView()
            GenShapekey()
            FixEyes()
            FixSpine()
            RotateKnees()
            MergeFaceByDistance()
            RequestMeshMerge()
            ApplyTransforms()
            
        Run()
        
        return {'FINISHED'}
