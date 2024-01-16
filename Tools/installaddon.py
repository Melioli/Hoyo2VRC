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
            'better_fbx': ('betterfbx.zip', '(5, 4, 8)')
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

    def install_and_enable_addon(addon):
        # Check if the addon is already installed
        if addon in bpy.context.preferences.addons.keys():
            # Get the window and screen
            window = bpy.context.window
            screen = window.screen

            # Get the preferences area
            for area in screen.areas:
                if area.type == 'PREFERENCES':
                    break
            else:
                # No preferences area, raise an error
                raise RuntimeError("No preferences area")

            # Override the context
            override = {'window': window, 'screen': screen, 'area': area}

            # Remove the existing version of the addon
            bpy.ops.preferences.addon_remove(override, module=addon)

        # Install and enable the new version of the addon
        bpy.ops.preferences.addon_install(filepath=addon)
        bpy.ops.preferences.addon_enable(module=addon)

# Create an instance of the CheckAndInstallDependencies class
check_and_install_dependencies = CheckAndInstallDependencies()

# Register the instance as a handler for the load_post event
bpy.app.handlers.load_post.append(check_and_install_dependencies)