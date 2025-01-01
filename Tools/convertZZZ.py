import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import bmesh
import math
import os
import re
from . import blender_utils, model_utils, armature_utils, shapekey_utils

BlenderVersion = blender_utils.GetBlenderVersion()


class ConvertZenlessZoneZeroPlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.convertzzz"
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

                armature_utils.FixSpine(spine, hips, x_cord, y_cord, z_cord)
                armature_utils.FixChest(chest, spine, x_cord, y_cord, z_cord)
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

            # Attach feet to the corresponding bones
            bone_pairs = [
                # ("PelvisTwistCFA01", "Hips"),
                ("Left shoulder", "Left arm"),
                ("Right shoulder", "Right arm"),
                ("Left elbow", "Left wrist"),
                ("Right elbow", "Right wrist"),
                ("Neck", "Head"),
                ("Right leg", "Right knee"),
                ("Left leg", "Left knee"),  
                ("Right knee", "Right ankle"),
                ("Left knee", "Left ankle"),
            ]

            if bpy.context.scene.connect_twist_to_limbs:
                bone_pairs.append(("UpperArmTwistRA02", "Right elbow"))
                bone_pairs.append(("UpperArmTwistLA02", "Left elbow"))
            else:
                bone_pairs.append(("Right arm", "Right elbow"))
                bone_pairs.append(("Left arm", "Left elbow"))

            if bpy.context.scene.connect_chest_to_neck:
                bone_pairs.append(("Chest", "Neck"))
            else:
                bone_pairs.append(("Upper Chest", "Neck"))

            twist_bone_pairs = [
                ("UpperArmTwistRA01", "UpperArmTwistRA02"),
                ("UpperArmTwistLA01", "UpperArmTwistLA02"),
            ]

            blender_utils.ChangeMode("EDIT")
            armature_utils.ToggleArmatureSelection(armature, select=False)

            for bone1, bone2 in bone_pairs:
                armature_utils.attachfeets(armature, bone1, bone2)

            for bone1, bone2 in twist_bone_pairs:
                if armature_utils.ContainsName(bone1) and armature_utils.ContainsName(
                    bone2
                ):
                    armature_utils.attachfeets(armature, bone1, bone2)

            blender_utils.ChangeMode("OBJECT")

        def GenShapekey():
            # Find the face mesh by looking for object ending with _Face
            face_objects = [obj for obj in bpy.data.objects if obj.name.endswith('_Face')]
            if not face_objects:
                print("No object ending with _Face found. Skipping shape key generation.")
                return
            face_obj = face_objects[0]

            # Check if the required shape keys are present
            required_shape_keys = [
                "Fac_Mth_AaTalk", "Fac_Mth_Oo", "Fac_Mth_Uu","Fac_Mth_Ee", "Fac_Mth_Ii",
            ]
            fallback_shapekeys = [
                ("Fac_Mth_Aa1", "Fac_Mth_Ee", 0.5),
            ]

            fallback_dict = {key: value for key, value, _ in fallback_shapekeys}

            for key in required_shape_keys:
                if shapekey_utils.getKeyBlock(key, face_obj) is None:
                    if key in fallback_dict and shapekey_utils.getKeyBlock(fallback_dict[key], face_obj) is not None:
                        print(f"Replaced missing shape key {key} with fallback {fallback_dict[key]}")
                    else:
                        print(f"Required shape key {key} is not present and no fallback available.")

            # Generate additional shape keys
            shapekey_data = {
                "A": [(face_obj.name, "Fac_Mth_AaTalk", 1)],
                "O": [(face_obj.name, "Fac_Mth_Oo", 1),],
                "CH": [(face_obj.name, "Fac_Mth_Ee", 0.3), (face_obj.name, "Fac_Mth_Ii", 1), (face_obj.name, "Fac_Mth_Uu", 0.05)],
                "vrc.v_aa": [(face_obj.name, "A", 0.9998)],
                "vrc.v_ch": [(face_obj.name, "CH", 0.9996)],
                "vrc.v_dd": [(face_obj.name, "A", 0.3), (face_obj.name, "CH", 0.7)],
                "vrc.v_e": [(face_obj.name, "CH", 0.7), (face_obj.name, "O", 0.3)],
                "vrc.v_ff": [(face_obj.name, "A", 0.2), (face_obj.name, "CH", 0.4)],
                "vrc.v_ih": [(face_obj.name, "A", 0.5), (face_obj.name, "CH", 0.2)],
                "vrc.v_kk": [(face_obj.name, "A", 0.7), (face_obj.name, "CH", 0.4)],
                "vrc.v_nn": [(face_obj.name, "A", 0.2), (face_obj.name, "CH", 0.7)],
                "vrc.v_oh": [(face_obj.name, "A", 0.2), (face_obj.name, "O", 0.8)],
                "vrc.v_ou": [(face_obj.name, "O", 0.9994)],
                "vrc.v_pp": [(face_obj.name, "A", 0.0004), (face_obj.name, "O", 0.0004)],
                "vrc.v_rr": [(face_obj.name, "CH", 0.5), (face_obj.name, "O", 0.3)],
                "vrc.v_sil": [(face_obj.name, "A", 0.0002), (face_obj.name, "CH", 0.0002)],
                "vrc.v_ss": [(face_obj.name, "CH", 0.8)],
                "vrc.v_th": [(face_obj.name, "A", 0.4), (face_obj.name, "O", 0.15)],
                "Blink": [(face_obj.name, "Fac_Eye_Close", 1)],
                "Happy Blink": [(face_obj.name, "Fac_Eye_L_Wink", 1), (face_obj.name, "Fac_Eye_R_Wink", 1)],
            }

            for shapekey_name, mix in shapekey_data.items():
                try:
                    shapekey_utils.GenerateShapeKey(face_obj.name, shapekey_name, mix, fallback_shapekeys)
                    print(f"Successfully generated shape key: {shapekey_name}")
                except Exception as e:
                    print(f"Error generating shape key {shapekey_name}: {str(e)}")

            blender_utils.ChangeMode("OBJECT")

        def FixEyes():
            armature.select_set(True)
            blender_utils.ChangeMode("EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            # Get model size from the name
            size_match = re.search(r'Size(\d{2})', armature.name)
            offset = 0.025  # Default offset
            
            if size_match:
                size_num = int(size_match.group(1))
                print(size_num)
                # Adjust offset based on size number
                if size_num == 2:
                    offset = 0  # Less offset for Size02
                elif size_num == 3:
                    offset = 0.025  # Original offset for Size03
                else:
                    offset = 0.02   # Default offset for other sizes

            for eye_bone_name in ["Skn_L_Eye", "Skn_R_Eye", "Eye_L", "Eye_R"]:
                armature_utils.MoveEyes(armature, eye_bone_name, BlenderVersion, eye_offset=offset)

            bpy.ops.armature.select_all(action="DESELECT")
            blender_utils.ChangeMode("OBJECT")

        def Run():
            model_utils.RemoveEmpties()
            model_utils.ScaleModel()
            model_utils.ClearRotations()
            model_utils.ScaleModel()
            model_utils.CleanMeshes()
            armature_utils.CleanBones()
            armature_utils.RenameBones(game, armature)
            SetupArmature()
            if bpy.context.scene.reconnect_armature:
                ConnectArmature()
            if bpy.context.scene.generate_shape_keys:
                GenShapekey()
            FixEyes()
            model_utils.ReorderUVMaps()
            model_utils.MergeMeshes()

        Run()

        return {"FINISHED"}
