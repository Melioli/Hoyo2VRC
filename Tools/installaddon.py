import os
import bpy
from bpy.types import Operator

class InstallDependencies(Operator):
    '''Install Dependencies'''
    bl_idname = 'hoyo2vrc.install_addons'
    bl_label = 'Hoyo2VRC: Install Dependencies'

    def execute(self, context):
        """
        Import
        1. Install CATS
        2. Install BetterFBX
        """
        # Define path to your downloaded script
        rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_script_dir = os.path.join(rootdir, 'Dependencies')

        # Define a list of the files in this folder, i.e. directory. The method listdir() will return this list from our folder of downloaded scripts. 
        file_list = sorted(os.listdir(path_to_script_dir))

        # Further specify that of this list of files, you only want the ones with the .zip extension.
        script_list = [item for item in file_list if item.endswith('.zip')]
        
        # Clear the cache
        bpy.ops.wm.read_homefile(use_empty=True)

        # Specify the file path of the individual scripts (their names joined with the location of your downloaded scripts folder) then use wm.addon_install() to install them. 
        for file in script_list:
            path_to_file = os.path.join(path_to_script_dir, file)
            bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=path_to_file, filter_folder=True, filter_python=False, filter_glob="*.py;*.zip")

        # Specify which add-ons you want enabled. For example, Crowd Render, Pie Menu Editor, etc. Use the script's python module. 
        enableTheseAddons = ['cats-blender-plugin-development', 'better_fbx']

        # Use addon_enable() to enable them.
        for string in enableTheseAddons: 
            name = enableTheseAddons
            bpy.ops.preferences.addon_enable(module = string)

        return {'FINISHED'}