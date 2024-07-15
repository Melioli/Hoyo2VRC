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

def CursorToObject(object_name, x_offset=0, y_offset=0.035):
    # Select the specified object
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        raise ValueError(f"Object '{object_name}' not found")

    # Set the object as the active object and select it
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')

    # Snap the cursor to the selected vertices
    original_area_type = bpy.context.area.type
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.context.area.type = original_area_type

    # Adjust the cursor location
    cursor_location = bpy.context.scene.cursor.location
    cursor_location.x += x_offset
    cursor_location.y += y_offset
    bpy.context.scene.cursor.location = cursor_location
    
    # Deselect the object
    obj.select_set(False)

    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
def ResetCursor():
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)