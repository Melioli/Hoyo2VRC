import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import bmesh
import math
import os
import re
from . import blender_utils, model_utils, armature_utils, shapekey_utils

BlenderVersion = blender_utils.GetBlenderVersion()


class ConvertGenshinWeapon(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.convertgiw"
    bl_label = "Convert GI Weapon"

    def execute(self, context):

        # Find valid model in scene
        Model = None
        for obj in bpy.context.scene.objects:
            if model_utils.IsValidModel(obj):
                Model = obj
                break

        # Identify the model
        game, body_type, model_name = model_utils.IdentifyModel(Model.name)
        print(game, body_type, model_name)
        print(BlenderVersion)

        def Run():
            model_utils.RemoveEmpties()
            model_utils.ClearRotations()
            model_utils.CleanMeshes()
            model_utils.MergeMeshes()
            model_utils.FinalName("Weapon")

        Run()

        return {"FINISHED"}