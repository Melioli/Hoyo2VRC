import bpy
from . import model_utils, blender_utils


def getKeyBlock(keyName):
    keyBlock = [x for x in bpy.data.shape_keys if x.key_blocks.get(f"{keyName}")]
    if keyBlock:
        # print(keyBlock)
        return keyBlock[-1].name


def GenerateShapeKey(object_name, shapekey_name, mix, fallback_shapekeys=None):
    # Set the value of the shape keys in the mix
    for key_name, value in mix:
        key_block = getKeyBlock(key_name)
        if key_block is not None:
            bpy.data.shape_keys[key_block].key_blocks[key_name].value = value
        elif fallback_shapekeys is not None:
            # Look for a fallback shape key
            fallback_key_name = next(
                (
                    fallback
                    for key, fallback, _ in fallback_shapekeys
                    if key == key_name
                ),
                None,
            )
            if fallback_key_name is not None:
                fallback_key_block = getKeyBlock(fallback_key_name)
                if fallback_key_block is not None:
                    bpy.data.shape_keys[fallback_key_block].key_blocks[
                        fallback_key_name
                    ].value = value

    # Add a new shape key from the mix
    new_shape_key = bpy.data.objects[object_name].shape_key_add(
        name=shapekey_name, from_mix=True
    )

    # Set the value of the new shape key to 1
    new_shape_key.value = 1

    # Reset all shape keys
    for key in bpy.data.objects[object_name].data.shape_keys.key_blocks:
        key.value = 0

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