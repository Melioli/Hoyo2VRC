import bpy
from . import model_utils, blender_utils


def getKeyBlock(keyName, obj=None):
    if obj is None:
        obj = bpy.context.active_object
    if obj.data.shape_keys:
        kb = obj.data.shape_keys.key_blocks.get(keyName)
        return kb
    return None


def GenerateShapeKey(target_object_name, shapekey_name, mix, fallback_shapekeys=None):
    target_object = bpy.data.objects[target_object_name]
    
    if target_object.data.shape_keys is None:
        target_object.shape_key_add(name='Basis')

    new_key = target_object.shape_key_add(name=shapekey_name)
    new_key.value = 0.0  # Set the initial value to 0 instead of 1

    # Store original shape key values
    original_values = {}

    # First pass: set shape key values and store originals
    for item in mix:
        if len(item) == 2:
            obj_name, key_name = target_object_name, item[0]
            value = item[1]
        elif len(item) == 3:
            obj_name, key_name, value = item
        else:
            print(f"Invalid mix item: {item}. Skipping.")
            continue

        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"Object {obj_name} not found. Skipping.")
            continue

        if obj not in original_values:
            original_values[obj] = {key.name: key.value for key in obj.data.shape_keys.key_blocks}

        key_block = getKeyBlock(key_name, obj)
        if key_block is None:
            if fallback_shapekeys:
                fallback_key_name = next((fallback for key, fallback, _ in fallback_shapekeys if key == key_name), None)
                if fallback_key_name:
                    key_block = getKeyBlock(fallback_key_name, obj)
                    if key_block:
                        print(f"Using fallback shape key {fallback_key_name} for {key_name} in {obj.name}")
                    else:
                        print(f"Fallback shape key {fallback_key_name} not found in {obj.name}. Skipping.")
                        continue
                else:
                    print(f"No fallback found for shape key {key_name} in {obj.name}. Skipping.")
                    continue
            else:
                print(f"Shape key {key_name} not found in {obj.name} and no fallbacks provided. Skipping.")
                continue

        key_block.value = value

    # Second pass: calculate and apply the new vertex positions
    for vert_index in range(len(target_object.data.vertices)):
        final_co = target_object.data.shape_keys.reference_key.data[vert_index].co.copy()
        
        for item in mix:
            if len(item) == 2:
                obj_name, key_name = target_object_name, item[0]
                value = item[1]
            elif len(item) == 3:
                obj_name, key_name, value = item
            else:
                continue

            obj = bpy.data.objects.get(obj_name)
            if obj is None:
                continue

            key_block = getKeyBlock(key_name, obj)
            if key_block is None:
                continue

            if obj == target_object:
                final_co += (key_block.data[vert_index].co - obj.data.shape_keys.reference_key.data[vert_index].co) * value
            elif vert_index < len(key_block.data):
                # For other objects, we assume the vertex order is the same
                final_co += (key_block.data[vert_index].co - obj.data.shape_keys.reference_key.data[vert_index].co) * value

        new_key.data[vert_index].co = final_co

    # Reset shape keys to their original values
    for obj, values in original_values.items():
        for key in obj.data.shape_keys.key_blocks:
            key.value = values.get(key.name, 0)

    new_key.value = 0.0  # Ensure the new shape key's value is set to 0 after creation

    return new_key


def GetShapeKey(object_name, shape_name):
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    if bpy.context.object.data.shape_keys == None:
        return None
    for shape_key in bpy.context.object.data.shape_keys.key_blocks:
        if shape_key.name == shape_name:
            return shape_key

def ResetPose(root_object):
    bpy.context.view_layer.objects.active = root_object
    blender_utils.ChangeMode("POSE")
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.transforms_clear()
    blender_utils.ChangeMode("OBJECT")

def FaceRigToShapekey(root=None, meshname="Face"):
    # If no root object is provided, use the active object
    if root is None:
        root = bpy.context.active_object

    # Find the first armature in the scene if root is not an armature
    if root.type != "ARMATURE":
        root = next((obj for obj in bpy.data.objects if obj.type == "ARMATURE"), None)
        if root is None:
            print("No armature found in the scene.")
            return

    face_obj = bpy.data.objects.get(meshname)
    if face_obj is None:
        print(f"No object found with name {meshname}.")
        return

    if not bpy.data.actions:
        print("No Animations Found.")
        return

    for action in bpy.data.actions:
        if ".00" in action.name or "Emo_" not in action.name:
            continue

        print(action.name)
        arr = action.name.split("_")
        shapekey_name = "_".join(arr[2:])

        if action is not None:
            root.animation_data.action = action
            bpy.ops.object.visual_transform_apply()

        bpy.context.view_layer.objects.active = face_obj
        bpy.ops.object.modifier_apply_as_shapekey(
            keep_modifier=True, modifier=face_obj.modifiers[0].name
        )
        shapekey = GetShapeKey(face_obj.name, face_obj.modifiers[0].name)
        shapekey.name = shapekey_name

        ResetPose(root)
        
def RemoveShapeKeys(shape_key_names, object_name):
    obj = bpy.data.objects.get(object_name)
    if obj is None or obj.data.shape_keys is None:
        print(f"No shape keys found for object '{object_name}'.")
        return

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    for shape_key_name in shape_key_names:
        if shape_key_name in obj.data.shape_keys.key_blocks:
            # Set the active shape key to the one we want to remove
            obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index(shape_key_name)
            # Remove the active shape key
            bpy.ops.object.shape_key_remove(all=False)