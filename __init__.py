import bpy
import sys
import re
from pathlib import Path
from bpy.types import Panel

from .Tools import (
    model_utils,
    importer,
    exporter,
    hoyofbx,
    convertGIPC,
    convertHSRPC,
    convertHI3PC,
    convertNPC,
)
from . import settings


bl_info = {
    "name": "Hoyo2VRC",
    "author": "Meliodas",
    "version": (3, 0, 3),
    "blender": (4, 0, 2),
    "location": "3D View > Sidebar > Hoyo2VRC",
    "description": "Convert Hoyoverse models to VRChat usable models.",
    "warning": "Requires Hoyoverse Datamined Assets",
    "doc_url": "https://docs.hoyotoon.com",
    "support": "COMMUNITY",
    "category": "VRC",
    "tracker_url": "",
}


class Hoyo2VRCModelPanel(Panel):
    bl_idname = "hoyo2vrc_PT_model_panel"
    bl_label = "Model Conversion"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hoyo2VRC"

    def draw(self, context):
        layout = self.layout

        # Get the version number from bl_info
        version = bl_info["version"]
        version_str = ".".join(map(str, version))

        # Create a box for the version number
        box = layout.box()
        box.label(text="Hoyo2VRC Version:" + version_str, icon="INFO")

        # Add a box section for the model
        box = layout.box()
        box.label(text="Model Conversions", icon="MESH_DATA")

        # Add a row for importing and exporting the model
        row = box.row()
        row.operator(operator="hoyo2vrc.import", text="Import Model", icon="IMPORT")

        # Initialize Model to None
        Model = None

        # Iterate over all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a valid model
            if model_utils.IsValidModel(obj):
                Model = obj
                break

        if Model:

            # Add a row for exporting the model
            row.operator(operator="hoyo2vrc.export", text="Export Model", icon="EXPORT")

            # Add a row for converting the avatar
            row = box.row()

            # Identify the model
            game, body_type, model_name = model_utils.IdentifyModel(Model.name)

            # Define a dictionary to map game names to operator functions and display texts
            games = {
                "Genshin Impact": ("hoyo2vrc.convertgpc", "Convert GI Avatar"),
                "Honkai Star Rail": ("hoyo2vrc.converthsrpc", "Convert HSR Avatar"),
                "Honkai Impact": ("hoyo2vrc.converthi3pc", "Convert HI3 Avatar"),
                # "NPC": ("hoyo2vrc.convertnpc", "Convert NPC"),
            }

            # Get the operator function and display text for the current game
            operator_func, display_text = games.get(game, (None, None))

            # If the operator function exists, call it with the appropriate parameters
            if operator_func:
                operator = row.operator(
                    operator=operator_func, text=display_text, icon="PLAY"
                )
            elif game == "NPC":
                row.label(text="NPC is currently not supported", icon="ERROR")


class Hoyo2VRCConversionSettingsPanel(Panel):
    bl_label = "Conversion Settings"
    bl_idname = "hoyo2vrc_PT_Settings_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hoyo2VRC"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        # Add a box section for the Mesh settings
        box = layout.box()

        # Add a row for the "Merge Meshes" option
        row = box.row()
        row.prop(
            context.scene,
            "merge_all_meshes",
            text="Merge Meshes",
            icon="CHECKBOX_HLT" if context.scene.merge_all_meshes else "CHECKBOX_DEHLT",
        )
        row = box.row()
        row.prop(
            context.scene,
            "connect_chest_to_neck",
            text="Connect Chest to Neck",
            icon=(
                "CHECKBOX_HLT"
                if context.scene.connect_chest_to_neck
                else "CHECKBOX_DEHLT"
            ),
        )
        row = box.row()
        row.prop(
            context.scene,
            "connect_twist_to_limbs",
            text="Connect Twists to Limbs",
            icon=(
                "CHECKBOX_HLT"
                if context.scene.connect_twist_to_limbs
                else "CHECKBOX_DEHLT"
            ),
        )
        row = box.row()
        row.prop(
            context.scene,
            "reconnect_armature",
            text="Reconnect Armature",
            icon=(
                "CHECKBOX_HLT" if context.scene.reconnect_armature else "CHECKBOX_DEHLT"
            ),
        )
        row = box.row()
        row.prop(
            context.scene,
            "humanoid_armature_fix",
            text="Humanoid Armature Fixing",
            icon=(
                "CHECKBOX_HLT"
                if context.scene.humanoid_armature_fix
                else "CHECKBOX_DEHLT"
            ),
        )

        # Add a separator for better visual organization
        box.separator()


classes = [
    convertGIPC.ConvertGenshinPlayerCharacter,
    convertHI3PC.ConvertHonkaiImpactPlayerCharacter,
    convertHSRPC.ConvertHonkaiStarRailPlayerCharacter,
    convertNPC.ConvertNonePlayerCharacter,
    importer.Hoyo2VRCImportFbx,
    exporter.Hoyo2VRCExportFbx,
    hoyofbx.Hoyo2VRCImport,
    hoyofbx.Hoyo2VRCExport,
    Hoyo2VRCModelPanel,
    Hoyo2VRCConversionSettingsPanel,
]


def register():
    settings.register_settings()

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    settings.unregister_settings()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
