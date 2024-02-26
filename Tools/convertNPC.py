import bpy
from bpy.types import Operator
import os
import math
import re
from . import blender_utils, model_utils, armature_utils, shapekey_utils

BlenderVersion = blender_utils.GetBlenderVersion()


class ConvertNonePlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.convertnpc"
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

        def GenShapekey():

            # Check if 'Face' object exists
            if "Face" not in bpy.data.objects:
                print("Face object does not exist. Skipping shape key generation.")
                return

            blender_utils.SelectObject("Face")

            # Check if the required shape keys are present
            required_shape_keys = ["Mouth_A01", "Mouth_Angry02", "Mouth_Open01"]
            fallback_shapekeys = [
                ("Mouth_O01", "Mouth_Open01", 0.5),
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
                "A": [("Mouth_A01", 1.0)],
                "O": [("Mouth_Open01", 1.0), ("Mouth_A01", 0.5)],
                "CH": [("Mouth_Angry02", 1.0)],
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
                        "Face", shapekey_name, new_mix, fallback_shapekeys
                    )
                else:
                    print(
                        f"Skipping generation of {shapekey_name} due to missing shape keys."
                    )

            blender_utils.ChangeMode("OBJECT")

        def FixEyes():
            # Check if the required eye bones exist
            eye_bones = ["+EyeBoneLA02", "+EyeBoneRA02", "Eye_L", "Eye_R"]

            armature.select_set(True)
            blender_utils.ChangeMode("EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            for eye_bone in eye_bones:
                if eye_bone in armature.data.bones:
                    armature_utils.MoveEyes(armature, eye_bone, BlenderVersion)

            # Exit edit mode
            blender_utils.ChangeMode("OBJECT")

        def ConnectArmature():

            bone_pairs = [
                ("Left leg", "Left knee"),
                ("Right leg", "Right knee"),
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
                if armature_utils.BoneExists(
                    armature, bone_name1
                ) and armature_utils.BoneExists(armature, bone_name2):
                    armature_utils.attachbones(
                        armature, bone_name1, bone_name2, exact_match=True
                    )

            blender_utils.ChangeMode("OBJECT")

        def CheckForFace():
            # Check if 'Face' mesh exists
            if "Face" in bpy.data.objects:
                # Check for the existence of 'Face_Eye' and 'Brow'
                if "Face_Eye" in bpy.data.objects and "Brow" in bpy.data.objects:
                    model_utils.MergeFaceByDistance("Face", ["Face_Eye", "Brow"], "A")
                elif "Eyebrow" in bpy.data.objects and "EyeShape" in bpy.data.objects:
                    model_utils.MergeFaceByDistance(
                        "Face", ["Eyebrow", "EyeShape"], "A"
                    )

        def Run():
            model_utils.ScaleModel()
            model_utils.RemoveEmpties()
            model_utils.ClearRotations()
            model_utils.CleanMeshes()
            armature_utils.RenameBones(game, armature)
            SetupArmature()
            GenShapekey()
            FixEyes()
            if bpy.context.scene.reconnect_armature:
                ConnectArmature()
            model_utils.MergeFaceByDistance("Face", ["Face_Eye", "Brow"], "A")
            model_utils.MergeMeshes()

            Run()

            return {"FINISHED"}

            model_utils.MergeMeshes()

        Run()

        return {"FINISHED"}
