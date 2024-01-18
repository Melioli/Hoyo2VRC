import bpy
import sys
import re
from pathlib import Path
from bpy.types import Panel


from Hoyo2VRC.Tools.importer import Hoyo2VRCImportFbx
from Hoyo2VRC.Tools.exporter import Hoyo2VRCExportFbx
from Hoyo2VRC.Tools.hoyofbx import Hoyo2VRCImport, Hoyo2VRCExport
from Hoyo2VRC.Tools.convertGIPC import ConvertGenshinPlayerCharacter
from Hoyo2VRC.Tools.convertHSRPC import ConvertHonkaiStarRailPlayerCharacter
from Hoyo2VRC.Tools.convertHI3PC import ConvertHonkaiImpactPlayerCharacter
from Hoyo2VRC.Tools.convertNPC import ConvertNonePlayerCharacter



bl_info = {
    "name": "Hoyo2VRC",
    "author": "Meliodas, Mken",
    "version": (2, 0, 0),
    "blender": (3, 6, 2),
    "location": "3D View > Sidebar > Hoyo2VRC",
    "description": "Convert Hoyoverse models to VRC",
    "warning": "Requires Hoyoverse Datamined Assets",
    "doc_url": "",
    "support": 'COMMUNITY',
    "category": "VRC",
    "tracker_url": "",
    "doc_url": "https://docs.hoyotoon.com"
}

class Hoyo2VRCModelPanel(Panel):
    bl_idname = "hoyo2vrc_PT_model_panel"
    bl_label = "Model"
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hoyo2VRC"

    def draw(self, context):
        layout = self.layout
        
         # Get the version number from bl_info
        version = bl_info["version"]
        version_str = '.'.join(map(str, version))

        # Create a box for the version number
        box = layout.box()
        box.label(text="Hoyo2VRC Version:" + version_str, icon='INFO')  # You can replace 'INFO' with any other icon you prefer

        # Add a box section for the model
        box = layout.box()
        box.label(text="Model Conversions", icon='MESH_DATA')
        

        # Add a row for importing the model
        row = box.row()
        row.operator(
            operator='hoyo2vrc.import',
            text='Import Model',
            icon='IMPORT'
        )
        if bpy.context.selected_objects:
            #Add a row for exporting the model
            row.operator(
                operator='hoyo2vrc.export',
                text='Export Model',
                icon='EXPORT'
            )
            # Add a row for converting the avatar
            row = box.row()       
            name = bpy.context.object.name.replace(".001", "").replace("_Render", "").replace("_merge", "").replace(" (merge)", "").replace("_Edit", " ")
            if re.match(r"^(Cs_Avatar|Avatar|NPC_Avatar)_(Boy|Girl|Lady|Male|Loli)_(Sword|Claymore|Bow|Catalyst|Pole)_[a-zA-Z]+(?<!_\d{2})$", name):
                # Genshin Impact Playable character
                row.operator(
                    operator='hoyo2vrc.convertgpc',
                    text='Convert GI Avatar',
                    icon='PLAY'
                )
            elif re.match(r"^(Player|Avatar|Art|NPC_Avatar)_(Boy|Girl|Lady|Male|Kid|Lad|Maid|Miss|[a-zA-Z]+)?_?[a-zA-Z]*_(?<!_\d{2})\d{2}$", name):
                # Honkai Star Rail Playable Character
                row.operator(
                    operator='hoyo2vrc.converthsrpc',
                    text='Convert HSR Avatar',
                    icon='PLAY'
                )
            elif re.match(r"^Avatar_\w+?_C\d+(_\w+)$", name):
                # Honkai Impact Playable Character
                row.operator(
                    operator='hoyo2vrc.converthi3pc',
                    text='Convert HI3 Avatar',
                    icon='PLAY'
                )
            else :
                row.operator(
                    operator='hoyo2vrc.convertnpc',
                    text='Convert NPC',
                    icon='PLAY'
                )

class Hoyo2VRCToggleMenu(bpy.types.Menu):
    bl_idname = "HOYO2VRC_MT_toggle_menu"
    bl_label = "Toggle Menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "merge_all_meshes", text="Merge All Meshes")
        
        layout.prop(context.scene, "connect_chest_to_neck", text="Chest Connects to Neck")

class Hoyo2VRCToggleMenuButton(bpy.types.Operator):
    bl_idname = "hoyo2vrc.toggle_menu_button"
    bl_label = "Toggle Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu(name=Hoyo2VRCToggleMenu.bl_idname)
        return {'FINISHED'}

class Hoyo2VRCSettingsPanel(Panel):
    bl_label = "Settings"
    bl_idname = "hoyo2vrc_PT_Settings_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hoyo2VRC"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        # Add a box section for the settings
        box = layout.box()
        box.label(text="Toggles", icon='TOOL_SETTINGS')
        
        # Add a row for the "Merge All Meshes" option
        row = box.row()
        row.prop(context.scene, "merge_all_meshes")
        
        # Add a row for the "Chest Connects to Neck" option
        row = box.row()
        row.prop(context.scene, "connect_chest_to_neck")

        # Add a separator for better visual organization
        box.separator()
        

classes = [
    ConvertGenshinPlayerCharacter,
    ConvertHonkaiImpactPlayerCharacter,
    ConvertHonkaiStarRailPlayerCharacter,
    ConvertNonePlayerCharacter,
    Hoyo2VRCImportFbx,
    Hoyo2VRCExportFbx,
    Hoyo2VRCImport,
    Hoyo2VRCExport,
    Hoyo2VRCModelPanel,
    Hoyo2VRCToggleMenu,
    Hoyo2VRCToggleMenuButton,
    Hoyo2VRCSettingsPanel,
]

def register():
    bpy.types.Scene.merge_all_meshes = bpy.props.BoolProperty(
        name="Merge All Meshes",
        description="Decide whether all meshes should be merged or not",
        default = True
    )
    
    bpy.types.Scene.connect_chest_to_neck = bpy.props.BoolProperty(
        name="Connect Chest to Neck",
        description="Decide the Chest bone should connect to the Neck bone instead of the Upper Chest bone",
        default = False
    )

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)