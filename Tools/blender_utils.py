import bpy


def GetBlenderVersion():
    return bpy.app.version


def ChangeMode(mode):
    valid_modes = [
        "OBJECT",
        "EDIT",
        "SCULPT",
        "VERTEX_PAINT",
        "WEIGHT_PAINT",
        "TEXTURE_PAINT",
        "PARTICLE_EDIT",
        "POSE",
    ]
    if mode in valid_modes:
        bpy.ops.object.mode_set(mode=mode)
    else:
        print(f"Invalid mode: {mode}. Please choose from {valid_modes}")


def SelectObject(obj_name):
    obj = bpy.data.objects.get(obj_name)
    if obj is not None:
        obj.select_set(True)
    return obj


def SetActiveObject(obj_name):
    obj = bpy.data.objects.get(obj_name)
    if obj is not None:
        bpy.context.view_layer.objects.active = obj
    return obj
