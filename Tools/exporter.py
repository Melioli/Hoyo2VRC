import bpy
import bpy_types
import bmesh
import math
import mathutils
import sys
import os
import shutil
import time
import platform
import subprocess
import idprop
import copy
import uuid
from bpy.props import *
import bpy_extras


def save_frame_rate(f, frame_rate):
    item_list = ["FrameRate", str(frame_rate)]
    f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_hierarchy_dic(f, hierarchy_dic):
    for (key, value) in hierarchy_dic.items():
        item_list = ["Hierarchy", key, value[0], value[1].replace(",", "\\;"), value[2]]
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_node_dic(f, node_dic):
    for (key, value) in node_dic.items():
        for (key2, value2) in value.items():
            for item in value2:
                item_list = ["Node", key, key2, item[0].replace(",", "\\;"), str(item[1])]
                f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_default_pose_dic(f, default_pose_dic):
    for (key, value) in default_pose_dic.items():
        item_list = ["DefaultPose", str(key)]
        item_list.extend(["{:.8f}".format(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_bind_pose_dic(f, bind_pose_dic):
    for (key, value) in bind_pose_dic.items():
        item_list = ["BindPose", str(key)]
        item_list.extend(["{:.8f}".format(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_pose_key_dic(f, pose_key_dic):
    for (key, value) in pose_key_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["PoseKey", str(key), str(key2), str(len(value)), str(value2[0])]
            item_list.extend(["{:.8f}".format(item) for item in value2[1]])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_vertex_dic(f, vertex_dic):
    for (key, value) in vertex_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["Vertex", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def take_second_from_token(token):
    return token[1]


def save_weight_dic(f, weight_dic, my_max_bone_influences):
    for (key, value) in weight_dic.items():
        for (key2, value2) in enumerate(value):
            # sort weights reversely
            value2.sort(key=take_second_from_token, reverse=True)
            # truncate weights
            if my_max_bone_influences != 'Unlimited':
                value2 = value2[:min(len(value2), int(my_max_bone_influences))]
            # normalize weights
            sum = 0.0
            for token in value2:
                sum += token[1]
            if sum > 0.0:
                for token in value2:
                    token[1] /= sum
            item_list = ["Weight", str(key), str(key2), str(len(value))]
            item_list.extend([str(item2) for item in value2 for item2 in item])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_shape_dic(f, shape_dic):
    for (key, value) in shape_dic.items():
        item_list = ["Shape", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_shape_key_dic(f, shape_key_dic):
    for (key, value) in shape_key_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["ShapeKey", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_camera_key_dic(f, camera_key_dic):
    for (key, value) in camera_key_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["CameraKey", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_polygon_dic(f, polygon_dic):
    for (key, value) in polygon_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["Polygon", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_uv_dic(f, uv_dic):
    for (key, value) in uv_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["UV", str(key), str(key2), str(len(value))]
            item_list.extend([str(item2) for item in value2 for item2 in item])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_tangent_dic(f, tangent_dic):
    for (key, value) in tangent_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["Tangent", str(key), str(key2), str(len(value))]
            item_list.extend([str(item2) for item in value2 for item2 in item])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_normal_dic(f, normal_dic):
    for (key, value) in normal_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["Normal", str(key), str(key2), str(len(value))]
            item_list.extend([str(item2) for item in value2 for item2 in item])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_color_dic(f, color_dic):
    for (key, value) in color_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["Color", str(key), str(key2), str(len(value))]
            item_list.extend([str(item2) for item in value2 for item2 in item])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_texture_dic(f, texture_dic):
    for (key, value) in texture_dic.items():
        item_list = ["Texture", str(key), value[0].replace(",", "\\;"), value[1].replace(",", "\\;")]
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_material_dic(f, material_dic):
    for (key, value) in material_dic.items():
        item_list = ["Material", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_mesh_material_dic(f, mesh_material_dic):
    for (key, value) in mesh_material_dic.items():
        item_list = ["MeshMaterial", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_polygon_material_dic(f, polygon_material_dic):
    for (key, value) in polygon_material_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["PolygonMaterial", str(key), str(key2), str(len(value)), str(value2)]
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_camera_dic(f, camera_dic):
    for (key, value) in camera_dic.items():
        item_list = ["Camera", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_light_dic(f, light_dic):
    for (key, value) in light_dic.items():
        item_list = ["Light", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_vertex_animation_dic(f, vertex_animation_dic):
    for (key, value) in vertex_animation_dic.items():
        for (key2, value2) in enumerate(value):
            for (key3, value3) in enumerate(value2[1]):
                item_list = ["VertexPoseKey", str(key), str(key2), str(len(value)), str(value2[0]), str(key3), str(len(value2[1]))]
                item_list.extend([str(item) for item in value3])
                f.write("[{}]\r\n".format(",".join(item_list)))
            f.write("\r\n")
        f.write("\r\n")


def save_custom_property_dic(f, custom_property_dic):
    for (key, value) in custom_property_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["CustomProperty", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_edge_crease_dic(f, edge_crease_dic):
    for (key, value) in edge_crease_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["EdgeCrease", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_edge_smoothing_dic(f, edge_smoothing_dic):
    for (key, value) in edge_smoothing_dic.items():
        for (key2, value2) in enumerate(value):
            item_list = ["EdgeSmoothing", str(key), str(key2), str(len(value))]
            item_list.extend([str(item) for item in value2])
            f.write("[{}]\r\n".format(",".join(item_list)))
        f.write("\r\n")


def save_ik_dic(f, ik_dic):
    for (key, value) in ik_dic.items():
        item_list = ["IK", str(key)]
        item_list.extend([str(item) for item in value])
        f.write("[{}]\r\n".format(",".join(item_list)))
    f.write("\r\n")


def save_current_selections(context, current_selection_dic):
    for ob in context.scene.objects:
        current_selection_dic[ob] = ob.select_get()

def restore_current_selections(context, current_selection_dic):
    for ob in context.scene.objects:
        ob.select_set(current_selection_dic[ob])

def save_current_poses(context, context_objects, current_pose_dic):
    for ob in context_objects:
        if ob.type == 'ARMATURE':
            current_pose_dic[ob] = {}
            for bone in ob.pose.bones:
                current_pose_dic[ob][bone] = copy.deepcopy(bone.matrix_basis)


def restore_current_poses(context, context_objects, current_pose_dic):
    for ob in context_objects:
        if ob.type == 'ARMATURE':
            for bone in ob.pose.bones:
                bone.matrix_basis = current_pose_dic[ob][bone]


def reset_all_armatures(context, context_objects):
    for ob in context_objects:
        if ob.type == 'ARMATURE':
            save_hide_viewport = ob.hide_viewport
            save_hidden = ob.hide_get()
            # make visible
            ob.hide_viewport = False
            ob.hide_set(False)
            # deselect all
            for selected_obj in context.selected_objects:
                selected_obj.select_set(False)
            # select the object
            ob.select_set(True)
            # must set to active object
            context.view_layer.objects.active = ob
            # save bone selection status
            bone_selection_list = []
            for bone in ob.data.bones:
                bone_selection_list.append(bone.select)
            # must be in pose mode to reset transform of selected bones
            bpy.ops.object.mode_set(mode='POSE', toggle=False)
            # select all bones
            bpy.ops.pose.select_all(action='SELECT')
            # Reset location, rotation, and scaling of selected bones to their default values
            bpy.ops.pose.transforms_clear()
            # exit pose mode
            bpy.ops.object.mode_set(mode='OBJECT')
            # restore bone selection status
            for (i, bone) in enumerate(ob.data.bones):
                bone.select = bone_selection_list[i]
            # restore hidden status
            ob.hide_viewport = save_hide_viewport
            ob.hide_set(save_hidden)


def fix_parent_for_rigify_bones(hierarchy_dic):
    # try setting parent for each bone in hierarchy
    for (key, value) in hierarchy_dic.items():
        # fix parent for bone
        if value[0] == 'BONE':
            ob = value[-1]
            parent_node = ob.parent
            found = False
            while parent_node != None:
                parent_name = parent_node.name
                # fix parent name to match deform bone
                if parent_name.startswith("tweak_"):
                    parent_name = "DEF-{}".format(parent_name[6:])
                elif parent_name.startswith("MCH-") and parent_name.find("_tweak.") != -1:
                    idx = parent_name.find("_tweak.")
                    parent_name = "DEF-{}{}".format(parent_name[4:idx], parent_name[idx+6:])
                elif parent_name.startswith("MCH-"):
                    parent_name = "DEF-{}".format(parent_name[4:])
                elif parent_name.startswith("ORG-"):
                    grandparent = parent_node.parent
                    if grandparent != None:
                        siblings = grandparent.children
                        found2 = False
                        for sibling in siblings:
                            sibling_name = sibling.name
                            if sibling_name == "MCH-{}".format(parent_name[4:]):
                                found2 = True
                                break
                        if not found2:
                            parent_name = "DEF-{}".format(parent_name[4:])
                    else:
                        parent_name = "DEF-{}".format(parent_name[4:])
                elif parent_name.startswith("eye_master."):
                    parent_name = "DEF-{}".format(parent_name)

                # ignore itself
                if value[1] != parent_name:
                    for (key2, value2) in hierarchy_dic.items():
                        if value2[1] == parent_name:
                            hierarchy_dic[key][2] = key2
                            found = True
                            break
                    if found:
                        break
                parent_node = parent_node.parent


def get_hierarchy_key_from_empty_name(hierarchy_dic, empty_name):
    for (key, value) in hierarchy_dic.items():
        if value[0] == 'EMPTY' and value[1] == empty_name:
            return key
    return None


def get_hierarchy_key_from_armature_key_and_bone_name(hierarchy_dic, armature_key, bone_name):
    for (key, value) in hierarchy_dic.items():
        if value[0] == 'BONE':
            tokens = key.split(".")
            if len(tokens) == 2 and tokens[0] == armature_key:
                if value[1] == bone_name:
                    return key
    return armature_key


def make_hierarchy_dic(hierarchy_dic, use_only_deform_bones, use_rigify_armature, use_rigify_root_bone, use_only_selected_deform_bones, block_list, context_objects):
    for (index, ob) in enumerate(context_objects):
        if ob.type in ['ARMATURE', 'MESH', 'EMPTY', 'CAMERA', 'LAMP', 'LIGHT']:
            # ignore mesh with zero polygons
            if ob.type == 'MESH' and len(ob.data.polygons) == 0:
                continue
            hierarchy_dic[str(index)] = ['LIGHT' if ob.type == 'LAMP' or ob.type == 'LIGHT' else ob.type, ob.name, str(-1), None, ob]
            # add bones of the armature
            if ob.type == 'ARMATURE':
                for (index2, bone) in enumerate(ob.data.bones):
                    if not use_only_deform_bones or \
                        (bone.use_deform and not use_only_selected_deform_bones) or \
                        (bone.use_deform and use_only_selected_deform_bones and bone.select) or \
                        (use_rigify_armature and use_rigify_root_bone and bone.name == "root"):
                        # ip like identifier
                        hierarchy_dic[".".join([str(index), str(index2)])] = ["BONE", bone.name, str(index), ob, bone]
                    # add to block list
                    if use_only_deform_bones and bone.use_deform and use_only_selected_deform_bones and not bone.select:
                        block_list.append((ob.name, bone.name))
    # try setting parent for each hierarchy item
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        parent_node = ob.parent
        found = False
        while parent_node != None:
            for (key2, value2) in hierarchy_dic.items():
                if value2[-1] == parent_node:
                    # object attach to bone
                    if value[0] != 'BONE' and ob.parent_bone != "" and ob.parent_type == 'BONE':
                        hierarchy_dic[key][2] = get_hierarchy_key_from_armature_key_and_bone_name(hierarchy_dic, key2, ob.parent_bone)
                    else:
                        hierarchy_dic[key][2] = key2
                    found = True
                    break
            if found:
                break
            parent_node = parent_node.parent
    # fix parents for Rigify armature
    if use_rigify_armature:
        fix_parent_for_rigify_bones(hierarchy_dic)


def make_default_pose_dic(default_pose_dic, ob_parent, ob, is_bone, bone_correction_matrix):
    index = len(default_pose_dic)
    default_pose_dic[index] = []
    default_pose = (ob.matrix_world if ob.type not in ['CAMERA', 'LIGHT'] else ob.matrix_world @ mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y' if ob.type == 'CAMERA' else 'X')) if ob_parent == None else ob_parent.matrix_world @ ob.matrix_local
    # user defined axis
    if is_bone and bone_correction_matrix != None:
        default_pose = default_pose @ bone_correction_matrix
    for row in default_pose.transposed():
        for item in row:
            default_pose_dic[index].append(item)
    return index


def make_bind_pose_dic(bind_pose_dic, ob_parent, ob, is_bone, bone_correction_matrix):
    index = len(bind_pose_dic)
    bind_pose_dic[index] = []
    bind_pose = (ob.matrix_world if ob.type not in ['CAMERA', 'LIGHT'] else ob.matrix_world @ mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y' if ob.type == 'CAMERA' else 'X')) if ob_parent == None else ob_parent.matrix_world @ ob.matrix_local
    # user defined axis
    if is_bone and bone_correction_matrix != None:
        bind_pose = bind_pose @ bone_correction_matrix
    for row in bind_pose.transposed():
        for item in row:
            bind_pose_dic[index].append(item)
    return index


def make_vertex_dic(vertex_dic, ob, exist_object_dic):
    keyword = ('Vertex', ob.data.vertices)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make vertex dic
        index = len(vertex_dic)
        length = len(ob.data.vertices)
        vertex_dic[index] = [None] * length
        for (i, vertex) in enumerate(ob.data.vertices):
            vertex_dic[index][i] = (vertex.co[0], vertex.co[1], vertex.co[2])
        exist_object_dic[keyword] = index
    return index


def make_camera_dic(camera_dic, ob, exist_object_dic):
    keyword = ('CAMERA', ob.data)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make camera dic
        index = len(camera_dic)
        camera_dic[index] = [ob.data.type, ob.data.lens, 1 if ob.data.dof.use_dof else 0, ob.data.dof.focus_distance, math.degrees(ob.data.angle), math.degrees(ob.data.angle_x), math.degrees(ob.data.angle_y), ob.data.lens_unit, ob.data.clip_start, ob.data.clip_end, ob.data.sensor_width, ob.data.sensor_height, ob.data.shift_x, ob.data.shift_y]
        exist_object_dic[keyword] = index
    return index


def make_light_dic(light_dic, ob, exist_object_dic):
    keyword = ('LIGHT', ob.data)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make light dic
        index = len(light_dic)
        light_dic[index] = [ob.data.type, ob.data.energy, ob.data.color[0], ob.data.color[1], ob.data.color[2]]
        exist_object_dic[keyword] = index
    return index


def make_custom_property_dic(custom_property_dic, ob, exist_object_dic):
    keyword = ('CustomProperty', ob.data if type(ob) != bpy.types.Bone and type(ob) != bpy.types.Material and ob.data != None else ob)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make custom property dic
        index = len(custom_property_dic)
        custom_property_list = []
        if len(ob.keys()) > 0:
            for key in ob.keys():
                if key not in '_RNA_UI':
                    if type(ob[key]) is int:
                        key_type = 'INT'
                        custom_property_list.append([key, key_type, ob[key]])
                    elif type(ob[key]) is float:
                        key_type = 'FLOAT'
                        custom_property_list.append([key, key_type, ob[key]])
                    elif type(ob[key]) is str:
                        key_type = 'STRING'
                        custom_property_list.append([key, key_type, ob[key].replace(",", "\\;")])
                    elif type(ob[key]) is idprop.types.IDPropertyArray and len(ob[key]) in [2, 3, 4]:
                        key_type = 'VECTOR_FLOAT'
                        custom_property_list.append([key, key_type])
                        for value in ob[key].to_list():
                            custom_property_list[-1].append(value)
        if len(custom_property_list) == 0:
            return None
        custom_property_dic[index] = custom_property_list
        exist_object_dic[keyword] = index
    return index


def make_vertex_animation_dic(context, vertex_animation_dic, ob, exist_object_dic, use_vertex_space, use_timeline_range, my_animation_offset, my_vertex_frame_start, my_vertex_frame_end):
    keyword = ('VertexPoseKey', ob.data.vertices)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make vertex animation dic
        index = len(vertex_animation_dic)
        vertex_animation_dic[index] = []
        # we use the user defined range to avoid too many data exported
        (action_start, action_end) = (my_vertex_frame_start, my_vertex_frame_end)
        if use_timeline_range:
            (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
        for frame in range(action_start, action_end+1):
            bpy.context.scene.frame_set(frame)
            bpy.context.view_layer.update()
            depsgraph = bpy.context.evaluated_depsgraph_get()
            ob_eval = ob.evaluated_get(depsgraph)
            me = ob_eval.to_mesh()
            #me.calc_normals()
            vertex_matrix = ob.matrix_world
            normal_matrix = ob.matrix_world.inverted_safe().transposed()
            normal_matrix.translation = mathutils.Vector()
            normal_matrix.normalize()
            length = len(me.vertices)
            vertex_animation_dic[index].append([])
            vertex_animation_dic[index][-1].append(frame + my_animation_offset)
            vertex_animation_dic[index][-1].append([None] * length)
            for (i, vertex) in enumerate(me.vertices):
                position = vertex.co if use_vertex_space == "local" else vertex_matrix @ vertex.co
                normal = vertex.normal if use_vertex_space == "local" else normal_matrix @ vertex.normal
                vertex_animation_dic[index][-1][-1][i] = [position[0], position[1], position[2], normal[0], normal[1], normal[2]]
            ob_eval.to_mesh_clear()
        exist_object_dic[keyword] = index
    return index


def make_shape_dic(shape_dic, ob, exist_object_dic):
    keyword = ('Shape', ob.data.vertices)
    if keyword in exist_object_dic:
        name_index_pairs = exist_object_dic[keyword]
    else:
        # make shape dic
        name_index_pairs = []
        if ob.data.shape_keys != None:
            # we only export relative shape keys
            if ob.data.shape_keys.use_relative == True:
                bm = bmesh.new()
                bm.from_mesh(ob.data)
                # we assume that the first shape is the basis shape
                basis = bm.verts.layers.shape.values()[0]
                for (i, layer) in enumerate(bm.verts.layers.shape.values()):
                    # ignore the basis shape
                    if i != 0:
                        index = len(shape_dic)
                        shape_dic[index] = []
                        for (j, vertex) in enumerate(bm.verts):
                            if vertex[layer] != vertex[basis]:
                                shape_dic[index].append(j)
                                shape_dic[index].append(vertex[layer].x)
                                shape_dic[index].append(vertex[layer].y)
                                shape_dic[index].append(vertex[layer].z)
                        name_index_pairs.append((layer.name, index))
                bm.free  # free and prevent further access
        exist_object_dic[keyword] = name_index_pairs
    return name_index_pairs


def make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic):
    keyword = ('ShapeKey', shape_key_data, ob.data.vertices)
    if keyword in exist_object_dic:
        (action_name, index) = exist_object_dic[keyword]
    else:
        action_name = None
        index = None
        # make shape key dic
        if ob.data.shape_keys != None:
            if ob.data.shape_keys.animation_data != None:
                # driven by bone or by NLA track, bake the shape keys.
                if use_driver_based_shape_key or (my_animation_type == 'Active' and ob.data.shape_keys.animation_data.action == None):
                    # driven by bone?
                    (action_start, action_end) = get_pose_key_range(context, hierarchy_dic, my_animation_type)
                    # driven by NLA track?
                    if action_start == None and action_end == None:
                        (action_start, action_end) = get_shape_key_nla_frame_range(context, ob)
                    if use_timeline_range:
                        (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
                    # exists any pose key
                    if action_start != None and action_end != None:
                        index = len(shape_key_dic)
                        shape_key_dic[index] = []
                        action_name = "baked shape key"
                        for frame in range(action_start, action_end+1):
                            # set frame
                            context.scene.frame_set(frame)
                            bpy.context.view_layer.update()
                            values = []
                            for (i, block) in enumerate(ob.data.shape_keys.key_blocks.values()):
                                # ignore Basic channel
                                if i > 0:
                                    values.append(block.value)
                            shape_key_dic[index].append([])
                            shape_key_dic[index][-1].append(frame + my_animation_offset)
                            for i in range(len(values)):
                                # ignore Basic channel
                                shape_key_dic[index][-1].append(i+1)
                                shape_key_dic[index][-1].append(values[i])
                elif my_animation_type == 'Active' or my_animation_type == 'Actions':
                        index = len(shape_key_dic)
                        shape_key_dic[index] = []
                        action_name = ob.data.shape_keys.animation_data.action.name
                        (action_start, action_end) = [int(x) for x in ob.data.shape_keys.animation_data.action.frame_range]
                        if use_timeline_range:
                            (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
                        for frame in range(action_start, action_end+1):
                            values = []
                            for (i, block) in enumerate(ob.data.shape_keys.key_blocks.values()):
                                # ignore Basic channel
                                if i > 0:
                                    fcurve = ob.data.shape_keys.animation_data.action.fcurves.find(data_path=block.path_from_id("value"))
                                    if fcurve == None:
                                        values.append(0.0)
                                    else:
                                        values.append(fcurve.evaluate(frame))
                            shape_key_dic[index].append([])
                            shape_key_dic[index][-1].append(frame + my_animation_offset)
                            for i in range(len(values)):
                                # ignore Basic channel
                                shape_key_dic[index][-1].append(i+1)
                                shape_key_dic[index][-1].append(values[i])
                elif my_animation_type == 'Tracks':
                    (action_start, action_end) = get_shape_key_nla_frame_range(context, ob)
                    if use_timeline_range:
                        (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
                    # exists any pose key
                    if action_start != None and action_end != None:
                        index = len(shape_key_dic)
                        shape_key_dic[index] = []
                        action_name = get_shape_key_nla_track_name(context, ob)
                        for frame in range(action_start, action_end+1):
                            # set frame
                            context.scene.frame_set(frame)
                            bpy.context.view_layer.update()
                            values = []
                            for (i, block) in enumerate(ob.data.shape_keys.key_blocks.values()):
                                # ignore Basic channel
                                if i > 0:
                                    values.append(block.value)
                            shape_key_dic[index].append([])
                            shape_key_dic[index][-1].append(frame + my_animation_offset)
                            for i in range(len(values)):
                                # ignore Basic channel
                                shape_key_dic[index][-1].append(i+1)
                                shape_key_dic[index][-1].append(values[i])
        exist_object_dic[keyword] = (action_name, index)
    return (action_name, index)


def make_camera_key_dic(context, hierarchy_dic, camera_key_dic, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic):
    camera_key_data = None
    if ob.data.animation_data != None:
        if (my_animation_type == 'Active' or my_animation_type == 'Actions') and ob.data.animation_data.action != None:
            camera_key_data = ob.data.animation_data.action
        elif my_animation_type == 'Tracks':
            camera_key_data = get_active_camera_nla_track(context, ob)
    keyword = ('CameraKey', camera_key_data if camera_key_data != None else ob.data)
    if keyword in exist_object_dic:
        (action_name, index) = exist_object_dic[keyword]
    else:
        action_name = None
        index = None
        # make camera key dic
        if ob.data.animation_data != None:
            if (my_animation_type == 'Active' or my_animation_type == 'Actions') and ob.data.animation_data.action != None:
                index = len(camera_key_dic)
                camera_key_dic[index] = []
                action_name = ob.data.animation_data.action.name
                (action_start, action_end) = [int(x) for x in ob.data.animation_data.action.frame_range]
                if use_timeline_range:
                    (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
                fcurve = ob.data.animation_data.action.fcurves.find(data_path=ob.data.path_from_id("lens"))
                fcurve2 = ob.data.animation_data.action.fcurves.find(data_path=ob.data.dof.path_from_id("focus_distance"))
                for frame in range(action_start, action_end+1):
                    camera_key_dic[index].append([])
                    camera_key_dic[index][-1].append(frame + my_animation_offset)
                    camera_key_dic[index][-1].append(0.0 if not fcurve else fcurve.evaluate(frame))
                    camera_key_dic[index][-1].append(0.0 if not fcurve2 else fcurve2.evaluate(frame))
            elif my_animation_type == 'Tracks' and ob.data.animation_data.nla_tracks != None:
                index = len(camera_key_dic)
                camera_key_dic[index] = []
                action_name = get_camera_nla_track_name(context, ob)
                (action_start, action_end) = get_camera_nla_frame_range(context, ob)
                if use_timeline_range:
                    (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
                fcurve = ob.data.animation_data.action.fcurves.find(data_path=ob.data.path_from_id("lens"))
                fcurve2 = ob.data.animation_data.action.fcurves.find(data_path=ob.data.dof.path_from_id("focus_distance"))
                for frame in range(action_start, action_end+1):
                    camera_key_dic[index].append([])
                    camera_key_dic[index][-1].append(frame + my_animation_offset)
                    camera_key_dic[index][-1].append(0.0 if not fcurve else fcurve.evaluate(frame))
                    camera_key_dic[index][-1].append(0.0 if not fcurve2 else fcurve2.evaluate(frame))
        exist_object_dic[keyword] = (action_name, index)
    return (action_name, index)


def make_weight_dic(hierarchy_dic, weight_dic, ob, exist_object_dic, bone_dictionary, block_dictionary):
    keyword = ('Weight', ob.data.vertices)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make weight dic
        index = None
        bound_to_any_armature = False
        for mod in ob.modifiers:
            if type(mod) == bpy.types.ArmatureModifier:
                # ignore empty modifiers
                if mod.object != None:
                    bound_to_any_armature = True
                    break
        if bound_to_any_armature:
            if len(ob.vertex_groups) > 0:
                index = len(weight_dic)
                length = len(ob.data.vertices)
                weight_dic[index] = [None] * length
                for (i, vertex) in enumerate(ob.data.vertices):
                    temp_list = []
                    for group in vertex.groups:
                        group_index = group.group
                        # beyond vertex group range due to outdated data
                        if group_index not in range(len(ob.vertex_groups)):
                            continue
                        group_weight = group.weight
                        group_name = ob.vertex_groups[group_index].name
                        # search in dictionary
                        armature_key = None
                        bone_key = None
                        # we support multiple armatures
                        for mod in ob.modifiers:
                            if type(mod) == bpy.types.ArmatureModifier:
                                # ignore empty modifiers
                                if mod.object != None:
                                    armature_name = mod.object.name
                                    # merge vertex weights if the vertex group is in block list
                                    block = (armature_name, group_name)
                                    if block in block_dictionary:
                                        merged = False
                                        # linear search in current vertex's weight list
                                        for item in temp_list:
                                            # vertex weight already exists
                                            if block_dictionary[block][0] == item[0] and block_dictionary[block][1] == item[1]:
                                                item[2] += group_weight
                                                merged = True
                                                break
                                        # vertex weight not exists
                                        if not merged:
                                            temp_list.append([block_dictionary[block][0], block_dictionary[block][1], group_weight])
                                    elif armature_name in bone_dictionary:
                                        temp_armature_key = bone_dictionary[armature_name][0]
                                        if group_name in bone_dictionary[armature_name][1]:
                                            armature_key = temp_armature_key
                                            bone_key = bone_dictionary[armature_name][1][group_name]
                        # vertex has weight
                        if armature_key != None and bone_key != None:
                            merged = False
                            # linear search in current vertex's weight list
                            for item in temp_list:
                                # vertex weight already exists
                                if armature_key == item[0] and bone_key == item[1]:
                                    item[2] += group_weight
                                    merged = True
                                    break
                            # vertex weight not exists
                            if not merged:
                                temp_list.append([armature_key, bone_key, group_weight])
                    # save to weight dic
                    weight_dic[index][i] = []
                    for item in temp_list:
                        weight_dic[index][i].append([item[1], item[2]])
        exist_object_dic[keyword] = index
    return index


def make_polygon_dic(polygon_dic, ob, exist_object_dic):
    if ob.data.polygons in exist_object_dic:
        return exist_object_dic[ob.data.polygons]
    index = len(polygon_dic)
    length = len(ob.data.polygons)
    polygon_dic[index] = [None] * length
    for (i, polygon) in enumerate(ob.data.polygons):
        polygon_dic[index][i] = [ob.data.loops[loop_index].vertex_index for loop_index in polygon.loop_indices]
    exist_object_dic[ob.data.polygons] = (ob.name, index)
    return (ob.name, index)


def make_uv_dic(uv_dic, ob, exist_object_dic):
    keyword = ('UV', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        name_index_pairs = exist_object_dic[keyword]
    else:
        # make uv dic
        name_index_pairs = []
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        for layer in bm.loops.layers.uv.values():
            index = len(uv_dic)
            length = len(ob.data.polygons)
            uv_dic[index] = [None] * length
            for (i, face) in enumerate(bm.faces):
                uv_dic[index][i] = [(loop[layer].uv[0], loop[layer].uv[1]) for loop in face.loops]
            name_index_pairs.append((layer.name, index))
        bm.free  # free and prevent further access
        exist_object_dic[keyword] = name_index_pairs
    return name_index_pairs


def make_tangent_dic(tangent_dic, ob, exist_object_dic):
    keyword = ('Tangent', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        name_index_pairs = exist_object_dic[keyword]
    else:
        # make tangent dic
        name_index_pairs = []
        # we have to store all the layer names to a list due to a blender bug, after having called calc_tangents(), the next uv layer name might point to an empty string, thus blender thows an error message.
        uv_layer_names = [uvlayer.name for uvlayer in ob.data.uv_layers]
        for i in range(len(uv_layer_names)):
            layer_name = uv_layer_names[i]
            ob.data.calc_tangents(uvmap=layer_name)
            index = len(tangent_dic)
            length = len(ob.data.polygons)
            tangent_dic[index] = [None] * length
            for (i, polygon) in enumerate(ob.data.polygons):
                tangent_dic[index][i] = [tuple(ob.data.loops[loop_index].tangent)+tuple(ob.data.loops[loop_index].bitangent) for loop_index in polygon.loop_indices]
            name_index_pairs.append((layer_name, index))
            ob.data.free_tangents()
        exist_object_dic[keyword] = name_index_pairs
    return name_index_pairs


def make_normal_dic(normal_dic, ob, exist_object_dic):
    keyword = ('Normal', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        return exist_object_dic[keyword]
    index = len(normal_dic)
    length = len(ob.data.polygons)
    normal_dic[index] = [None] * length
    if bpy.app.version < (4, 1):
        # generate polygon loop normals
        ob.data.calc_normals_split()
    for (i, polygon) in enumerate(ob.data.polygons):
        if bpy.app.version < (4, 1):
            normal_dic[index][i] = [tuple(ob.data.loops[loop_index].normal) for loop_index in polygon.loop_indices]
        else:
            normal_dic[index][i] = [tuple(ob.data.corner_normals[loop_index].vector) for loop_index in polygon.loop_indices]
    if bpy.app.version < (4, 1):
        # free polygon loop normals
        ob.data.free_normals_split()
    exist_object_dic[keyword] = index
    return index


def make_polygon_material_dic(polygon_material_dic, ob, exist_object_dic):
    keyword = ('PolygonMaterial', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        return exist_object_dic[keyword]
    index = len(polygon_material_dic)
    length = len(ob.data.polygons)
    polygon_material_dic[index] = [None] * length
    for (i, polygon) in enumerate(ob.data.polygons):
        polygon_material_dic[index][i] = polygon.material_index
    exist_object_dic[keyword] = index
    return index


def make_color_dic(color_dic, ob, exist_object_dic):
    keyword = ('Color', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        name_index_pairs = exist_object_dic[keyword]
    else:
        # make uv dic
        name_index_pairs = []
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        for layer in bm.loops.layers.color.values():
            index = len(color_dic)
            length = len(ob.data.polygons)
            color_dic[index] = [None] * length
            for (i, face) in enumerate(bm.faces):
                color_dic[index][i] = [(loop[layer][0], loop[layer][1], loop[layer][2], loop[layer][3]) for loop in face.loops]
            name_index_pairs.append((layer.name, index))
        bm.free  # free and prevent further access
        exist_object_dic[keyword] = name_index_pairs
    return name_index_pairs


def make_node(node_dic, key, key2, name, index):
    if key not in node_dic:
        node_dic[key] = {}
    if key2 not in node_dic[key]:
        node_dic[key][key2] = []
    node_dic[key][key2].append([name, index])



def guess_texture_type(material, texture_file_name):
    texture_type = -1
    if bpy.context.scene.render.engine == 'CYCLES' or bpy.context.scene.render.engine == 'BLENDER_EEVEE':
        # material use node
        if material.use_nodes == True:
            if material.node_tree != None:
                for node in material.node_tree.nodes:
                    if node.bl_idname == 'ShaderNodeTexImage':
                        if node.image != None:
                            if node.image.filepath_from_user() == texture_file_name:
                                current_node = node
                                while current_node.outputs != None and len(current_node.outputs) > 0 and current_node.outputs[0].is_linked:
                                    to_node = current_node.outputs[0].links[0].to_node
                                    to_socket = current_node.outputs[0].links[0].to_socket
                                    if (to_node.bl_idname == 'ShaderNodeMixRGB' or to_node.bl_idname == 'ShaderNodeMix') and (to_socket.name == 'Color1' or to_socket.name == 'A'):
                                        texture_type = 0
                                        break
                                    elif to_node.bl_idname == 'ShaderNodeBsdfDiffuse' or to_node.bl_idname == 'ShaderNodeBsdfPrincipled':
                                        if to_socket.name == 'Color' or to_socket.name == 'Base Color':
                                            texture_type = 0
                                        if to_socket.name == 'Metallic':
                                            texture_type = 1
                                        if to_socket.name == 'Specular' or to_socket.name == 'Specular IOR Level':
                                            texture_type = 2
                                        if to_socket.name == 'Roughness':
                                            texture_type = 3
                                        if to_socket.name == 'Emission' or to_socket.name == 'Emission Color':
                                            texture_type = 4
                                        if to_socket.name == 'Alpha':
                                            texture_type = 5
                                        break
                                    elif to_node.bl_idname == 'ShaderNodeNormalMap' and to_socket.name == 'Color':
                                        texture_type = 6
                                        break
                                    elif to_node.bl_idname == 'ShaderNodeBump':
                                        texture_type = 7
                                        break
                                    elif to_node.bl_idname == 'ShaderNodeDisplacement':
                                        texture_type = 8
                                        break
                                    elif to_node.bl_idname == 'ShaderNodeOutputMaterial' and to_socket.name == 'Displacement':
                                        texture_type = 8
                                        break
                                    elif (to_node.bl_idname == 'ShaderNodeMixRGB' or to_node.bl_idname == 'ShaderNodeMix') and (to_socket.name == 'Color2' or to_socket.name == 'B'):
                                        texture_type = 9
                                        break
                                    else:
                                        current_node = to_node

    return texture_type


def make_material_dic(material_dic, texture_dic, ob, texture_map, material_map, custom_property_dic, use_embed_media, use_copy_texture, subdirname, packed_texture_filenames, exist_object_dic):
    for slot in ob.material_slots:
        material = slot.material
        # ignore empty materials
        if material != None:
            if material not in material_map:
                material_name = material.name.replace(",", "\\;")
                diffuse_color = [material.diffuse_color[0], material.diffuse_color[1], material.diffuse_color[2]]
                specular_color = [material.specular_color[0], material.specular_color[1], material.specular_color[2]]
                emissive_color = [0.0, 0.0, 0.0]
                metallic = material.metallic
                specular = material.specular_intensity
                roughness = material.roughness
                texture_filenames = set()
                packed_texture_map = {}
                texture_uv_maps = {}
                if bpy.context.scene.render.engine == 'CYCLES' or bpy.context.scene.render.engine == 'BLENDER_EEVEE':
                    # material use node
                    if material.use_nodes == True:
                        if material.node_tree != None:
                            for node in material.node_tree.nodes:
                                # override diffuse color
                                if node.bl_idname == 'ShaderNodeBsdfPrincipled':
                                    diffuse_color[0] = node.inputs['Base Color'].default_value[0]
                                    diffuse_color[1] = node.inputs['Base Color'].default_value[1]
                                    diffuse_color[2] = node.inputs['Base Color'].default_value[2]

                                    if bpy.app.version < (4, 0):
                                        emissive_color[0] = node.inputs['Emission'].default_value[0]
                                        emissive_color[1] = node.inputs['Emission'].default_value[1]
                                        emissive_color[2] = node.inputs['Emission'].default_value[2]
                                    else:
                                        emissive_color[0] = node.inputs['Emission Color'].default_value[0]
                                        emissive_color[1] = node.inputs['Emission Color'].default_value[1]
                                        emissive_color[2] = node.inputs['Emission Color'].default_value[2]

                                    metallic = node.inputs['Metallic'].default_value
                                    if bpy.app.version < (4, 0):
                                        specular = node.inputs['Specular'].default_value
                                    else:
                                        specular = node.inputs['Specular IOR Level'].default_value
                                    roughness = node.inputs['Roughness'].default_value
                                if node.bl_idname == 'ShaderNodeTexImage':
                                    if node.image != None and node.image.source != 'GENERATED':
                                        (base, ext) = os.path.splitext(node.image.filepath_from_user())
                                        if ext != '':
                                            # deal with packed image
                                            if node.image.packed_file != None:
                                                unpacked_texture_filename = os.path.join(os.path.dirname(__file__), "data", os.path.basename(node.image.filepath_from_user()))
                                                # Blender supports UDIM texture since v2.82, UDIM texture filename usually contains "1001."
                                                partition = unpacked_texture_filename.partition("1001.")
                                                using_udim_image = (partition[1] == "1001.") and node.image.source == 'TILED'
                                                original_raw_path = node.image.filepath_raw
                                                node.image.filepath_raw = unpacked_texture_filename if not using_udim_image else unpacked_texture_filename.replace("1001.", "<UDIM>.")
                                                node.image.save()
                                                node.image.filepath_raw = original_raw_path
                                                packed_texture_filenames.append(unpacked_texture_filename)
                                                packed_texture_map[node.image.filepath_from_user()] = unpacked_texture_filename
                                                if using_udim_image:
                                                    for tile in node.image.tiles:
                                                        if tile.number != 1001:
                                                            packed_texture_filenames.append(unpacked_texture_filename.replace("1001.", "{}.".format(tile.number)))
                                            else:
                                                # Blender supports UDIM texture since v2.82, UDIM texture filename usually contains "1001."
                                                partition = node.image.filepath_from_user().partition("1001.")
                                                using_udim_image = (partition[1] == "1001.") and node.image.source == 'TILED'
                                                packed_texture_filenames.append(node.image.filepath_from_user())
                                                packed_texture_map[node.image.filepath_from_user()] = node.image.filepath_from_user()
                                                if using_udim_image:
                                                    for tile in node.image.tiles:
                                                        if tile.number != 1001:
                                                            packed_texture_filenames.append(node.image.filepath_from_user().replace("1001.", "{}.".format(tile.number)))
                                            texture_uv_maps[node.image.filepath_from_user()] = 'default'
                                            if node.inputs['Vector'].is_linked:
                                                from_node = node.inputs['Vector'].links[0].from_node
                                                if from_node.bl_idname == 'ShaderNodeUVMap':
                                                    if from_node.uv_map != '':
                                                        texture_uv_maps[node.image.filepath_from_user()] = from_node.uv_map
                                            else:
                                                if len(ob.data.uv_layers) > 0:
                                                    for uv_layer in ob.data.uv_layers:
                                                        if uv_layer.active_render:
                                                            texture_uv_maps[node.image.filepath_from_user()] = uv_layer.name
                                            texture_filenames.add(node.image.filepath_from_user())
                # add all slot textures
                for texture_file_name in texture_filenames:
                    if texture_file_name not in texture_map:
                        index = len(texture_dic)
                        texture_dic[index] = (packed_texture_map[texture_file_name], texture_uv_maps[texture_file_name])
                        # fix path if copy textures
                        if not use_embed_media and use_copy_texture:
                            texture_dic[index] = (os.path.join(subdirname, os.path.basename(texture_dic[index][0])), texture_uv_maps[texture_file_name])
                        # save for later use
                        texture_map[texture_file_name] = index

                texture_index_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                # guess texture types
                for texture_file_name in texture_filenames:
                    texture_type = guess_texture_type(material, texture_file_name)
                    if texture_type != -1:
                        texture_index_list[texture_type] = texture_map[texture_file_name]
                index = len(material_dic)
                custom_property_index = make_custom_property_dic(custom_property_dic, material, exist_object_dic)
                material_dic[index] = (material_name, diffuse_color[0], diffuse_color[1], diffuse_color[2], texture_index_list[0], -1.0, -1.0, -1.0, texture_index_list[1], specular_color[0], specular_color[1], specular_color[2], texture_index_list[2], -1.0, -1.0, -1.0, texture_index_list[3], emissive_color[0], emissive_color[1], emissive_color[2], texture_index_list[4], -1.0, -1.0, -1.0, texture_index_list[5], -1.0, -1.0, -1.0, texture_index_list[6], -1.0, -1.0, -1.0, texture_index_list[7], -1.0, -1.0, -1.0, texture_index_list[8], -1.0, -1.0, -1.0, texture_index_list[9], metallic, specular, roughness, custom_property_index if custom_property_index != None else -1)
                # save for later use
                material_map[material] = index


def make_mesh_material_dic(mesh_material_dic, ob, exist_object_dic, material_map):
    keyword = ('MeshMaterial', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        temp_list = []
        for slot in ob.material_slots:
            material = slot.material
            # ignore empty materials
            if material != None:
                if material in material_map:
                    temp_list.append(material_map[material])
        if len(temp_list) == 0:
            return None
        index = len(mesh_material_dic)
        mesh_material_dic[index] = temp_list
        exist_object_dic[keyword] = index
    return index


def make_edge_crease_dic(edge_crease_dic, ob, exist_object_dic, my_edge_crease_scale):
    if bpy.app.version < (3, 4):
        if not ob.data.use_customdata_edge_crease:
            return None
    elif bpy.app.version >= (4, 0):
        if not ob.data.edge_creases:
            return None
    else:
        if not ob.data.has_crease_edge:
            return None

    keyword = ('EdgeCrease', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        temp_list = []
        if bpy.app.version < (4, 0):
            for edge in ob.data.edges:
                if edge.crease != 0.0:
                    temp_list.append([edge.vertices[0], edge.vertices[1], edge.crease * my_edge_crease_scale])
        else:
            for (i, edge) in enumerate(ob.data.edges):
                edge_crease = ob.data.edge_creases.data[i].value
                if edge_crease != 0.0:
                    temp_list.append([edge.vertices[0], edge.vertices[1], edge_crease * my_edge_crease_scale])
        if len(temp_list) == 0:
            return None
        index = len(edge_crease_dic)
        edge_crease_dic[index] = temp_list
        exist_object_dic[keyword] = index
    return index


def make_edge_smoothing_dic(edge_smoothing_dic, ob, exist_object_dic):
    keyword = ('EdgeSmoothing', ob.data.vertices, ob.data.polygons)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        temp_list = []
        for edge in ob.data.edges:
            if edge.use_edge_sharp:
                temp_list.append([edge.vertices[0], edge.vertices[1]])
        if len(temp_list) == 0:
            return None
        index = len(edge_smoothing_dic)
        edge_smoothing_dic[index] = temp_list
        exist_object_dic[keyword] = index
    return index


def make_ik_dic(hierarchy_dic, ik_dic, ob, exist_object_dic):
    keyword = ('IK', ob)
    if keyword in exist_object_dic:
        index = exist_object_dic[keyword]
    else:
        # make ik dic
        index = len(ik_dic)
        ik_found = False
        for constraint in ob.constraints:
            if constraint.type == 'IK':
                target_key = get_hierarchy_key_from_empty_name(hierarchy_dic, constraint.target.name) if constraint.target != None and constraint.target.type == 'EMPTY' else "-1"
                ik_dic[index] = [constraint.name.replace(",", "\\;"), target_key, constraint.chain_count if not constraint.use_tail else constraint.chain_count-1]
                exist_object_dic[keyword] = index
                ik_found = True
                # ignore multiple ik constraints
                break
        # no ik constraint found
        if not ik_found:
            return None
    return index


# generate {(armature name, bone name): (armature key, bone key)} mapping
# we use the dictionary to get armature key and bone key by armature name and bone name
def make_block_dictionary(hierarchy_dic, bone_dictionary, block_list, use_rigify_armature):
    block_dictionary = {}
    for block in block_list:
        for (key, value) in hierarchy_dic.items():
            if value[0] == 'ARMATURE':
                armature_key = key
                armature_name = value[1]
                # armature matched
                if armature_name == block[0]:
                    ob = value[-1]
                    # search valid deform bone recusively in bone list
                    parent_node = ob.data.bones[block[1]].parent
                    found = False
                    while parent_node != None:
                        parent_name = parent_node.name
                        # fix parent name to match deform bone
                        if use_rigify_armature:
                            if parent_name.startswith("ORG-") or parent_name.startswith("MCH-"):
                                parent_name = "DEF-{}".format(parent_name[4:])
                        for (key2, value2) in hierarchy_dic.items():
                            if value2[0] == 'BONE':
                                tokens = key2.split(".")
                                if len(tokens) == 2 and tokens[0] == armature_key:
                                    bone_key = key2
                                    bone_name = value2[1]
                                    if bone_name == parent_name:
                                        block_dictionary[block] = (armature_key, bone_key)
                                        found = True
                                        break
                        if found == True:
                            break
                        parent_node = parent_node.parent
    return block_dictionary


# generate {armature name: (armature key, {bone name: bone key})} mapping
# we use the dictionary to get armature key and bone key by armature name and bone name
def make_bone_dictionary(hierarchy_dic):
    bone_dictionary = {}
    for (key, value) in hierarchy_dic.items():
        if value[0] == 'ARMATURE':
            armature_key = key
            armature_name = value[1]
            dictionary = {}
            for (key2, value2) in hierarchy_dic.items():
                if value2[0] == 'BONE':
                    tokens = key2.split(".")
                    if len(tokens) == 2 and tokens[0] == armature_key:
                        bone_key = key2
                        bone_name = value2[1]
                        dictionary[bone_name] = bone_key
            bone_dictionary[armature_name] = (armature_key, dictionary)
    return bone_dictionary


def make_generic_node_dic(context, hierarchy_dic, use_only_deform_bones, node_dic, default_pose_dic, bind_pose_dic, vertex_dic, weight_dic, shape_dic, polygon_dic, uv_dic, tangent_dic, normal_dic, color_dic, polygon_material_dic, texture_dic, material_dic, mesh_material_dic, exist_object_dic, use_animation, use_timeline_range, my_animation_offset, my_animation_type, block_list, use_rigify_armature, camera_dic, light_dic, custom_property_dic, edge_crease_dic, use_edge_crease, my_edge_crease_scale, my_edge_smoothing, edge_smoothing_dic, applied_mesh_dic, ik_dic, use_embed_media, use_copy_texture, subdirname, packed_texture_filenames, bone_correction_matrix):
    bone_dictionary = make_bone_dictionary(hierarchy_dic)
    block_dictionary = make_block_dictionary(hierarchy_dic, bone_dictionary, block_list, use_rigify_armature)
    # make material dic in the first pass, for we need it in the second pass
    texture_map = {}
    material_map = {}
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        if value[0] == 'MESH':
            make_material_dic(material_dic, texture_dic, ob, texture_map, material_map, custom_property_dic, use_embed_media, use_copy_texture, subdirname, packed_texture_filenames, exist_object_dic)
    # second pass
    for (key, value) in hierarchy_dic.items():
        ob_parent = value[-2]
        ob = value[-1]
        # add visibility node
        hide_viewport = ob.hide_viewport if hasattr(ob, 'hide_viewport') else False
        make_node(node_dic, key, 'Visibility', '', 0 if hide_viewport else 1)
        index = make_default_pose_dic(default_pose_dic, ob_parent, ob, value[0] == 'BONE', bone_correction_matrix)
        make_node(node_dic, key, 'DefaultPose', '', index)
        index = make_bind_pose_dic(bind_pose_dic, ob_parent, ob, value[0] == 'BONE', bone_correction_matrix)
        make_node(node_dic, key, 'BindPose', '', index)
        if value[0] == 'MESH':
            # make sure the mesh data is valid
            ob.data.validate(clean_customdata=False)
            index = make_vertex_dic(vertex_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'Vertex', '', index)
            index = make_weight_dic(hierarchy_dic, weight_dic, ob, exist_object_dic, bone_dictionary, block_dictionary)
            if index != None:
                make_node(node_dic, key, 'Weight', '', index)
            name_index_pairs = make_shape_dic(shape_dic, ob, exist_object_dic)
            for (shape_name, index) in name_index_pairs:
                make_node(node_dic, key, 'Shape', shape_name, index)
            (mesh_name, index) = make_polygon_dic(polygon_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'Polygon', mesh_name, index)
            name_index_pairs = make_uv_dic(uv_dic, ob, exist_object_dic)
            for (uv_name, index) in name_index_pairs:
                make_node(node_dic, key, 'UV', uv_name, index)
            loop_tatals = [None] * len(ob.data.polygons)
            ob.data.polygons.foreach_get("loop_total", loop_tatals)
            # We only compute tangents for triangles and quads.
            if all((loop_tatal < 5 for loop_tatal in loop_tatals)):
                del loop_tatals
                name_index_pairs = make_tangent_dic(tangent_dic, ob, exist_object_dic)
                for (uv_name, index) in name_index_pairs:
                    make_node(node_dic, key, 'Tangent', uv_name, index)
            index = make_normal_dic(normal_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'Normal', '', index)
            name_index_pairs = make_color_dic(color_dic, ob, exist_object_dic)
            for (color_name, index) in name_index_pairs:
                make_node(node_dic, key, 'Color', color_name, index)
            index = make_polygon_material_dic(polygon_material_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'PolygonMaterial', '', index)
            index = make_mesh_material_dic(mesh_material_dic, ob, exist_object_dic, material_map)
            if index != None:
                make_node(node_dic, key, 'MeshMaterial', '', index)
            if use_edge_crease:
                index = make_edge_crease_dic(edge_crease_dic, ob, exist_object_dic, my_edge_crease_scale)
                if index != None:
                    make_node(node_dic, key, 'EdgeCrease', '', index)
            if my_edge_smoothing == 'Blender':
                index = make_edge_smoothing_dic(edge_smoothing_dic, ob, exist_object_dic)
                if index != None:
                    make_node(node_dic, key, 'EdgeSmoothing', '', index)
        elif value[0] == 'CAMERA':
            index = make_camera_dic(camera_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'Camera', '', index)
        elif value[0] == 'LIGHT':
            index = make_light_dic(light_dic, ob, exist_object_dic)
            make_node(node_dic, key, 'Light', '', index)
        elif value[0] == 'BONE':
            tokens = key.split(".")
            armature_key = tokens[0]
            armature_node = hierarchy_dic[armature_key]
            armature = armature_node[-1]
            bone_name = value[1]
            pose_bone = armature.pose.bones[bone_name]
            if not use_only_deform_bones:
                index = make_ik_dic(hierarchy_dic, ik_dic, pose_bone, exist_object_dic)
                if index != None:
                    make_node(node_dic, key, 'IK', '', index)
        if value[0] != 'ARMATURE':
            index = make_custom_property_dic(custom_property_dic, ob, exist_object_dic)
            if index != None:
                make_node(node_dic, key, 'CustomProperty', '', index)


def get_nla_track_name(context, ob):
    active_tracks = []
    for track in ob.animation_data.nla_tracks:
        if track.mute:
            continue
        active_tracks.append(track.name)
    if len(active_tracks) == 0:
        return "Untitled"
    else:
        return "_".join(active_tracks)


def get_active_nla_track(context, ob):
    active_track = None
    for track in ob.animation_data.nla_tracks:
        if not track.mute:
            active_track = track
            break
    return active_track if active_track != None else ob.animation_data.nla_tracks


def get_nla_frame_range(context, ob):
    frame_start = None
    frame_end = None
    for track in ob.animation_data.nla_tracks:
        if track.mute:
            continue
        for strip in track.strips:
            if strip.mute:
                continue
            if frame_start == None or strip.frame_start < frame_start:
                frame_start = int(strip.frame_start)
            if frame_end == None or strip.frame_end > frame_end:
                frame_end = int(strip.frame_end)
    if frame_start == None:
        frame_start = context.scene.frame_start
    if frame_end == None:
        frame_end = context.scene.frame_end
    return (frame_start, frame_end)


def get_shape_key_nla_track_name(context, ob):
    active_tracks = []
    for track in ob.data.shape_keys.animation_data.nla_tracks:
        if track.mute:
            continue
        active_tracks.append(track.name)
    if len(active_tracks) == 0:
        return "Untitled"
    else:
        return "_".join(active_tracks)


def get_active_shape_key_nla_track(context, ob):
    active_track = None
    for track in ob.data.shape_keys.animation_data.nla_tracks:
        if not track.mute:
            active_track = track
            break
    return active_track if active_track != None else ob.data.shape_keys.animation_data.nla_tracks


def get_shape_key_nla_frame_range(context, ob):
    frame_start = None
    frame_end = None
    for track in ob.data.shape_keys.animation_data.nla_tracks:
        if track.mute:
            continue
        for strip in track.strips:
            if strip.mute:
                continue
            if frame_start == None or strip.frame_start < frame_start:
                frame_start = int(strip.frame_start)
            if frame_end == None or strip.frame_end > frame_end:
                frame_end = int(strip.frame_end)
    if frame_start == None:
        frame_start = context.scene.frame_start
    if frame_end == None:
        frame_end = context.scene.frame_end
    return (frame_start, frame_end)


def get_camera_nla_track_name(context, ob):
    active_tracks = []
    for track in ob.data.animation_data.nla_tracks:
        if track.mute:
            continue
        active_tracks.append(track.name)
    if len(active_tracks) == 0:
        return "Untitled"
    else:
        return "_".join(active_tracks)


def get_active_camera_nla_track(context, ob):
    active_track = None
    for track in ob.data.animation_data.nla_tracks:
        if not track.mute:
            active_track = track
            break
    return active_track if active_track != None else ob.data.animation_data.nla_tracks


def get_camera_nla_frame_range(context, ob):
    frame_start = None
    frame_end = None
    for track in ob.data.animation_data.nla_tracks:
        if track.mute:
            continue
        for strip in track.strips:
            if strip.mute:
                continue
            if frame_start == None or strip.frame_start < frame_start:
                frame_start = int(strip.frame_start)
            if frame_end == None or strip.frame_end > frame_end:
                frame_end = int(strip.frame_end)
    if frame_start == None:
        frame_start = context.scene.frame_start
    if frame_end == None:
        frame_end = context.scene.frame_end
    return (frame_start, frame_end)


def make_pose_key_dic(context, node_dic, key, pose_key_dic, ob_parent, ob, frame_count, frame, frame_index, my_animation_type, my_animation_offset, is_bone, bone_correction_matrix):
    if frame == 0:
        index = len(pose_key_dic)
        if ob_parent == None:
            if my_animation_type == 'Actions':
                action_name = ob.animation_data.action.name
            elif my_animation_type == 'Tracks':
                action_name = get_nla_track_name(context, ob)
            else:
                action_name = ob.animation_data.action.name if not (ob.animation_data.action == None and ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0) else get_nla_track_name(context, ob)
        else:
            if my_animation_type == 'Actions':
                action_name = ob_parent.animation_data.action.name
            elif my_animation_type == 'Tracks':
                action_name = get_nla_track_name(context, ob_parent)
            else:
                action_name = ob_parent.animation_data.action.name if not (ob_parent.animation_data.action == None and ob_parent.animation_data.use_nla and len(ob_parent.animation_data.nla_tracks) > 0) else get_nla_track_name(context, ob_parent)
        pose_key_dic[index] = [None] * frame_count
        make_node(node_dic, key, 'PoseKey', action_name, index)
    else:
        index = node_dic[key]['PoseKey'][-1][1]
    pose_key = (ob.matrix_world if ob.type not in ['CAMERA', 'LIGHT'] else ob.matrix_world @ mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y' if ob.type == 'CAMERA' else 'X')) if ob_parent == None else ob_parent.matrix_world @ ob_parent.pose.bones[ob.name].matrix
    # user defined axis
    if is_bone and bone_correction_matrix != None:
        pose_key = pose_key @ bone_correction_matrix
    temp_list = [frame_index + my_animation_offset, []]
    for row in pose_key.transposed():
        for item in row:
            temp_list[1].append(item)
    pose_key_dic[index][frame] = temp_list


def get_pose_key_range(context, hierarchy_dic, my_animation_type):
    min_action_start = None
    max_action_end = None
    for (key, value) in hierarchy_dic.items():
        ob_type = value[0]
        if ob_type != 'BONE':
            ob = value[-1]
            if my_animation_type == 'Actions':
                if ob.animation_data != None and ob.animation_data.action != None:
                    (action_start, action_end) = [int(x) for x in ob.animation_data.action.frame_range]
                    if min_action_start == None or action_start < min_action_start:
                        min_action_start = action_start
                    if max_action_end == None or action_end > max_action_end:
                        max_action_end = action_end
            elif my_animation_type == 'Tracks':
                if ob.animation_data != None and ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0:
                    (action_start, action_end) = get_nla_frame_range(context, ob)
                    if min_action_start == None or action_start < min_action_start:
                        min_action_start = action_start
                    if max_action_end == None or action_end > max_action_end:
                        max_action_end = action_end
            else:
                if ob.animation_data != None and ((ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0) or ob.animation_data.action != None):
                    (action_start, action_end) = [int(x) for x in ob.animation_data.action.frame_range] if not (ob.animation_data.action == None and ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0) else get_nla_frame_range(context, ob)
                    if min_action_start == None or action_start < min_action_start:
                        min_action_start = action_start
                    if max_action_end == None or action_end > max_action_end:
                        max_action_end = action_end
    return (min_action_start, max_action_end)


def make_pose_key_node_dic(context, hierarchy_dic, node_dic, pose_key_dic, my_animation_type, use_timeline_range, my_animation_offset, desired_object, bone_correction_matrix):
    (action_start, action_end) = get_pose_key_range(context, hierarchy_dic, my_animation_type)
    if use_timeline_range:
        (action_start, action_end) = (max(action_start, context.scene.frame_start), min(action_end, context.scene.frame_end))
    # exists any pose key
    if action_start != None and action_end != None:
        for frame in range(action_start, action_end + 1):
            # set frame
            context.scene.frame_set(frame)
            bpy.context.view_layer.update()
            for (key, value) in hierarchy_dic.items():
                ob_parent = value[-2]
                ob = value[-1]
                # ignore not desired object for NLA tracks
                if desired_object != None:
                    if value[0] == 'BONE':
                        if desired_object != ob_parent:
                            continue
                    else:
                        if ob != desired_object:
                            continue
                node_type = value[0]
                if ob_parent == None:
                    # object has animation
                    if ob.animation_data != None and ((ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0) or ob.animation_data.action != None):
                        make_pose_key_dic(context, node_dic, key, pose_key_dic, ob_parent, ob, action_end + 1 - action_start, frame - action_start, frame, my_animation_type, my_animation_offset, node_type == 'BONE', bone_correction_matrix)
                else:
                    # object has animation
                    if ob_parent.animation_data != None and ((ob_parent.animation_data.use_nla and len(ob_parent.animation_data.nla_tracks) > 0) or ob_parent.animation_data.action != None):
                        make_pose_key_dic(context, node_dic, key, pose_key_dic, ob_parent, ob, action_end + 1 - action_start, frame - action_start, frame, my_animation_type, my_animation_offset, node_type == 'BONE', bone_correction_matrix)


# Unity will eat the armature node when the skinned meshes are the children of the armature nodes, to preserve the armature node, we need to move the skinned meshes out of the armature node.
def fix_compatibility_for_unity(hierarchy_dic):
    for (key, value) in hierarchy_dic.items():
        node_type = value[0]
        if node_type == 'ARMATURE':
            parent_key = value[2]
            for (key2, value2) in hierarchy_dic.items():
                node_type2 = value2[0]
                if node_type2 == 'MESH':
                    parent_key2 = value2[2]
                    if parent_key2 == key:
                        value2[2] = parent_key


def make_applied_mesh_dic(context, hierarchy_dic, origin_object_dic, applied_mesh_dic, use_include_armature_deform_modifier):
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        if value[0] != 'BONE' and ob.type == 'MESH':
            # ignore mesh with shape keys
            if ob.data.shape_keys != None:
                continue
            # ignore mesh without modifiers
            if len(ob.modifiers) == 0:
                continue
            armature_modifier_count = 0
            other_modifier_count = 0
            for mod in ob.modifiers:
                if type(mod) == bpy.types.ArmatureModifier:
                    # ignore empty modifiers
                    if mod.object != None:
                        armature_modifier_count += 1
                else:
                    other_modifier_count += 1
            # ignore mesh without other modifiers when not applying armature modifier
            if not use_include_armature_deform_modifier:
                if other_modifier_count == 0:
                    continue
            # ignore mesh with empty armature modifier and no other modifiers
            if armature_modifier_count + other_modifier_count == 0:
                continue
            origin_mesh = ob.data
            if origin_mesh in applied_mesh_dic:
                applied_mesh = applied_mesh_dic[origin_mesh]
            else:
                depsgraph = context.evaluated_depsgraph_get()
                ob_eval = ob.evaluated_get(depsgraph)
                # create an applied mesh from the current modifiers state.
                applied_mesh = bpy.data.meshes.new_from_object(ob_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
                # save applied mesh
                applied_mesh_dic[origin_mesh] = applied_mesh
            # save original mesh
            origin_object_dic[ob] = origin_mesh
            # replace original mesh
            ob.data = applied_mesh

def remove_applied_mesh_dic(origin_object_dic, applied_mesh_dic):
    # restore original meshes
    for (ob, origin_mesh) in origin_object_dic.items():
        ob.data = origin_mesh
    # remove applied meshes from data pool
    for applied_mesh in applied_mesh_dic.values():
        bpy.data.meshes.remove(applied_mesh)

def make_all_vertex_animations(context, hierarchy_dic, node_dic, vertex_animation_dic, use_vertex_format, use_vertex_space, use_timeline_range, my_animation_offset, my_vertex_frame_start, my_vertex_frame_end, exist_object_dic):
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        if value[0] == 'MESH':
                index = make_vertex_animation_dic(context, vertex_animation_dic, ob, exist_object_dic, use_vertex_space, use_timeline_range, my_animation_offset, my_vertex_frame_start, my_vertex_frame_end)
                make_node(node_dic, key, 'VertexPoseKey', '', index)
                make_node(node_dic, key, 'VertexFormat', use_vertex_format, -1)
                make_node(node_dic, key, 'VertexSpace', use_vertex_space, -1)

def make_all_actions(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic):
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        for action in bpy.data.actions:
            # transform actions
            if value[0] != 'BONE' and ob.animation_data != None:
                # ignore shape key actions, the id_root of shape key is 'KEY'
                if action.id_root == 'OBJECT':
                    save_action = ob.animation_data.action
                    ob.animation_data.action = action
                    make_pose_key_node_dic(context, hierarchy_dic, node_dic, pose_key_dic, my_animation_type, use_timeline_range, my_animation_offset, None, bone_correction_matrix)
                    if use_driver_based_shape_key:
                        if ob.type == 'ARMATURE':
                            for (key2, value2) in hierarchy_dic.items():
                                ob2 = value2[-1]
                                if value2[0] == 'MESH':
                                    if ob2.data.shape_keys != None:
                                        if ob2.data.shape_keys.animation_data != None:
                                            shape_key_data = (ob2.data.shape_keys.animation_data, ob.animation_data.action)
                                            (action_name, index) = make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob2, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                                            if action_name != None and index != None:
                                                make_node(node_dic, key2, 'ShapeKey', action_name, index)
                    ob.animation_data.action = save_action
            # shape key actions
            if value[0] == 'MESH':
                if ob.data.shape_keys != None:
                    if ob.data.shape_keys.animation_data != None:
                        # only deal with shape key actions, the id_root of shape key is 'KEY'
                        if action.id_root == 'KEY':
                            save_action = ob.data.shape_keys.animation_data.action
                            ob.data.shape_keys.animation_data.action = action
                            shape_key_data = ob.data.shape_keys.animation_data.action
                            (action_name, index) = make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                            ob.data.shape_keys.animation_data.action = save_action
                            if action_name != None and index != None:
                                make_node(node_dic, key, 'ShapeKey', action_name, index)
            # camera actions
            elif value[0] == 'CAMERA':
                if ob.data.animation_data != None:
                    # only deal with camera actions, the id_root of shape key is 'CAMERA'
                    if action.id_root == 'CAMERA':
                        save_action = ob.data.animation_data.action
                        ob.data.animation_data.action = action
                        (action_name, index) = make_camera_key_dic(context, hierarchy_dic, camera_key_dic, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                        ob.data.animation_data.action = save_action
                        if action_name != None and index != None:
                            make_node(node_dic, key, 'CameraKey', action_name, index)

def make_all_nla_tracks(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic):
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        if value[0] != 'BONE' and ob.animation_data != None:
            if ob.animation_data.use_nla and len(ob.animation_data.nla_tracks) > 0:
                save_mutes = [False] * len(ob.animation_data.nla_tracks)
                ob.animation_data.nla_tracks.foreach_get('mute', save_mutes)
                all_mutes = [True] * len(ob.animation_data.nla_tracks)
                for i in range(len(ob.animation_data.nla_tracks)):
                    ob.animation_data.nla_tracks.foreach_set('mute', all_mutes)
                    ob.animation_data.nla_tracks[i].mute = False
                    make_pose_key_node_dic(context, hierarchy_dic, node_dic, pose_key_dic, my_animation_type, use_timeline_range, my_animation_offset, ob, bone_correction_matrix)
                    if use_driver_based_shape_key:
                        if ob.type == 'ARMATURE':
                            for (key2, value2) in hierarchy_dic.items():
                                ob2 = value2[-1]
                                if value2[0] == 'MESH':
                                    if ob2.data.shape_keys != None:
                                        if ob2.data.shape_keys.animation_data != None:
                                            shape_key_data = (ob2.data.shape_keys.animation_data, ob.animation_data.nla_tracks[i])
                                            (action_name, index) = make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob2, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                                            if action_name != None and index != None:
                                                make_node(node_dic, key2, 'ShapeKey', action_name, index)
                ob.animation_data.nla_tracks.foreach_set('mute', save_mutes)
        # shape key nla tracks
        if value[0] == 'MESH':
            if ob.data.shape_keys != None:
                if ob.data.shape_keys.animation_data != None:
                    if ob.data.shape_keys.animation_data.use_nla and len(ob.data.shape_keys.animation_data.nla_tracks) > 0:
                        save_mutes = [False] * len(ob.data.shape_keys.animation_data.nla_tracks)
                        ob.data.shape_keys.animation_data.nla_tracks.foreach_get('mute', save_mutes)
                        all_mutes = [True] * len(ob.data.shape_keys.animation_data.nla_tracks)
                        for i in range(len(ob.data.shape_keys.animation_data.nla_tracks)):
                            ob.data.shape_keys.animation_data.nla_tracks.foreach_set('mute', all_mutes)
                            ob.data.shape_keys.animation_data.nla_tracks[i].mute = False
                            shape_key_data = ob.data.shape_keys.animation_data.nla_tracks[i]
                            (action_name, index) = make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                            if action_name != None and index != None:
                                make_node(node_dic, key, 'ShapeKey', action_name, index)
                        ob.data.shape_keys.animation_data.nla_tracks.foreach_set('mute', save_mutes)
        # camera nla tracks
        elif value[0] == 'CAMERA':
            if ob.data.animation_data != None:
                if ob.data.animation_data.use_nla and len(ob.data.animation_data.nla_tracks) > 0:
                    save_mutes = [False] * len(ob.data.animation_data.nla_tracks)
                    ob.data.animation_data.nla_tracks.foreach_get('mute', save_mutes)
                    all_mutes = [True] * len(ob.data.animation_data.nla_tracks)
                    for i in range(len(ob.data.animation_data.nla_tracks)):
                        ob.data.animation_data.nla_tracks.foreach_set('mute', all_mutes)
                        ob.data.animation_data.nla_tracks[i].mute = False
                        (action_name, index) = make_camera_key_dic(context, hierarchy_dic, camera_key_dic, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                        if action_name != None and index != None:
                            make_node(node_dic, key, 'CameraKey', action_name, index)
                    ob.data.animation_data.nla_tracks.foreach_set('mute', save_mutes)

def make_active_action_or_nla_tracks(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic):
    # transform actions
    make_pose_key_node_dic(context, hierarchy_dic, node_dic, pose_key_dic, my_animation_type, use_timeline_range, my_animation_offset, None, bone_correction_matrix)
    for (key, value) in hierarchy_dic.items():
        ob = value[-1]
        # shape key actions
        if value[0] == 'MESH':
            if ob.data.shape_keys != None:
                if ob.data.shape_keys.animation_data != None:
                    shape_key_data = ob.data.shape_keys.animation_data
                    (action_name, index) = make_shape_key_dic(context, hierarchy_dic, shape_key_dic, use_driver_based_shape_key, shape_key_data, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                    if action_name != None and index != None:
                        make_node(node_dic, key, 'ShapeKey', action_name, index)
        # camera actions
        elif value[0] == 'CAMERA':
            if ob.data.animation_data != None:
                (action_name, index) = make_camera_key_dic(context, hierarchy_dic, camera_key_dic, ob, use_timeline_range, my_animation_offset, my_animation_type, exist_object_dic)
                if action_name != None and index != None:
                    make_node(node_dic, key, 'CameraKey', action_name, index)

def concatenate_all(node_dic, pose_key_dic, shape_key_dic):
    for (key, value) in node_dic.items():
        for (key2, value2) in value.items():
            if key2 == 'PoseKey':
                if len(value2) > 1:
                    concatenate_index = len(pose_key_dic)
                    pose_key_dic[concatenate_index] = []
                    frame_offset = 0
                    for item in value2:
                        to_concatenate_index = item[1]
                        for pose_key in pose_key_dic[to_concatenate_index]:
                            pose_key_dic[concatenate_index].append([frame_offset + pose_key[0] - pose_key_dic[to_concatenate_index][0][0] + 1, pose_key[1]])
                        frame_offset += pose_key_dic[to_concatenate_index][-1][0] - pose_key_dic[to_concatenate_index][0][0] + 1
                    # clear all actions
                    node_dic[key][key2] = []
                    # add the concatenated action
                    make_node(node_dic, key, 'PoseKey', "Concatenated PoseKey Action", concatenate_index)
            elif key2 == 'ShapeKey':
                if len(value2) > 1:
                    concatenate_index = len(shape_key_dic)
                    shape_key_dic[concatenate_index] = []
                    frame_offset = 0
                    for item in value2:
                        to_concatenate_index = item[1]
                        for shape_key in shape_key_dic[to_concatenate_index]:
                            shape_key_dic[concatenate_index].append([])
                            shape_key_dic[concatenate_index][-1].append(frame_offset + shape_key[0] - shape_key_dic[to_concatenate_index][0][0] + 1)
                            shape_key_dic[concatenate_index][-1].extend(shape_key[1:])
                        frame_offset += shape_key_dic[to_concatenate_index][-1][0] - shape_key_dic[to_concatenate_index][0][0] + 1
                    # clear all actions
                    node_dic[key][key2] = []
                    # add the concatenated action
                    make_node(node_dic, key, 'ShapeKey', "Concatenated ShapeKey Action", concatenate_index)

def write_some_data(context, filepath, context_objects, use_animation, use_timeline_range, my_animation_offset, use_driver_based_shape_key, my_animation_type, use_only_deform_bones, use_rigify_armature, use_rigify_root_bone, use_only_selected_deform_bones, my_max_bone_influences, primary_bone_axis, secondary_bone_axis, use_vertex_animation, use_vertex_format, use_vertex_space, my_vertex_frame_start, my_vertex_frame_end, use_edge_crease, my_edge_crease_scale, my_edge_smoothing, use_apply_modifiers, use_include_armature_deform_modifier, use_concatenate_all, use_embed_media, use_copy_texture, subdirname, packed_texture_filenames):
    print("running write_some_data...")
    print("="*30)
    hierarchy_dic = {}
    default_pose_dic = {}
    bind_pose_dic = {}
    pose_key_dic = {}
    node_dic = {}
    vertex_dic = {}
    weight_dic = {}
    shape_dic = {}
    shape_key_dic = {}
    polygon_dic = {}
    uv_dic = {}
    tangent_dic = {}
    normal_dic = {}
    color_dic = {}
    polygon_material_dic = {}
    texture_dic = {}
    material_dic = {}
    mesh_material_dic = {}
    exist_object_dic = {}
    block_list = []
    camera_dic = {}
    light_dic = {}
    vertex_animation_dic = {}
    custom_property_dic = {}
    edge_crease_dic = {}
    edge_smoothing_dic = {}
    origin_object_dic = {}
    applied_mesh_dic = {}
    current_selection_dic = {}
    current_pose_dic = {}
    ik_dic = {}
    camera_key_dic = {}
    save_use_keyframe_insert_auto = context.tool_settings.use_keyframe_insert_auto
    if save_use_keyframe_insert_auto:
        context.tool_settings.use_keyframe_insert_auto = False
    save_current_selections(context, current_selection_dic)
    save_current_poses(context, context_objects, current_pose_dic)
    current_frame = context.scene.frame_current
    # make frame rate
    frame_rate = context.scene.render.fps / context.scene.render.fps_base
    make_hierarchy_dic(hierarchy_dic, use_only_deform_bones, use_rigify_armature, use_rigify_root_bone, use_only_selected_deform_bones, block_list, context_objects)
    # we must make applied mesh dic before reset all armatures if include armature deform modifier is enabled.
    if use_apply_modifiers and use_include_armature_deform_modifier:
        make_applied_mesh_dic(context, hierarchy_dic, origin_object_dic, applied_mesh_dic, use_include_armature_deform_modifier)
    # we pass all objects to the function to avoid armatures not be reset if the user selected only the meshes.
    reset_all_armatures(context, context_objects)
    # we must make applied mesh dic after reset all armatures if include armature deform modifier is disabled.
    if use_apply_modifiers and not use_include_armature_deform_modifier:
        make_applied_mesh_dic(context, hierarchy_dic, origin_object_dic, applied_mesh_dic, use_include_armature_deform_modifier)
    # Calculate bone correction matrix
    bone_correction_matrix = None  # Default is None = no change
    if (primary_bone_axis, secondary_bone_axis) != ('Y', 'X'):
        from bpy_extras.io_utils import axis_conversion
        bone_correction_matrix = axis_conversion(from_forward=secondary_bone_axis,
                                                 from_up=primary_bone_axis,
                                                 to_forward='X',
                                                 to_up='Y',
                                                 ).to_4x4()
    make_generic_node_dic(context, hierarchy_dic, use_only_deform_bones, node_dic, default_pose_dic, bind_pose_dic, vertex_dic, weight_dic, shape_dic, polygon_dic, uv_dic, tangent_dic, normal_dic, color_dic, polygon_material_dic, texture_dic, material_dic, mesh_material_dic, exist_object_dic, use_animation, use_timeline_range, my_animation_offset, my_animation_type, block_list, use_rigify_armature, camera_dic, light_dic, custom_property_dic, edge_crease_dic, use_edge_crease, my_edge_crease_scale, my_edge_smoothing, edge_smoothing_dic, applied_mesh_dic, ik_dic, use_embed_media, use_copy_texture, subdirname, packed_texture_filenames, bone_correction_matrix)
    # make animation
    if use_animation:
        if use_vertex_animation:
            make_all_vertex_animations(context, hierarchy_dic, node_dic, vertex_animation_dic, use_vertex_format, use_vertex_space, use_timeline_range, my_animation_offset, my_vertex_frame_start, my_vertex_frame_end, exist_object_dic)
        else:
            if my_animation_type == 'Active':
                make_active_action_or_nla_tracks(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic)
            elif my_animation_type == 'Actions':
                make_all_actions(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic)
            elif my_animation_type == 'Tracks':
                make_all_nla_tracks(context, hierarchy_dic, node_dic, pose_key_dic, shape_key_dic, camera_key_dic, use_driver_based_shape_key, my_animation_type, use_timeline_range, my_animation_offset, bone_correction_matrix, exist_object_dic)
            # concatenate all animations
            if use_concatenate_all:
                if my_animation_type == 'Actions' or my_animation_type == 'Tracks':
                    concatenate_all(node_dic, pose_key_dic, shape_key_dic)
    # remove any applied meshes
    remove_applied_mesh_dic(origin_object_dic, applied_mesh_dic)
    fix_compatibility_for_unity(hierarchy_dic)
    with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
        save_frame_rate(f, frame_rate)
        save_hierarchy_dic(f, hierarchy_dic)
        save_node_dic(f, node_dic)
        save_default_pose_dic(f, default_pose_dic)
        save_bind_pose_dic(f, bind_pose_dic)
        save_pose_key_dic(f, pose_key_dic)
        save_vertex_dic(f, vertex_dic)
        save_weight_dic(f, weight_dic, my_max_bone_influences)
        save_shape_dic(f, shape_dic)
        save_shape_key_dic(f, shape_key_dic)
        save_camera_key_dic(f, camera_key_dic)
        save_polygon_dic(f, polygon_dic)
        save_uv_dic(f, uv_dic)
        save_tangent_dic(f, tangent_dic)
        save_normal_dic(f, normal_dic)
        save_color_dic(f, color_dic)
        save_polygon_material_dic(f, polygon_material_dic)
        save_texture_dic(f, texture_dic)
        save_material_dic(f, material_dic)
        save_mesh_material_dic(f, mesh_material_dic)
        save_camera_dic(f, camera_dic)
        save_light_dic(f, light_dic)
        save_vertex_animation_dic(f, vertex_animation_dic)
        save_custom_property_dic(f, custom_property_dic)
        save_edge_crease_dic(f, edge_crease_dic)
        save_edge_smoothing_dic(f, edge_smoothing_dic)
        save_ik_dic(f, ik_dic)
    # set to current frame
    context.scene.frame_set(current_frame)
    restore_current_poses(context, context_objects, current_pose_dic)
    restore_current_selections(context, current_selection_dic)
    if save_use_keyframe_insert_auto:
        context.tool_settings.use_keyframe_insert_auto = True
    bpy.context.view_layer.update()
    print("="*30)

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class Hoyo2VRCExportFbx(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "hoyo2vrc_export.fbx"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Hoyo2VRC Export FBX"
    bl_options = {'UNDO', 'PRESET'}

    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'


    # ExportHelper mixin class uses this
    filename_ext = ""

    filter_glob: StringProperty(
            default="*.fbx;*.dae;*.obj;*.dxf",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    my_file_type: EnumProperty(
            name="File Type",
            description="File Type",
            items=(('.fbx', "FBX", "FBX (*.fbx)"),
                   ('.dae', "DAE", "Collada DAE (*.dae)"),
                   ('.obj', "OBJ", "Alias OBJ (*.obj)"),
                   ('.dxf', "DXF", "AutoCAD DXF (*.dxf)")),
            default='.fbx',
            )

    my_fbx_format: EnumProperty(
            name="FBX Format",
            description="File format",
            items=(('binary', "Binary", "FBX binary (*.fbx)"),
                   ('ascii', "Ascii", "FBX ascii (*.fbx)")),
            default='binary',
            )

    my_fbx_version: EnumProperty(
            name="FBX Version",
            description="File version compatibility",
            items=(('FBX53_MB55', "FBX53_MB55", "FBX_53_MB55_COMPATIBLE"),
                   ('FBX60_MB60', "FBX_60", "FBX_60_COMPATIBLE"),
                   ('FBX200508_MB70', "FBX_2005_08", "FBX_2005_08_COMPATIBLE"),
                   ('FBX200602_MB75', "FBX_2006_02", "FBX_2006_02_COMPATIBLE"),
                   ('FBX200608', "FBX_2006_08", "FBX_2006_08_COMPATIBLE"),
                   ('FBX200611', "FBX_2006_11", "FBX_2006_11_COMPATIBLE"),
                   ('FBX200900', "FBX_2009_00", "FBX_2009_00_COMPATIBLE"),
                   ('FBX200900v7', "FBX_2009_00_V7", "FBX_2009_00_V7_COMPATIBLE"),
                   ('FBX201000', "FBX_2010_00", "FBX_2010_00_COMPATIBLE"),
                   ('FBX201100', "FBX_2011_00", "FBX_2011_00_COMPATIBLE"),
                   ('FBX201200', "FBX_2012_00", "FBX_2012_00_COMPATIBLE"),
                   ('FBX201300', "FBX_2013_00", "FBX_2013_00_COMPATIBLE"),
                   ('FBX201400', "FBX_2014_00", "FBX_2014_00_COMPATIBLE"),
                   ('FBX201600', "FBX_2016_00", "FBX_2016_00_COMPATIBLE"),
                   ('FBX201800', "FBX_2018_00", "FBX_2018_00_COMPATIBLE"),
                   ('FBX201900', "FBX_2019_00", "FBX_2019_00_COMPATIBLE"),
                   ('FBX202000', "FBX_2020_00", "FBX_2020_00_COMPATIBLE")),
            default='FBX201800',
            )

    my_fbx_axis: EnumProperty(
            name="FBX Axis",
            description="File Axis",
            items=(('MayaZUp', "MayaZUp", "Compatible with Maya"),
                   ('OpenGL', "OpenGL", "Compatible with OpenGL"),
                   ('Unity', "Unity", "Rotate all contents 180 degrees around the vertical axis, let the character face you in Unity Editor. Warning: This pose is not compatible with the 'Humanoid' animation type, if you want to use the 'Humanoid' animation type in Unity Editor, please use 'MayaZUp' or 'OpenGL'"),
                   ('Unreal1', "Unreal1", "Rotate all contents -90 degrees around the vertical axis, let the character face you in Unreal Editor"),
                   ('Unreal2', "Unreal2", "Rotate all contents 90 degrees around the vertical axis, let the character turn his back on you in Unreal Editor"),
                   ),
            default='MayaZUp',
            )

    my_fbx_unit: EnumProperty(
            name="FBX Unit",
            description="FBX Unit",
            items=(('mm', "mm", "mm"),
                   ('dm', "dm", "dm"),
                   ('cm', "cm", "cm"),
                   ('m', "m", "m"),
                   ('km', "km", "km"),
                   ('Inch', "Inch", "Inch"),
                   ('Foot', "Foot", "Foot"),
                   ('Mile', "Mile", "Mile"),
                   ('Yard', "Yard", "Yard"),),
            default='cm',
            )

    use_selection: BoolProperty(
            name="Selected Objects",
            description="Export selected and visible objects only",
            default=False,
            )

    use_active_collection: BoolProperty(
            name="Active Collection",
            description="Export only objects from the active collection (and its children)",
            default=False,
            )

    use_visible: BoolProperty(
            name="Visible Objects",
            description="Export visible objects only",
            default=False,
            )

    use_only_deform_bones: BoolProperty(
            name="Only Deform Bones",
            description="Export only deform bones",
            default=False,
            )

    use_only_selected_deform_bones: BoolProperty(
            name="Only Selected Deform Bones",
            description="Export only selected deform bones in 'EDIT' mode",
            default=False,
            )

    use_vertex_animation: BoolProperty(
            name="Vertex Animation",
            description="Export vertex animation",
            default=False,
            )

    use_vertex_format: EnumProperty(
            name="Vertex Format",
            description="Vertex format",
            items=(('mcx', "Maya(.mcx)", "Maya format"),
                   ('pc2', "3DS Max(.pc2)", "3DS Max format")),
            default='mcx',
            )

    use_vertex_space: EnumProperty(
            name="Vertex Space",
            description="Vertex space",
            items=(('local', "Local Space", "Local Space"),
                   ('world', "World Space", "World Space")),
            default='world',
            )

    my_vertex_frame_start: IntProperty(
        name = "Frame Start",
        description = "Vertex Animation Frame Start",
        default = 1,
        min = -1000000,
        max = 1000000)

    my_vertex_frame_end: IntProperty(
        name = "Frame End",
        description = "Vertex Animation Frame End",
        default = 10,
        min = -1000000,
        max = 1000000)

    use_animation: BoolProperty(
            name="Animation",
            description="Export animation",
            default=True,
            )

    use_timeline_range: BoolProperty(
            name="Timeline Range",
            description="Export animations in the timeline range",
            default=False,
            )

    my_animation_offset: IntProperty(
        name = "Animation Offset",
        description = "Add an offset to all keyframes",
        default = 0,
        min = -1000000,
        max = 1000000)

    use_apply_modifiers: BoolProperty(
            name="Apply Modifiers",
            description="Apply all modifiers on mesh objects except armature deform ones, but all mesh objects with shape keys will be ignored",
            default=True,
            )

    use_include_armature_deform_modifier: BoolProperty(
            name="Include Armature Deform Modifier",
            description="Apply armature deform modifiers on mesh objects too when the 'Apply Modifiers' option is enabled",
            default=False,
            )

    use_triangulate: BoolProperty(
            name="Triangulate",
            description="Triangulate meshes",
            default=False,
            )

    use_raw_normals_and_raw_tangents: BoolProperty(
            name="Raw Normals And Raw Tangents",
            description="Export raw normals and raw tangents, the fbx file will get larger, but the tangents will be loaded correctly into Unreal Editor due to a bug of its FBX importer",
            default=False,
            )

    use_driver_based_shape_key: BoolProperty(
            name="Driver Based Shape Key",
            description="If the blend shapes are driven by bones, you need to enable this option",
            default=False,
            )

    my_animation_type: EnumProperty(
            name="Animation Type",
            description="Single animation or multiple animations",
            items=(('Active', "Active Animation", "Export the active animation, if an object has any NLA tracks, export the active NLA track; Otherwise, export the active action"),
                   ('Actions', "All Actions", "Export all actions"),
                   ('Tracks', "All NLA Tracks", "Export all NLA tracks")),
            default='Active',
            )

    use_concatenate_all: BoolProperty(
            name="Concatenate All",
            description="When exporting all animations, concatenate all actions or NLA tracks into a single action",
            default=False,
            )

    my_max_bone_influences: EnumProperty(
            name="Max Bone Influences",
            description="Maximum bone influences you can have per vertex",
            items=(('2', "2", "Suitable for mobile game"),
                   ('3', "3", "Suitable for mobile game"),
                   ('4', "4", "Suitable for mobile game"),
                   ('6', "6", "Suitable for desktop game"),
                   ('8', "8", "Suitable for desktop game"),
                   ('Unlimited', "Unlimited", "Suitable for generic animation")),
            default='Unlimited',
            )

    primary_bone_axis: EnumProperty(
            name="Primary Bone Axis",
            description="User defined primary bone axis",
            items=(('X', "X Axis", ""),
                   ('Y', "Y Axis", ""),
                   ('Z', "Z Axis", ""),
                   ('-X', "-X Axis", ""),
                   ('-Y', "-Y Axis", ""),
                   ('-Z', "-Z Axis", ""),
                   ),
            default='Y',
            )

    secondary_bone_axis: EnumProperty(
            name="Secondary Bone Axis",
            description="User defined primary bone axis",
            items=(('X', "X Axis", ""),
                   ('Y', "Y Axis", ""),
                   ('Z', "Z Axis", ""),
                   ('-X', "-X Axis", ""),
                   ('-Y', "-Y Axis", ""),
                   ('-Z', "-Z Axis", ""),
                   ),
            default='X',
            )

    use_rigify_armature: BoolProperty(
            name="Rigify Armature",
            description="Make game-friendly armature for Rigify Auto-Rigging System",
            default=False,
            )

    use_rigify_root_bone: BoolProperty(
            name="Keep Root Bone",
            description="Keep the root bone when making game-friendly armature for Rigify Auto-Rigging System",
            default=True,
            )

    my_scale: FloatProperty(
        name = "Scale",
        description = "Scale all data",
        default = 1.0,
        min = 0.0001,
        max = 10000.0)

    use_optimize_for_game_engine: BoolProperty(
            name="Optimize For Game Engine",
            description="Make game engine friendly translation, rotation and scaling",
            default=True,
            )

    use_reset_mesh_origin: BoolProperty(
            name="Reset Mesh Origin",
            description="Reset mesh origin to world origin when 'Optimize For Game Engine' is enabled",
            default=True,
            )

    use_reset_mesh_rotation: BoolProperty(
            name="Reset Mesh Rotation",
            description="Reset mesh rotation to zero when 'Optimize For Game Engine' is enabled",
            default=True,
            )

    use_only_root_empty_node: BoolProperty(
            name="Only Root Empty Node",
            description="Reset rotation and scaling only for the empty nodes at root hierarchy, ignore the empty nodes not at root hierarchy when 'Optimize For Game Engine' is enabled",
            default=True,
            )

    use_ignore_armature_node: BoolProperty(
            name="Ignore Armature Node",
            description="Do not export the armature node as a dummy node",
            default=True,
            )

    use_edge_crease: BoolProperty(
            name="Edge Crease",
            description="Export edge crease",
            default=True,
            )

    my_edge_smoothing: EnumProperty(
            name="Smoothing Groups",
            description="How to generate smoothing groups",
            items=(('None', "None", "Does not generate smoothing groups"),
                   ('Blender', "Generate By Hard Edges", "Generate smoothing groups from hard edges by Blender"),
                   ('FBXSDK', "Generate By FBX SDK", "Generate smoothing groups from normals by FBX SDK")),
            default='FBXSDK',
            )

    my_edge_crease_scale: FloatProperty(
        name = "Edge Crease Scale",
        description = "Scale of edge crease weights",
        default = 1.0,
        min = 0.0001,
        max = 10000.0)

    my_separate_files: BoolProperty(
            name="Separate Files",
            description="Export to separate files",
            default=False,
            )

    use_move_to_origin: BoolProperty(
            name="Move To Origin",
            description="Move each object to origin when exporting, and move it back after exporting",
            default=False,
            )

    my_material_style: EnumProperty(
            name="Material Style",
            description="How to map texture images to FBX's standard material property names",
            items=(('Blender', "Blender", "Compatible with Blender's material system"),
                   ('Unity', "Unity Engine", "Compatible with Unity Engine's material system"),
                   ('Unreal', "Unreal Engine", "Compatible with Unreal Engine's material system"),
                   ('Godot', "Godot Engine", "Compatible with Godot Engine's material system")),
            default='Blender',
            )

    use_embed_media: BoolProperty(
            name="Embed Media",
            description="Embed all texture images into FBX file",
            default=False,
            )

    use_copy_texture: BoolProperty(
            name="Copy Textures",
            description="If not embed media, copy texture images to user-defined subdirectory",
            default=False,
            )

    my_texture_subdirectory: StringProperty(
            name="Subdirectory",
            description="User-defined subdirectory",
            default="textures",
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    my_simplify_algorithm: EnumProperty(
            name="Simplify Keyframe",
            description="Simplify keyframe values by removing similar keyframe values",
            items=(('0', "Do Not Simplify   ", "Don't simplify keyframes at all, keep all keyframes"),
                   ('1', "By Relative Height", "This algorithm measure error with a threshold(In Percentages), it is based on the relative height differences of the sampled curve, and it is compatible with Blender's built-in keyframe simplify algorithm"),
                   ('2', "By Douglas Peuker ", "This algorithm measure error with a threshold(In Percentages), it is based on the famous Douglas-Peuker algorithm"),
                   ('3', "By Relative Angle ", "This algorithm measure error with a threshold(In Percentages), it is based on the relative angle differences of the sampled curve"),
                   ('4', "By Absolute Angle ", "This algorithm is based on the absolute angle differences of the sampled curve, smooth parts will be reduced to straight lines, the higher the angle threshold(In degrees), the more will be simplified. To get best result, you need to test with different angle thresholds(In degrees) manually")),
            default='0',
            )

    my_simplify_keyframe_factor: FloatProperty(
        name = "Simplify Threshold",
        description = "How much to simplify keyframe values, the higher the threshold, the more will be simplified",
        default = 1.0,
        min = 0.0,
        max = 180.0)

    use_unroll_filter: BoolProperty(
            name="Unroll Filter",
            description="Fix unexpected sudden rolls",
            default=False,
            )

    use_independent_animation_stack: BoolProperty(
            name="Independent Animation Stack",
            description="Export animations as independent animation stacks",
            default=False,
            )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Basic Options:")
        box.prop(self, 'my_file_type')
        box.prop(self, 'use_selection')
        box.prop(self, 'use_active_collection')
        box.prop(self, 'use_visible')
        box.prop(self, 'my_fbx_unit')
        box.prop(self, 'my_scale')

        box = layout.box()
        box.label(text="FBX Options:")
        box.prop(self, 'my_fbx_format')
        box.prop(self, 'my_fbx_version')
        box.prop(self, 'my_fbx_axis')
        box.prop(self, 'my_material_style')
        box.prop(self, 'use_embed_media')

        box = layout.box()
        box.label(text="Texture Options:")
        box.prop(self, 'use_copy_texture')
        box.prop(self, 'my_texture_subdirectory')

        box = layout.box()
        box.label(text="Rigify Auto-Rigging System Options:")
        box.prop(self, 'use_rigify_armature')
        box.prop(self, 'use_rigify_root_bone')

        box = layout.box()
        box.label(text="Bone Options:")
        box.prop(self, 'primary_bone_axis')
        box.prop(self, 'secondary_bone_axis')
        box.prop(self, 'use_only_deform_bones')
        box.prop(self, 'use_only_selected_deform_bones')
        box.prop(self, 'my_max_bone_influences')

        box = layout.box()
        box.label(text="Animation Options:")
        box.prop(self, 'use_animation')
        box.prop(self, 'use_timeline_range')
        box.prop(self, 'my_animation_offset')
        box.prop(self, 'use_driver_based_shape_key')
        box.prop(self, 'my_animation_type')
        box.prop(self, 'use_concatenate_all')
        box.prop(self, 'use_independent_animation_stack')
        box.prop(self, 'my_simplify_algorithm')
        box.prop(self, 'my_simplify_keyframe_factor')
        box.prop(self, 'use_unroll_filter')

        box = layout.box()
        box.label(text="Vertex Animation Options:")
        box.prop(self, 'use_vertex_animation')
        box.prop(self, 'use_vertex_format')
        box.prop(self, 'use_vertex_space')
        box.prop(self, 'my_vertex_frame_start')
        box.prop(self, 'my_vertex_frame_end')

        box = layout.box()
        box.label(text="Game Engine Options:")
        box.prop(self, 'use_optimize_for_game_engine')
        row = box.row()
        row.prop(self, 'use_reset_mesh_origin')
        row.enabled = self.use_optimize_for_game_engine
        row = box.row()
        row.prop(self, 'use_reset_mesh_rotation')
        row.enabled = self.use_optimize_for_game_engine
        row = box.row()
        row.prop(self, 'use_only_root_empty_node')
        row.enabled = self.use_optimize_for_game_engine
        box.prop(self, 'use_ignore_armature_node')

        box = layout.box()
        box.label(text="Mesh Options:")
        box.prop(self, 'use_apply_modifiers')
        row = box.row()
        row.prop(self, 'use_include_armature_deform_modifier')
        row.enabled = self.use_apply_modifiers
        box.prop(self, 'use_triangulate')
        box.prop(self, 'use_raw_normals_and_raw_tangents')

        box = layout.box()
        box.label(text="Edge Options:")
        box.prop(self, 'my_edge_smoothing')
        box.prop(self, 'use_edge_crease')
        box.prop(self, 'my_edge_crease_scale')

        box = layout.box()
        box.label(text="Batch Options:")
        box.prop(self, 'my_separate_files')
        box.prop(self, 'use_move_to_origin')


    def clean_temporary_files(self, subdirname, output_path, packed_texture_filenames):
        if os.path.exists(output_path):
            os.remove(output_path)
        if not self.use_embed_media and self.use_copy_texture and len(packed_texture_filenames) > 0:
            if not os.path.exists(subdirname):
                os.mkdir(subdirname)
            for unpacked_texture_filename in packed_texture_filenames:
                src = unpacked_texture_filename
                dst = os.path.join(subdirname, os.path.basename(unpacked_texture_filename))
                # do not overwrite image
                if os.path.exists(src) and not os.path.exists(dst):
                    shutil.copy(src, dst)
        output_directory = os.path.dirname(output_path)
        for unpacked_texture_filename in packed_texture_filenames:
            unpacked_texture_directory = os.path.dirname(unpacked_texture_filename)
            if unpacked_texture_directory == output_directory:
                if os.path.exists(unpacked_texture_filename):
                    os.remove(unpacked_texture_filename)


    def execute(self, context):
        start_time = time.time()
        # do the job in background
        executable_path = None
        if platform.system() == 'Windows':
            if platform.machine().lower().endswith('amd64') or platform.machine().lower().endswith('x86_64'):
                executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "x64", "fbx-utility")
            elif platform.machine().lower().endswith('arm64') or platform.machine().lower().endswith('aarch64'):
                executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "arm64", "fbx-utility")
            else:
                executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "x86", "fbx-utility")
        else:
            if platform.system() == 'Linux':
                glibc_version = os.confstr('CS_GNU_LIBC_VERSION').split(" ")
                if glibc_version[0] == 'glibc' and glibc_version[1] >= '2.29':
                    executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "fbx-utility")
                else:
                    executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "fbx-utility2")
            elif platform.system() == 'Darwin':
                if platform.mac_ver()[0] >= '10.15':
                    executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "fbx-utility")
                elif platform.mac_ver()[0] >= '10.13':
                    executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "fbx-utility2")
                else:
                    executable_path = os.path.join(os.path.dirname(__file__), "bin", platform.system(), "fbx-utility3")
            # chmod
            if not os.access(executable_path, os.X_OK):
                os.chmod(executable_path, 0o755)

        # delete deprecated output path
        deprecated_output_path = os.path.join(os.path.dirname(__file__), "data", "untitled-fbx.txt")
        if os.path.exists(deprecated_output_path):
            os.remove(deprecated_output_path)

        # write to inner format
        output_path = os.path.join(os.path.dirname(__file__), "data", uuid.uuid4().hex + ".txt")
        # get directory name
        dirname = os.path.dirname(self.filepath)
        # get subdirectory name
        subdirname = os.path.join(dirname, self.my_texture_subdirectory)

        if self.use_active_collection:
            if self.use_selection:
                context_objects = tuple(ob for ob in context.view_layer.active_layer_collection.collection.all_objects if ob.select_get())
            else:
                context_objects = context.view_layer.active_layer_collection.collection.all_objects
        else:
            if self.use_selection:
                context_objects = context.selected_objects
            else:
                context_objects = context.view_layer.objects
        if self.use_visible:
            context_objects = tuple(ob for ob in context_objects if ob.visible_get())

        packed_texture_filenames = []

        # batch export
        if self.my_separate_files:
            # export every context object separately
            for context_object in context_objects:
                if self.use_move_to_origin:
                    # save the translation
                    save_translation_x = context_object.matrix_world[0][3]
                    save_translation_y = context_object.matrix_world[1][3]
                    save_translation_z = context_object.matrix_world[2][3]
                    # reset the translation
                    context_object.matrix_world[0][3] = 0.0
                    context_object.matrix_world[1][3] = 0.0
                    context_object.matrix_world[2][3] = 0.0
                    bpy.context.view_layer.update()
                write_some_data(context, output_path, [context_object], self.use_animation, self.use_timeline_range, self.my_animation_offset, self.use_driver_based_shape_key, self.my_animation_type, True if self.use_rigify_armature or self.use_only_selected_deform_bones else self.use_only_deform_bones, self.use_rigify_armature, self.use_rigify_root_bone, self.use_only_selected_deform_bones, self.my_max_bone_influences, self.primary_bone_axis, self.secondary_bone_axis, self.use_vertex_animation, self.use_vertex_format, self.use_vertex_space, self.my_vertex_frame_start, self.my_vertex_frame_end, self.use_edge_crease, self.my_edge_crease_scale, self.my_edge_smoothing, self.use_apply_modifiers, self.use_include_armature_deform_modifier, self.use_concatenate_all, self.use_embed_media, self.use_copy_texture, subdirname, packed_texture_filenames)
                if self.use_move_to_origin:
                    # restore the translation
                    context_object.matrix_world[0][3] = save_translation_x
                    context_object.matrix_world[1][3] = save_translation_y
                    context_object.matrix_world[2][3] = save_translation_z
                    bpy.context.view_layer.update()

                # add extension if not exists
                filepath = bpy.path.ensure_ext(os.path.join(dirname, context_object.name), self.my_file_type)
                result = subprocess.run([executable_path, output_path, filepath, str(self.my_scale), self.my_fbx_format, self.my_fbx_version, self.my_fbx_axis, "None", "None", "True" if self.use_optimize_for_game_engine else "False", "True" if self.use_ignore_armature_node else "False", "True" if self.use_reset_mesh_origin else "False", "True" if self.use_reset_mesh_rotation else "False", "None", "True" if self.use_triangulate else "False", "True" if self.use_raw_normals_and_raw_tangents else "False", "None", self.my_edge_smoothing, "True" if self.use_embed_media else "False", self.my_simplify_algorithm, str(self.my_simplify_keyframe_factor), self.my_material_style, "True" if self.use_unroll_filter else "False", self.my_fbx_unit, "True" if self.use_independent_animation_stack else "False", "True" if self.use_only_root_empty_node else "False", "None"])

                if result.returncode != 0:
                    self.clean_temporary_files(subdirname, output_path, packed_texture_filenames)
                    return {'CANCELLED'}
        else:
            write_some_data(context, output_path, context_objects, self.use_animation, self.use_timeline_range, self.my_animation_offset, self.use_driver_based_shape_key, self.my_animation_type, True if self.use_rigify_armature or self.use_only_selected_deform_bones else self.use_only_deform_bones, self.use_rigify_armature, self.use_rigify_root_bone, self.use_only_selected_deform_bones, self.my_max_bone_influences, self.primary_bone_axis, self.secondary_bone_axis, self.use_vertex_animation, self.use_vertex_format, self.use_vertex_space, self.my_vertex_frame_start, self.my_vertex_frame_end, self.use_edge_crease, self.my_edge_crease_scale, self.my_edge_smoothing, self.use_apply_modifiers, self.use_include_armature_deform_modifier, self.use_concatenate_all, self.use_embed_media, self.use_copy_texture, subdirname, packed_texture_filenames)

            # add extension if not exists
            filepath = bpy.path.ensure_ext(self.filepath, self.my_file_type)
            result = subprocess.run([executable_path, output_path, filepath, str(self.my_scale), self.my_fbx_format, self.my_fbx_version, self.my_fbx_axis, "None", "None", "True" if self.use_optimize_for_game_engine else "False", "True" if self.use_ignore_armature_node else "False", "True" if self.use_reset_mesh_origin else "False", "True" if self.use_reset_mesh_rotation else "False", "None", "True" if self.use_triangulate else "False", "True" if self.use_raw_normals_and_raw_tangents else "False", "None", self.my_edge_smoothing, "True" if self.use_embed_media else "False", self.my_simplify_algorithm, str(self.my_simplify_keyframe_factor), self.my_material_style, "True" if self.use_unroll_filter else "False", self.my_fbx_unit, "True" if self.use_independent_animation_stack else "False", "True" if self.use_only_root_empty_node else "False", "None"])

            if result.returncode != 0:
                self.clean_temporary_files(subdirname, output_path, packed_texture_filenames)
                return {'CANCELLED'}

        self.clean_temporary_files(subdirname, output_path, packed_texture_filenames)
        print("Finished in: {:.2f} seconds.".format(time.time() - start_time))
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(Hoyo2VRCExportFbx.bl_idname, text="Hoyo FBX Exporter (.fbx/.dae/.obj/.dxf)")


def register_exporter():
    bpy.utils.register_class(Hoyo2VRCExportFbx)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister_exporter():
    bpy.utils.unregister_class(Hoyo2VRCExportFbx)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register_exporter()

    # test call
    bpy.ops.hoyo2vrc_export.fbx('INVOKE_DEFAULT')
