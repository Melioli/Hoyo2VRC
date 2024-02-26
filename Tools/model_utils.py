import re
import bpy
from . import blender_utils


def IdentifyModel(name):
    name = (
        name.replace(".001", "")
        .replace("_Render", "")
        .replace("_merge", "")
        .replace(" (merge)", "")
        .replace("_Edit", " ")
    )

    game = None
    body_type = None
    model_name = None

    patterns = [
        # Genshin Impact Playable character
        (
            r"^(Cs_Avatar|Avatar|NPC_Avatar)_(Boy|Girl|Lady|Male|Loli)_(Sword|Claymore|Bow|Catalyst|Pole)_([a-zA-Z]+)(?<!_\d{2})$",
            "Genshin Impact",
            2,
            4,
        ),
        # Honkai Star Rail Playable Character
        (
            r"^(Player|Avatar|Art|NPC_Avatar)_([a-zA-Z]+)_?(?<!_\d{2})\d{2}$",
            "Honkai Star Rail",
            None,
            2,
        ),
        # Honkai Impact Playable Character
        (r"^(Avatar|Assister)_\w+?_C\d+(_\w+)$", "Honkai Impact", None, 1),
    ]

    for pattern, game_name, body_type_group, model_name_group in patterns:
        match = re.match(pattern, name)
        if match:
            game = game_name
            body_type = (
                match.group(body_type_group) if body_type_group is not None else None
            )
            model_name = (
                match.group(model_name_group) if model_name_group is not None else None
            )
            break
    else:
        game = "NPC"
        body_type = None
        model_name = None

    return game, body_type, model_name


def IsValidModel(obj):
    # Check if the object is an armature
    return obj.type == "ARMATURE"


def GetOrientations(armature):
    x_cord = 0
    y_cord = 1
    z_cord = 2
    fbx = False
    return x_cord, y_cord, z_cord, fbx

    keyBlock = [x for x in bpy.data.shape_keys if x.key_blocks.get(f"{keyName}")]
    if keyBlock:
        # print(keyBlock)
        return keyBlock[-1].name


def ScaleModel():
    for ob in bpy.context.scene.objects:
        if ob.type == "ARMATURE":
            ob.select_set(True)

            # Get the dimensions of the armature
            dimensions = ob.dimensions

            # Check the Z dimension and scale accordingly
            if dimensions.z > 100:
                bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
            elif dimensions.z > 10:
                bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
            elif 1 < dimensions.z < 3:
                pass  # Do nothing
            elif dimensions.z < 1:
                bpy.ops.transform.resize(value=(100, 100, 100))

            ob.select_set(False)


def RemoveEmpties():
    for ob in bpy.context.scene.objects:
        if ob.type == "EMPTY":
            ob.select_set(True)
            Empties = ob
            bpy.data.objects.remove(Empties, do_unlink=True)


def ClearRotations():
    for ob in bpy.context.scene.objects:
        if ob.type == "ARMATURE":
            ob.select_set(True)
            ob.rotation_euler = [0, 0, 0]
            ob.select_set(False)


def CleanMeshes():
    for obj in bpy.data.objects:
        if obj.type == "MESH" and (
            obj.name in ["EffectMesh", "EyeStar", "Weapon_L", "Weapon_R"]
            or "lod" in obj.name.lower()
        ):
            bpy.data.objects.remove(obj, do_unlink=True)


def JoinObjects(target_obj):

    # Set the mode to OBJECT
    blender_utils.ChangeMode("OBJECT")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # Select the target object
    target_obj.select_set(True)

    # Set the target object as the active object
    bpy.context.view_layer.objects.active = target_obj

    # Join the selected objects
    bpy.ops.object.join()

    blender_utils.ChangeMode("OBJECT")


def MergeFaceByDistance(target_obj_name, obj_names_to_merge, shapekey_name):
    # Get the target object
    target_obj = bpy.data.objects.get(target_obj_name)
    if target_obj is None:
        print(f"Target object {target_obj_name} not found")
        return

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # Select the target object
    target_obj.select_set(True)

    # Select the objects to merge
    for obj_name in obj_names_to_merge:
        obj = bpy.data.objects.get(obj_name)
        if obj is not None:
            obj.select_set(True)
        else:
            print(f"Object {obj_name} not found")

    # Set the target object as the active object
    bpy.context.view_layer.objects.active = target_obj

    # Join the selected objects into the active object
    bpy.ops.object.join()

    # Store the current active shape key index
    current_active_shape_key_index = target_obj.active_shape_key_index

    # Set the active shape key to the specified one
    target_obj.active_shape_key_index = (
        target_obj.data.shape_keys.key_blocks.keys().index(shapekey_name)
    )

    # Set the shape key value
    target_obj.data.shape_keys.key_blocks[shapekey_name].value = 1.0

    # Switch to edit mode
    blender_utils.ChangeMode("EDIT")

    # Select all vertices
    bpy.ops.mesh.select_all(action="SELECT")

    # Merge vertices by distance
    bpy.ops.mesh.remove_doubles(threshold=0.0001)

    # Deselect all vertices
    bpy.ops.mesh.select_all(action="DESELECT")

    # Switch back to object mode
    blender_utils.ChangeMode("OBJECT")

    # Reset the shape key value to 0
    target_obj.data.shape_keys.key_blocks[shapekey_name].value = 0

    # Restore the active shape key index
    target_obj.active_shape_key_index = current_active_shape_key_index


def MergeMeshes():
    if bpy.context.scene.merge_all_meshes:
        # Deselect all objects
        bpy.ops.object.select_all(action="DESELECT")

        # Select all mesh objects
        mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
        for obj in mesh_objects:
            obj.select_set(True)

        # Set the active object to the first selected mesh
        bpy.context.view_layer.objects.active = mesh_objects[0]

        # Join the selected objects
        bpy.ops.object.join()

        # Rename the active object to "Body"
        bpy.context.active_object.name = "Body"
    else:

        pass


def GetMeshes():
    return [obj for obj in bpy.data.objects if obj.type == "MESH"]


def ClearAnimations():
    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        # Check if the object has animation data
        if obj.animation_data is not None:
            # Clear all animation data
            obj.animation_data_clear()

    # Remove all actions
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)


def ApplyFaceMask(object_name, group_name):

    # Get the object from the scene
    obj = bpy.context.scene.objects.get(object_name)

    # Check if the object exists
    if obj is None:
        print(f"Object {object_name} not found")
        return

    # Create a new vertex group with the given name
    obj.vertex_groups.new(name=group_name)

    # Get the created vertex group
    vertex_group = obj.vertex_groups.get(group_name)

    # Check if the vertex group was created
    if vertex_group is None:
        print(f"Vertex group {group_name} not found")
        return

    # Assign all vertices of the object to the vertex group
    for vertex in obj.data.vertices:
        vertex_group.add([vertex.index], 1.0, "REPLACE")
