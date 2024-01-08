import os
import bpy
import importlib

class CheckAndInstallDependencies:
    '''Check and Install Dependencies'''

    def __init__(self):
        """
        Check if specified addons are installed and enabled, and install them if not
        """
        # Define path to your downloaded script
        rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_script_dir = os.path.join(rootdir, 'Dependencies')

        # Define a list of the files in this folder, i.e. directory. The method listdir() will return this list from our folder of downloaded scripts. 
        file_list = sorted(os.listdir(path_to_script_dir))

        # Further specify that of this list of files, you only want the ones with the .zip extension.
        script_list = [item for item in file_list if item.endswith('.zip')]

        # Specify which add-ons you want enabled, their required versions, and their corresponding file names
        enableTheseAddons = {
            'cats-blender-plugin-development': ('cats.zip', '(0, 19, 0)'),
            'better_fbx': ('betterfbx.zip', '(5, 1, 1)')
        }

        # Check if the required add-ons are installed and enabled
        installed_addons = {addon.module: addon for addon in bpy.context.preferences.addons}

        for addon, (addon_file, required_version) in enableTheseAddons.items():
            if addon in installed_addons:
                # The add-on is installed, so check its version
                module = importlib.import_module(addon)
                installed_version = str(module.bl_info['version'])
                if installed_version == required_version:
                    # The installed version is the required version
                    print(f"Addon {addon} is installed and enabled with the required version {required_version}.")
                else:
                    # The installed version is not the required version, so install it
                    self.install_addon(addon, addon_file, path_to_script_dir, script_list)
            else:
                # The add-on is not installed, so install it
                self.install_addon(addon, addon_file, path_to_script_dir, script_list)

    def install_addon(self, addon, addon_file, path_to_script_dir, script_list):
        for file in script_list:
            if addon_file == file:
                path_to_file = os.path.join(path_to_script_dir, file)
                def install_and_enable_addon():
                    # Display a warning message
                    bpy.ops.ui.show_message_box(message=f"Warning: The existing version of the {addon} addon will be removed and replaced with a new version. This will also remove any user settings for the addon.")
                    # Remove the existing version of the addon
                    bpy.ops.preferences.addon_remove(module=addon)
                    # Install the new version of the addon
                    bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=path_to_file, filter_folder=True, filter_python=False, filter_glob="*.py;*.zip")
                    bpy.ops.preferences.addon_refresh()  # Refresh the addons list
                    print(f"Attempting to enable addon: {addon}")  # Print the addon name before trying to enable it
                    bpy.ops.preferences.addon_enable(module=addon)
                    print(f"Addon {addon} has been installed and enabled.")
                bpy.app.timers.register(install_and_enable_addon)
                break

# Create an instance of the CheckAndInstallDependencies class
check_and_install_dependencies = CheckAndInstallDependencies()