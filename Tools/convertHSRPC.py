import bpy
from bpy.types import Operator
import os


## TO DO: Find a fix for HSR end name 001


class ConvertHonkaiStarRailPlayerCharacter(Operator):
    """Convert Model"""

    bl_idname = "hoyo2vrc.converthsrpc"
    bl_label = "OperatorLabel"

    def execute(self, context):
        blender_version = bpy.app.version

        def ScaleModel():
            for ob in bpy.context.scene.objects:
                if ob.type in ["ARMATURE"]:
                    ob.select_set(True)
                    bpy.ops.transform.resize(
                        value=(100, 100, 100),
                        orient_type="GLOBAL",
                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                        orient_matrix_type="GLOBAL",
                        constraint_axis=(True, True, True),
                        mirror=False,
                        use_proportional_edit=False,
                        proportional_edit_falloff="SMOOTH",
                        proportional_size=1,
                        use_proportional_connected=False,
                        use_proportional_projected=False,
                        snap=False,
                        snap_elements={"INCREMENT"},
                        use_snap_project=False,
                        snap_target="CLOSEST",
                        use_snap_self=True,
                        use_snap_edit=False,
                        use_snap_nonedit=False,
                        use_snap_selectable=False,
                    )
                    ob.select_set(False)

        def RemoveEmpties():
            for ob in bpy.context.scene.objects:
                if ob.type == "EMPTY":
                    ob.select_set(True)
                    Empties = ob
                    bpy.data.objects.remove(Empties, do_unlink=True)

        def GenerateShapeKeys():
            def get_shapekey(object_name, shape_name):
                bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
                if bpy.context.object.data.shape_keys == None:
                    return None
                for shape_key in bpy.context.object.data.shape_keys.key_blocks:
                    if shape_key.name == shape_name:
                        return shape_key

            def reset_pose(root_object):
                bpy.context.view_layer.objects.active = root_object
                bpy.ops.object.posemode_toggle()
                bpy.ops.pose.select_all(action="SELECT")
                bpy.ops.pose.transforms_clear()
                bpy.ops.object.posemode_toggle()

            root = bpy.context.active_object
            face_obj = bpy.data.objects["Face"]

            if (
                "Avatar" not in root.name
                and "Player" not in root.name
                and "Art" not in root.name
                and "NPC_Avatar" not in root.name
            ):
                raise BaseException("Valid object is not selected.")

            if face_obj is None:
                raise BaseException("Not found the Face object.")

            bpy.ops.object.mode_set(mode="OBJECT")
            reset_pose(root)

            # add basis shape
            if get_shapekey("Face", "Basis") == None:
                bpy.context.view_layer.objects.active = bpy.data.objects["Face"]
                bpy.ops.object.shape_key_add(from_mix=False)

            # convert animation to shapekey
            for action in bpy.data.actions:
                if ".00" in action.name or "Emo_" not in action.name:
                    continue

                print(action.name)
                arr = action.name.split("_")
                shapekey_name = "_".join(arr[2:])

                if not bpy.data.actions:
                    print("No Animations Found.")
                    break

                # apply animation
                if root is not None and action is not None:
                    root.animation_data.action = action
                    bpy.ops.object.visual_transform_apply()

                # convert shapekay
                bpy.context.view_layer.objects.active = face_obj
                bpy.ops.object.modifier_apply_as_shapekey(
                    keep_modifier=True, modifier=face_obj.modifiers[0].name
                )
                shapekey = get_shapekey(face_obj.name, face_obj.modifiers[0].name)
                shapekey.name = shapekey_name

                # reset transform
                reset_pose(root)

        def clear_animation_data():
            obj = bpy.context.object
            if obj is not None:
                # Remove all animation data
                obj.animation_data_clear()

                # Remove all animations
                for action in bpy.data.actions:
                    if action.users == 0:
                        bpy.data.actions.remove(action)

        def ClearRotations():
            for ob in bpy.context.scene.objects:
                if ob.type == "ARMATURE":
                    ob.select_set(True)
                    ob.rotation_euler = [0, 0, 0]
                    ob.select_set(False)

        def CleanMeshes():
            for obj in bpy.data.objects:
                if obj.type == "MESH" and obj.name in ["EffectMesh", "EyeStar"]:
                    bpy.data.objects.remove(obj, do_unlink=True)

        def FaceMask():
            maskObj = bpy.context.scene.objects["Face_Mask"]
            maskObj.vertex_groups.new(name="Head")
            for vertex in maskObj.data.vertices:
                vertList = []
                vertList.append(vertex.index)
                try:
                    headGroup = maskObj.vertex_groups["Head"]
                    headGroup.add(vertList, 1.0, "REPLACE")
                except:
                    continue

        def MergeMeshes():
            # Get all the meshes in the scene
            meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]

            # Select all the meshes except Face_Mask and Weapon
            for mesh in meshes:
                if mesh.name not in ["Weapon"]:
                    mesh.select_set(True)

            # Set the active object to the first selected mesh
            bpy.context.view_layer.objects.active = [
                obj for obj in meshes if obj.select_get()
            ][0]

            # Join the selected meshes
            bpy.ops.object.join()

            # Rename the resulting mesh to "Body" if it has a different name
            if bpy.context.active_object.name != "Body":
                bpy.context.active_object.name = "Body"

            # Deselect all the meshes
            bpy.ops.object.select_all(action="DESELECT")

        def RenameBones():
            # Define the bone names and new names
            bone_names = [
                "Root_M",
                "Hip_L",
                "Hip_R",
                "HipPart1_R",
                "HipPart1_L",
                "Spine1_M",
                "Spine2_M",
                "Chest_M",
                "Shoulder_L",
                "Shoulder_R",
                "Scapula_R",
                "Scapula_L",
                "Neck_M",
                "Head_M",
            ]
            new_names = [
                "Hips",
                "Left leg",
                "Right leg",
                "Right leg twist R",
                "Left leg twist L",
                "Spine",
                "Chest",
                "Upper chest",
                "Left arm",
                "Right arm",
                "Right shoulder",
                "Left shoulder",
                "Neck",
                "Head",
            ]

            # Get the armature object
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == "ARMATURE":
                    armature = obj
                    break

            # Rename the bones
            if armature is not None:
                for bone in armature.pose.bones:
                    if bone.name in bone_names:
                        bone.name = new_names[bone_names.index(bone.name)]

        def CleanBones():
            # Define the bone names to remove
            bone_names = ["Skin_GRP", "Main"]

            # Get the armature object
            armature = None
            for obj in bpy.context.scene.objects:
                if obj.type == "ARMATURE":
                    armature = obj
                    break

            # Set the active object in the context
            bpy.context.view_layer.objects.active = armature

            # Switch to edit mode
            bpy.ops.object.mode_set(mode="EDIT")

            # Remove the bones
            if armature is not None:
                for bone in armature.data.edit_bones:
                    if bone.name in bone_names:
                        armature.data.edit_bones.remove(bone)

            # Switch back to pose mode
            bpy.ops.object.mode_set(mode="OBJECT")

        def FixModelBoneView():
            bpy.context.scene.combine_mats = False
            bpy.context.scene.remove_zero_weight = False
            bpy.context.scene.remove_rigidbodies_joints = False
            bpy.context.scene.join_meshes = False
            bpy.ops.cats_armature.fix()
            # The problem lies with toggling join meshes it being on works good, but off breaks the weights of the eyes
            bpy.context.object.display_type = "WIRE"

        def FixVRCLite():
            ob = bpy.data.objects["Armature"]
            armature = ob.data
            bpy.data.objects["Armature"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            def attachfeets(foot, toe):
                armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x
                armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
                armature.edit_bones[foot].tail.z = armature.edit_bones[toe].head.z

            attachfeets("Spine", "Chest")
            attachfeets("Hips", "Spine")
            bpy.ops.object.mode_set(mode="OBJECT")

        def FixEyes():
            ob = bpy.data.objects["Armature"]
            armature = ob.data
            bpy.data.objects["Armature"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.armature.select_all(action="DESELECT")

            def attacheyes(foot, toe):
                armature.edit_bones[foot].tail.z = (
                    armature.edit_bones[toe].head.z - armature.edit_bones[foot].tail.y
                )
                armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
                armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x

            attacheyes("Eye_L", "Eye_All_L")
            attacheyes("Eye_R", "Eye_All_R")

            # Get the armature object and enter edit mode
            armature_obj = bpy.data.objects["Armature"]
            armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = armature_obj
            bpy.ops.object.mode_set(mode="EDIT")

            # Get the Eye_L and Eye_R bones
            eye_l_bone = armature_obj.data.edit_bones.get("Eye_L")
            eye_r_bone = armature_obj.data.edit_bones.get("Eye_R")
            face_bone = armature_obj.data.edit_bones.get("Face")

            # Get the Head bone
            head_bone = armature_obj.data.edit_bones.get("Head")

            # Reparent the Eye_L and Eye_R bones to the Head bone
            if eye_l_bone and eye_r_bone and face_bone and head_bone:
                eye_l_bone.parent = head_bone
                eye_r_bone.parent = head_bone
                face_bone.parent = head_bone

            # Exit edit mode
            bpy.ops.object.mode_set(mode="OBJECT")

        def ApplyTransforms():
            for ob in bpy.context.scene.objects:
                if ob.type in ["MESH", "ARMATURE"]:
                    ob.select_set(True)
                    bpy.ops.object.transform_apply(
                        location=True, rotation=True, scale=True
                    )
                    ob.select_set(False)

        def RequestMeshMerge():
            if bpy.context.scene.merge_all_meshes:
                # User checked "Merge All Meshes", so merge all meshes

                # Deselect all objects
                bpy.ops.object.select_all(action='DESELECT')

                # Select all mesh objects
                mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
                for obj in mesh_objects:
                    obj.select_set(True)

                # Set the active object to "Body" if it exists, otherwise use the first mesh object
                body_object = bpy.data.objects.get("Body")
                if body_object is not None:
                    bpy.context.view_layer.objects.active = body_object
                elif mesh_objects:
                    bpy.context.view_layer.objects.active = mesh_objects[0]

                # Join the selected objects into the active object
                bpy.ops.object.join()

                # Rename the active object to "Body"
                bpy.context.active_object.name = "Body"
            else:
                # User unchecked "Merge All Meshes", so do nothing
                pass
            
        def Run():
            ScaleModel()
            RemoveEmpties()
            GenerateShapeKeys()
            clear_animation_data()
            ClearRotations()
            CleanMeshes()
            FaceMask()
            MergeMeshes()
            RenameBones()
            CleanBones()
            FixModelBoneView()
            FixVRCLite()
            FixEyes()
            RequestMeshMerge()
            ApplyTransforms()

        Run()

        return {"FINISHED"}
