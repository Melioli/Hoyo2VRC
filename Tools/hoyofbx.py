import bpy
from bpy.types import Operator


class Hoyo2VRCImport(Operator):
    """Import Model Using Hoyo2VRC"""

    bl_idname = "hoyo2vrc.import"
    bl_label = "Hoyo2VRC: Hoyo2VRC Import"

    def execute(self, context):
        """
        Import
        1. Rotation: XYZ Euler
        2. Reset Mesh Origin: False
        3. Edge Options Smooth: Generate By Blender
        """
        bpy.ops.hoyo2vrc_import.fbx(
            "INVOKE_DEFAULT",
            my_rotation_mode="XYZ",
            use_reset_mesh_origin=False,
            my_edge_smoothing="Blender",
        )

        return {"FINISHED"}


class Hoyo2VRCExport(Operator):
    """Export Model Using Hoyo2VRC"""

    bl_idname = "hoyo2vrc.export"
    bl_label = "Hoyo2VRC: Hoyo2VRC Export"

    def execute(self, context):
        """
        Export
        1. Select Armature
        2. Scale: 1
        3. Optimize for Game Engine: False
        4. Reset Mesh Origin: False
        5. Edge Options Smooth: None
        6. Apply All Transforms: True
        """

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        armature = [object for object in bpy.data.objects if object.type == "ARMATURE"][
            0
        ]  # expecting 1 armature
        armature.select_set(True)

        # Select all objects
        bpy.ops.object.select_all(action="SELECT")

        # Apply the scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        bpy.ops.hoyo2vrc_export.fbx(
            "INVOKE_DEFAULT",
            my_scale=1.0,
            use_optimize_for_game_engine=True,
            my_fbx_version="FBX202000",
            use_reset_mesh_origin=False,
            my_edge_smoothing="None",
            use_ignore_armature_node=False,
        )

        return {"FINISHED"}
