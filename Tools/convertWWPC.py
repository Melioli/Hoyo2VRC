import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import bmesh
import math
import mathutils
from mathutils import Vector
import os
import re
from . import blender_utils, model_utils, armature_utils, shapekey_utils

BlenderVersion = blender_utils.GetBlenderVersion()


class ConvertWutheringWavesPlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.convertwuwa"
    bl_label = "OperatorLabel"

    def execute(self, context):

        # Iterate over all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a valid model
            if model_utils.IsValidModel(obj):
                Model = obj
                break

        # Identify the model
        game, body_type, model_name = model_utils.IdentifyModel(Model.name)
        print(game, body_type, model_name)
        print(BlenderVersion)

        global armature
        armature = armature_utils.GetArmature()

        def SetupArmature():

            # Rename the armature
            armature.name = "Armature"

            x_cord, y_cord, z_cord, fbx = model_utils.GetOrientations(armature)

            bpy.context.object.display_type = "WIRE"
            bpy.context.object.show_in_front = True

            # Switch to edit mode
            blender_utils.ChangeMode("EDIT")

            if context.scene.humanoid_armature_fix:
                # Check if the first bone in the hierarchy is 'Hips'
                if armature.data.edit_bones[0].name != "Hips":
                    # Rename the first bone to 'Hips'
                    armature.data.edit_bones[0].name = "Hips"

                armature_utils.SetHipAsParent(armature)

                armature_utils.RenameSpines(armature, ["Spine", "Chest", "Upper Chest"])

                bone_names = [
                    "Hips",
                    "Spine",
                    "Chest",
                    "Upper Chest",
                    "Head",
                    "Left leg",
                    "Right leg",
                    "Left knee",
                    "Right knee",
                ]
                (
                    hips,
                    spine,
                    chest,
                    upperchest,
                    head,
                    left_leg,
                    right_leg,
                    left_knee,
                    right_knee,
                ) = armature_utils.GetBones(armature, bone_names).values()

                # Fixing the hips
                armature_utils.FixHips(
                    hips, right_leg, left_leg, spine, x_cord, y_cord, z_cord
                )

                armature_utils.FixWWSpine(spine, hips, x_cord, y_cord, z_cord)
                armature_utils.FixWWChest(chest, spine, x_cord, y_cord, z_cord)
                armature_utils.FixUpperChest(upperchest, chest, x_cord, y_cord, z_cord)
                armature_utils.AdjustLegs(
                    left_leg, right_leg, left_knee, right_knee, y_cord
                )
                armature_utils.StraightenHead(armature, head, x_cord, y_cord, z_cord)
                armature_utils.FixMissingNeck(
                    armature, chest, head, x_cord, y_cord, z_cord
                )
                armature_utils.SetBoneRollToZero(armature)

            blender_utils.ChangeMode("OBJECT")

        def ConnectArmature():

            bone_pairs = [
                ("Left leg", "Left knee"),
                ("Left knee", "Left ankle"),
                ("Right leg", "Right knee"),
                ("Right knee", "Right ankle"),
                ("Right arm", "Right elbow"),
                ("Left arm", "Left elbow"),
                ("Left elbow", "Left wrist"),
                ("Right elbow", "Right wrist"),
                ("Right shoulder", "Right arm"),
                ("Left shoulder", "Left arm"),
                ("Neck", "Head"),
            ]

            if bpy.context.scene.connect_chest_to_neck:
                bone_pairs.append(("Chest", "Neck"))
            else:
                bone_pairs.append(("Upper Chest", "Neck"))

            blender_utils.ChangeMode("EDIT")
            armature_utils.ToggleArmatureSelection(armature, select=False)

            for bone_name1, bone_name2 in bone_pairs:
                armature_utils.attachbones(
                    armature, bone_name1, bone_name2, exact_match=True
                )

            blender_utils.ChangeMode("OBJECT")

        def GenShapekey():

            # Check if 'Face' object exists
            if "Body" not in bpy.data.objects:
                print("Body object does not exist. Skipping shape key generation.")
                return

            blender_utils.SelectObject("Body")

            # Check if the required shape keys are present
            required_shape_keys = ["A", "O", "I"]
            fallback_shapekeys = [
                ("A", "Aa", 0.75),
            ]

            fallback_dict = {key: value for key, value, _ in fallback_shapekeys}

            for i, key in enumerate(required_shape_keys):
                if shapekey_utils.getKeyBlock(key) is None:
                    # Check if there is a fallback shape key
                    if (
                        key in fallback_dict
                        and shapekey_utils.getKeyBlock(fallback_dict[key]) is not None
                    ):
                        required_shape_keys[i] = fallback_dict[key]
                        print(
                            f"Replaced missing shape key {key} with fallback {fallback_dict[key]}"
                        )
                    else:
                        print(
                            f"Required shape key {key} is not present and no fallback available. Skipping shape key generation."
                        )
                        return

            # Generate additional shape keys
            shapekey_data = {
                "A": [("A", 1)],
                "O": [("O", 1)],
                "CH": [("E", 0.3), ("I", 1), ("U", 0.05)],
                "vrc.v_aa": [("A", 0.9998)],
                "vrc.v_ch": [("CH", 0.9996)],
                "vrc.v_dd": [("A", 0.3), ("CH", 0.7)],
                "vrc.v_e": [("CH", 0.7), ("O", 0.3)],
                "vrc.v_ff": [("A", 0.2), ("CH", 0.4)],
                "vrc.v_ih": [("A", 0.5), ("CH", 0.2)],
                "vrc.v_kk": [("A", 0.7), ("CH", 0.4)],
                "vrc.v_nn": [("A", 0.2), ("CH", 0.7)],
                "vrc.v_oh": [("A", 0.2), ("O", 0.8)],
                "vrc.v_ou": [("O", 0.9994)],
                "vrc.v_pp": [("A", 0.0004), ("O", 0.0004)],
                "vrc.v_rr": [("CH", 0.5), ("O", 0.3)],
                "vrc.v_sil": [("A", 0.0002), ("CH", 0.0002)],
                "vrc.v_ss": [("CH", 0.8)],
                "vrc.v_th": [("A", 0.4), ("O", 0.15)],
            }

            for shapekey_name, mix in shapekey_data.items():
                new_mix = []
                for key, value in mix:
                    if shapekey_utils.getKeyBlock(key) is None:
                        # Look for a fallback shape key
                        if (
                            key in fallback_dict
                            and shapekey_utils.getKeyBlock(fallback_dict[key])
                            is not None
                        ):
                            new_key = fallback_dict[key]
                            new_mix.append((new_key, value))
                            print(
                                f"Replaced missing shape key {key} with fallback {new_key}"
                            )
                        else:
                            print(
                                f"Skipping shape key {key} due to no fallback available."
                            )
                    else:
                        new_mix.append((key, value))

                if new_mix:
                    shapekey_utils.GenerateShapeKey(
                        "Body", shapekey_name, new_mix, fallback_shapekeys
                    )
                else:
                    print(
                        f"Skipping generation of {shapekey_name} due to missing shape keys."
                    )

            blender_utils.ChangeMode("OBJECT")
        
        def SeparateWuWaEyes(shape_key_name):
            # Get the active object, which should be the armature
            armature_obj = bpy.context.view_layer.objects.active
            if armature_obj is None or armature_obj.type != 'ARMATURE':
                raise ValueError("Active object is not an armature")

            # Find the mesh object parented to the armature
            mesh_obj = None
            for obj in armature_obj.children:
                if obj.type == 'MESH' and "Body" in obj.name:
                    mesh_obj = obj
                    break

            if mesh_obj is None:
                raise ValueError("No body mesh object found parented to the armature")

            # Ensure the mesh object is selected and active
            bpy.context.view_layer.objects.active = mesh_obj
            mesh_obj.select_set(True)

            # Store the original shape key values
            original_shape_key_values = {sk.name: sk.value for sk in mesh_obj.data.shape_keys.key_blocks}

            # Set the specified shape key to 1.0
            mesh_obj.data.shape_keys.key_blocks[shape_key_name].value = 1.0

            # Enter edit mode for the mesh
            bpy.ops.object.mode_set(mode='EDIT')

            # Deselect all vertices
            bpy.ops.mesh.select_all(action='DESELECT')

            # Select vertices for the left eye based on the active shape key
            model_utils.SelectVertByShapeKey(bpy.context, 'L', shape_key_name)
            bpy.ops.mesh.separate(type='SELECTED')

            # Select vertices for the right eye based on the active shape key
            model_utils.SelectVertByShapeKey(bpy.context, 'R', shape_key_name)
            bpy.ops.mesh.separate(type='SELECTED')

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Get the newly created objects
            new_objects = [obj for obj in bpy.context.selected_objects if obj != mesh_obj]

            # Rename the new objects to "Left Eye" and "Right Eye"
            for obj in new_objects:
                if obj.type == 'MESH':  # Ensure the object is a mesh
                    bpy.context.view_layer.objects.active = obj
                    bm = bmesh.new()
                    bm.from_mesh(obj.data)
                    if any((obj.matrix_world @ v.co).x < 0 for v in bm.verts):
                        obj.name = "Left Eye"
                    else:
                        obj.name = "Right Eye"
                    bm.free()

                    # Reset the shape keys to their original values for the new objects
                    if obj.data.shape_keys:
                        for sk_name, sk_value in original_shape_key_values.items():
                            if sk_name in obj.data.shape_keys.key_blocks:
                                obj.data.shape_keys.key_blocks[sk_name].value = sk_value

            # Reset the shape keys to their original values for the original mesh object
            for sk_name, sk_value in original_shape_key_values.items():
                mesh_obj.data.shape_keys.key_blocks[sk_name].value = sk_value
                
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
                
            # Reset shape keys for the eyes
            for obj in new_objects:
                if obj.type == 'MESH' and obj.name in ["Left Eye", "Right Eye"]:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.shape_key_remove(all=True, apply_mix=False)
                    
            # Remove unused body shape keys
            UnusedShapekeys = ["Pupil_Up", "Pupil_Down", "Pupil_R", "Pupil_L", "Pupil_Scale"]
            shapekey_utils.RemoveShapeKeys(UnusedShapekeys, "Body")
            
            # Remove Unused Materials
            for obj in new_objects:
                if obj.type == 'MESH' and obj.name in ["Left Eye", "Right Eye"]:
                    model_utils.RemoveMaterials(obj, keep_suffixes=["Eye", "Eyes"])

            
            bpy.ops.object.mode_set(mode='OBJECT')

        def CreateEyes(eye_name, bone_name):
            # Run CursorToObject to set the cursor location
            blender_utils.CursorToObject(eye_name)

            # Ensure the cursor location is updated
            bpy.context.view_layer.update()

            # Select the armature
            armature = bpy.data.objects.get("Armature")  # Replace with the actual name of your armature
            if armature is None:
                raise ValueError("Armature not found")
            
            bpy.context.view_layer.objects.active = armature
            armature.select_set(True)

            # Enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Add a new bone at the cursor position
            bpy.ops.armature.bone_primitive_add(name=bone_name)
            
            # Get the newly created bone
            armature_data = armature.data
            edit_bones = armature_data.edit_bones
            bone = edit_bones[bone_name]
            
            # Set the tail of the bone to point upwards (along the Z-axis)
            bone.tail = bone.head + mathutils.Vector((0, 0, 4))
            
            # Set the parent of the newly created bone to the "Head" bone
            head_bone = edit_bones.get("Head")
            if head_bone is None:
                raise ValueError("Head bone not found")
            bone.parent = head_bone

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Select the eye object
            eye_obj = bpy.data.objects.get(eye_name)
            if eye_obj is None:
                raise ValueError(f"Object '{eye_name}' not found")
            
            bpy.context.view_layer.objects.active = eye_obj
            eye_obj.select_set(True)

            # Enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Create a vertex group for the bone
            if bone_name not in eye_obj.vertex_groups:
                vertex_group = eye_obj.vertex_groups.new(name=bone_name)
            else:
                vertex_group = eye_obj.vertex_groups[bone_name]

            # Assign all vertices to the vertex group
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.vertex_group_assign()

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Ensure the vertex group is linked to the bone for weight painting
            modifier = eye_obj.modifiers.new(name="Armature", type='ARMATURE')
            modifier.object = armature
            
            # Deselct the objects
            eye_obj.select_set(False)
            armature.select_set(False)
            
        def Run():
            armature_utils.RenameBones(game, armature)
            armature_utils.CleanBones()
            SetupArmature()
            if bpy.context.scene.reconnect_armature:
                ConnectArmature()
            model_utils.RenameMeshToBody()
            GenShapekey()
            SeparateWuWaEyes("Pupil_Scale")
            CreateEyes("Left Eye", "Eye_L")
            CreateEyes("Right Eye", "Eye_R")
            blender_utils.ResetCursor()


        Run()

        return {"FINISHED"}