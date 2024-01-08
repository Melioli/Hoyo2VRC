import bpy
import sys
import re
from pathlib import Path
from bpy.types import Panel

from Hoyo2VRC.Tools.betterfbx import BetterFBXImport, BetterFBXExport
from Hoyo2VRC.Tools.installaddon import InstallDependencies
from Hoyo2VRC.Tools.convertGIPC import ConvertGenshinPlayerCharacter
from Hoyo2VRC.Tools.convertHSRPC import ConvertHonkaiStarRailPlayerCharacter
from Hoyo2VRC.Tools.convertHI3PC import ConvertHonkaiImpactPlayerCharacter
from Hoyo2VRC.Tools.convertNPC import ConvertNonePlayerCharacter


bl_info = {
    "name": "Hoyo2VRC",
    "author": "Meliodas, Mken",
    "version": (1, 0, 9),
    "blender": (3, 6, 2),
    "location": "3D View > Sidebar > Hoyo2VRC",
    "description": "Convert Hoyoverse rips to VRC",
    "warning": "Requires CATS and BetterFBX. Please run the Install Dependencies Button",
    "doc_url": "",
    "support": 'COMMUNITY',
    "category": "VRC",
    "tracker_url": "",
    "doc_url": ""
}

class Hoyo2VRCModelPanel(Panel):
    bl_idname = "hoyo2vrc_PT_model_panel"
    bl_label = "Model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hoyo2VRC"

    def draw(self, context):
        layout = self.layout

        # Add a box section for the model
        box = layout.box()

        # Add a row for importing the model
        row = box.row()
        row.operator(
            operator='hoyo2vrc.betterfbx_import',
            text='Import Model',
            icon='IMPORT'
        )
        if bpy.context.selected_objects:
            #Add a row for exporting the model
            row.operator(
                operator='hoyo2vrc.betterfbx_export',
                text='Export Model',
                icon='EXPORT'
            )
            # Add a row for converting the avatar
            row = box.row()
            split = row.split(factor=0.8)  # Adjust the factor to change the width of the main button
            
            name = bpy.context.object.name.replace(".001", "").replace("_Render", "").replace("_merge", "").replace(" (merge)", "")
            if re.match(r"^(Cs_Avatar|Avatar|NPC_Avatar)_(Boy|Girl|Lady|Male|Loli)_(Sword|Claymore|Bow|Catalyst|Pole)_[a-zA-Z]+(?<!_\d{2})$", name):
                # Genshin Impact Playable character
                split.operator(
                    operator='hoyo2vrc.convertgpc',
                    text='Convert GI Avatar',
                    icon='PLAY'
                )
            elif re.match(r"^(Avatar|Art|NPC_Avatar)_(Boy|Girl|Lady|Male|Kid|Lad|Maid|Miss|[a-zA-Z]+)?_?[a-zA-Z]*_(?<!_\d{2})\d{2}$", name):
                # Honkai Star Rail Playable Character
                split.operator(
                    operator='hoyo2vrc.converthsrpc',
                    text='Convert HSR Avatar',
                    icon='PLAY'
                )
            elif re.match(r"^Avatar_\w+?_C\d+(_\w+)$", name):
                # Honkai Impact Playable Character
                split.operator(
                    operator='hoyo2vrc.converthi3pc',
                    text='Convert HI3 Avatar',
                    icon='PLAY'
                )
            else :
                split.operator(
                    operator='hoyo2vrc.convertnpc',
                    text='Convert NPC',
                    icon='PLAY'
                )
                
            # Add the toggle menu button to the right of the convert button
            split.operator(Hoyo2VRCToggleMenuButton.bl_idname, text="", icon='SETTINGS')

class Hoyo2VRCToggleMenu(bpy.types.Menu):
    bl_idname = "HOYO2VRC_MT_toggle_menu"
    bl_label = "Toggle Menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "merge_all_meshes", text="Merge All Meshes")

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

        # Add a row for installing dependencies
        row = box.row()
        row.operator(
            operator='hoyo2vrc.install_addons',
            text='Install Dependencies',
            icon='ERROR'
        )
        

classes = [
    ConvertGenshinPlayerCharacter,
    ConvertHonkaiImpactPlayerCharacter,
    ConvertHonkaiStarRailPlayerCharacter,
    ConvertNonePlayerCharacter,
    BetterFBXImport,
    BetterFBXExport,
    Hoyo2VRCModelPanel,
    Hoyo2VRCToggleMenu,
    Hoyo2VRCToggleMenuButton,
    Hoyo2VRCSettingsPanel,
    InstallDependencies

]

def register():
    bpy.types.Scene.merge_all_meshes = bpy.props.BoolProperty(
        name="Merge All Meshes",
        description="Decide whether all meshes should be merged or not",
        default = False
    )

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)