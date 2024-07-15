import re
import bpy
import bmesh
from . import blender_utils
from mathutils import Vector


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
        # Wuthering Waves Playable Character
        (r"^(R2T1\w+|NH\w+)$", "Wuthering Waves", None, 1),
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

def RenameMeshToBody():
    # Get the mesh object in the scene
    mesh_object = next((obj for obj in bpy.data.objects if obj.type == "MESH"), None)

    # Check if a mesh object exists
    if mesh_object is not None:
        # Rename the mesh object to "Body"
        mesh_object.name = "Body"

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

def MergeFaceByDistance(target_obj_name, obj_names_to_merge, shapekey_name=None):
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

    # If shapekey_name is not None and target object has shape keys, apply the shapekey
    if shapekey_name is not None and target_obj.data.shape_keys is not None:
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

    # If shapekey_name is not None and target object has shape keys, reset the shape key value and restore the active shape key index
    if shapekey_name is not None and target_obj.data.shape_keys is not None:
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
        
def SelectVertByShapeKey(context, side, shape_key_name):
    TOL = 1e-5  # tolerance
    ob = context.edit_object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    # Find the shape key by name
    shape_key = ob.data.shape_keys.key_blocks.get(shape_key_name)
    if shape_key is None:
        raise ValueError(f"Shape key '{shape_key_name}' not found")

    # Find materials that end with the specified suffix
    eye_material_indices = {i for i, mat in enumerate(ob.data.materials) if mat and mat.name.endswith('Eye') or mat.name.endswith('Eyes')}

    # Gather vertices connected to faces with the "Eye" material
    eye_verts = {v.index for face in bm.faces if face.material_index in eye_material_indices for v in face.verts}

    # Select vertices affected by the shape key and connected to the "Eye" material
    for v in bm.verts:
        if v.index in eye_verts:
            bv = me.vertices[v.index]
            v.select = (shape_key.data[v.index].co - bv.co).length > TOL
            if side == 'L' and v.co[0] < 0:
                v.select = False
            elif side == 'R' and v.co[0] >= 0:
                v.select = False

    bpy.ops.mesh.select_more(use_face_step=False)
    bmesh.update_edit_mesh(me)

def RemoveMaterials(obj, remove_suffixes=None, keep_suffixes=None):
    bpy.context.view_layer.objects.active = obj  # Set the active object context
    if remove_suffixes:
        # Remove materials that end with any of the specified suffixes
        for i in reversed(range(len(obj.material_slots))):
            mat = obj.material_slots[i].material
            if mat and any(mat.name.endswith(suffix) for suffix in remove_suffixes):
                obj.active_material_index = i
                bpy.ops.object.material_slot_remove()
    elif keep_suffixes:
        # Remove all materials except those that end with any of the specified suffixes
        for i in reversed(range(len(obj.material_slots))):
            mat = obj.material_slots[i].material
            if mat and not any(mat.name.endswith(suffix) for suffix in keep_suffixes):
                obj.active_material_index = i
                bpy.ops.object.material_slot_remove()

def CalculateEyeCenters():
    eye_centers = {}

    for eye_name in ["Left Eye", "Right Eye"]:
        eye_obj = bpy.data.objects.get(eye_name)
        if eye_obj is None:
            raise ValueError(f"Object '{eye_name}' not found")

        # Ensure the eye object is selected and active
        bpy.context.view_layer.objects.active = eye_obj
        eye_obj.select_set(True)

        # Calculate the center of the eye mesh
        bm = bmesh.new()
        bm.from_mesh(eye_obj.data)
        eye_center = sum((eye_obj.matrix_world @ v.co for v in bm.verts), Vector()) / len(bm.verts)
        bm.free()

        # Store the center in the dictionary
        eye_centers[eye_name] = eye_center

    return eye_centers
