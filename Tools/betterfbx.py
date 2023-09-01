import bpy
from bpy.types import Operator


class BetterFBXImport(Operator):
    '''Import Model Using BetterFBX'''
    bl_idname = 'hoyo2vrc.betterfbx_import'
    bl_label = 'Hoyo2VRC: BetterFBX Import'

    def execute(self, context):
        """
        Import
        1. Rotation: XYZ Euler
        2. Reset Mesh Origin: False
        3. Edge Options Smooth: Generate By Blender
        """
        bpy.ops.better_import.fbx(
            'INVOKE_DEFAULT', 
            my_rotation_mode='XYZ', 
            use_reset_mesh_origin=False, 
            my_edge_smoothing='Blender',
        )

        return {'FINISHED'}


class BetterFBXExport(Operator):
    '''Export Model Using BetterFBX'''
    bl_idname = 'hoyo2vrc.betterfbx_export'
    bl_label = 'Hoyo2VRC: BetterFBX Export'

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

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        armature = [object for object in bpy.data.objects if object.type == 'ARMATURE'][0]  # expecting 1 armature
        armature.select_set(True)

        bpy.ops.better_export.fbx(
            'INVOKE_DEFAULT', 
            my_scale=1,
            use_optimize_for_game_engine=False,
            use_reset_mesh_origin=False,
            my_edge_smoothing='None',
        )

        return {'FINISHED'}
