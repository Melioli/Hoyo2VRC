import bpy

# Define all settings in a dictionary
settings = {
    "merge_all_meshes": bpy.props.BoolProperty(
        name="Merge All Meshes",
        description="Toggle to merge all meshes into a single mesh during conversion.",
        default=False,
    ),
    "connect_chest_to_neck": bpy.props.BoolProperty(
        name="Connect Chest Tail to Neck",
        description="Toggle to connect the Chest bone tail to the Neck bone instead of the Upper Chest bone.",
        default=False,
    ),
    "connect_twist_to_limbs": bpy.props.BoolProperty(
        name="Connect Twist bones Tails to Limbs",
        description="Toggle to directly connect twist bones' tails to limbs (e.g., ArmTwist directly connected to Elbow)",
        default=False,
    ),
    "reconnect_armature": bpy.props.BoolProperty(
        name="Reconnect Armature",
        description="Toggle to reconnect armature bones during model conversion. (Turn off for NPC models.)",
        default=True,
    ),
    "humanoid_armature_fix": bpy.props.BoolProperty(
        name="Humanoid Armature Fixing",
        description="Toggle to fix the Armature based on Humanoid/VRC SDK/Full-Body-Tracking (On by default, disable for non-humanoid models).",
        default=True,
    ),
    "generate_shape_keys": bpy.props.BoolProperty(
        name="Generate Shape Keys",
        description="Toggle to generate shape keys during model conversion.",
        default=True,
    ),
    "keep_star_eye_mesh": bpy.props.BoolProperty(
        name="Keep Star Eye Mesh",
        description="Toggle to keep the Star Eye mesh during model conversion.",
        default=False,
    ),
}


def register_settings():
    for setting, prop in settings.items():
        setattr(bpy.types.Scene, setting, prop)


def unregister_settings():
    for setting in settings.keys():
        delattr(bpy.types.Scene, setting)
