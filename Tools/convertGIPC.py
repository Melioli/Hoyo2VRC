import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import bmesh
import math
import os
import re
from . import blender_utils, model_utils, armature_utils, shapekey_utils

BlenderVersion = blender_utils.GetBlenderVersion()


class ConvertGenshinPlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.convertgpc"
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
            # Check if 'Face' and 'Face_Eye' objects exist
            if "Face" not in bpy.data.objects or "Face_Eye" not in bpy.data.objects:
                print("Face or Face_Eye object does not exist. Skipping shape key generation.")
                return

            # Check if the required shape keys are present
            required_shape_keys = {
                "Face": ["Mouth_A01", "Mouth_Fury01", "Mouth_Open01"],
                "Face_Eye": ["Eye_WinkA_L", "Eye_WinkA_R", "Eye_WinkB_L", "Eye_WinkB_R", "Eye_WinkC_L", "Eye_WinkC_R"]
            }
            fallback_shapekeys = [
                ("Mouth_Fury01", "Mouth_Open01", 0.5),
            ]

            fallback_dict = {key: value for key, value, _ in fallback_shapekeys}

            for obj_name, keys in required_shape_keys.items():
                obj = bpy.data.objects.get(obj_name)
                if obj is None:
                    print(f"Object {obj_name} not found. Skipping its shape keys.")
                    continue

                for key in keys:
                    if shapekey_utils.getKeyBlock(key, obj) is None:
                        if key in fallback_dict and shapekey_utils.getKeyBlock(fallback_dict[key], obj) is not None:
                            print(f"Replaced missing shape key {key} with fallback {fallback_dict[key]} in {obj_name}")
                        else:
                            print(f"Required shape key {key} is not present in {obj_name} and no fallback available.")

            # Generate additional shape keys
            shapekey_data = {
                "A": [("Face", "Mouth_A01", 1)],
                "O": [
                    ("Face", "Mouth_Smile02", 0.5),
                    ("Face", "Mouth_A01", 0.5),
                    ("Face", "Mouth_Smile02", 0.5),
                ],
                "CH": [("Face", "Mouth_Open01", 1.0), ("Face", "Mouth_A01", 0.115)],
                "vrc.v_aa": [("Face", "A", 0.9998)],
                "vrc.v_ch": [("Face", "CH", 0.9996)],
                "vrc.v_dd": [("Face", "A", 0.3), ("Face", "CH", 0.7)],
                "vrc.v_e": [("Face", "CH", 0.7), ("Face", "O", 0.3)],
                "vrc.v_ff": [("Face", "A", 0.2), ("Face", "CH", 0.4)],
                "vrc.v_ih": [("Face", "A", 0.5), ("Face", "CH", 0.2)],
                "vrc.v_kk": [("Face", "A", 0.7), ("Face", "CH", 0.4)],
                "vrc.v_nn": [("Face", "A", 0.2), ("Face", "CH", 0.7)],
                "vrc.v_oh": [("Face", "A", 0.2), ("Face", "O", 0.8)],
                "vrc.v_ou": [("Face", "O", 0.9994)],
                "vrc.v_pp": [("Face", "A", 0.0004), ("Face", "O", 0.0004)],
                "vrc.v_rr": [("Face", "CH", 0.5), ("Face", "O", 0.3)],
                "vrc.v_sil": [("Face", "A", 0.0002), ("Face", "CH", 0.0002)],
                "vrc.v_ss": [("Face", "CH", 0.8)],
                "vrc.v_th": [("Face", "A", 0.4), ("Face", "O", 0.15)],
                "Blink": [("Face_Eye", "Eye_WinkB_L", 1), ("Face_Eye", "Eye_WinkB_R", 1)],
                "Happy Blink": [("Face_Eye", "Eye_WinkA_L", 1), ("Face_Eye", "Eye_WinkA_R", 1)],
                "Pensive Blink": [("Face_Eye", "Eye_WinkC_L", 1), ("Face_Eye", "Eye_WinkC_R", 1)],
            }

            for shapekey_name, mix in shapekey_data.items():
                # Determine the target object based on the first item in the mix
                target_object_name = mix[0][0]
                try:
                    shapekey_utils.GenerateShapeKey(target_object_name, shapekey_name, mix, fallback_shapekeys)
                    print(f"Successfully generated shape key: {shapekey_name}")
                except Exception as e:
                    print(f"Error generating shape key {shapekey_name}: {str(e)}")

            blender_utils.ChangeMode("OBJECT")

        def FixEyes():
            armature.select_set(True)
            blender_utils.ChangeMode("EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            for eye_bone_name in ["+EyeBoneLA02", "+EyeBoneRA02"]:
                armature_utils.MoveEyes(armature, eye_bone_name, BlenderVersion)

            bpy.ops.armature.select_all(action="DESELECT")

            # Exit edit mode
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
            if bpy.context.scene.generate_shape_keys:
                model_utils.MergeFaceByDistance("Face", ["Face_Eye", "Brow"], "A")
            else:
                model_utils.MergeFaceByDistance("Face", ["Face_Eye", "Brow"], "Mouth_A01")
            model_utils.MergeMeshes()

        Run()

        return {"FINISHED"}