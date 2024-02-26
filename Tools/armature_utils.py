import bpy
import re


def StripName(name):
    """Remove any prefix in the format 'Name_C(number)_' or 'Name_' from a name."""
    return re.sub(r"^\w+_C\d+_|^[^_]+_", "", name)


def GetArmature():
    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE":
            return obj
    return None


def GetGameData(game):
    if game == "Genshin Impact":
        return {
            "bone_names": {
                "Pelvis": "Hips",
                "LThigh": "Left leg",
                "RThigh": "Right leg",
                "LCalf": "Left knee",
                "RCalf": "Right knee",
                "LFoot": "Left ankle",
                "RFoot": "Right ankle",
                "LToe0": "Left toe",
                "RToe0": "Right toe",
                "LClavicle": "Left shoulder",
                "RClavicle": "Right shoulder",
                "LUpperArm": "Left arm",
                "RUpperArm": "Right arm",
                "LForearm": "Left elbow",
                "RForearm": "Right elbow",
                "LHand": "Left wrist",
                "RHand": "Right wrist",
                "LFinger0": "Thumb1_L",
                "LFinger01": "Thumb2_L",
                "LFinger02": "Thumb3_L",
                "LFinger1": "IndexFinger1_L",
                "LFinger11": "IndexFinger2_L",
                "LFinger12": "IndexFinger3_L",
                "LFinger2": "MiddleFinger1_L",
                "LFinger21": "MiddleFinger2_L",
                "LFinger22": "MiddleFinger3_L",
                "LFinger3": "RingFinger1_L",
                "LFinger31": "RingFinger2_L",
                "LFinger32": "RingFinger3_L",
                "LFinger4": "LittleFinger1_L",
                "LFinger41": "LittleFinger2_L",
                "LFinger42": "LittleFinger3_L",
                "RFinger0": "Thumb1_R",
                "RFinger01": "Thumb2_R",
                "RFinger02": "Thumb3_R",
                "RFinger1": "IndexFinger1_R",
                "RFinger11": "IndexFinger2_R",
                "RFinger12": "IndexFinger3_R",
                "RFinger2": "MiddleFinger1_R",
                "RFinger21": "MiddleFinger2_R",
                "RFinger22": "MiddleFinger3_R",
                "RFinger3": "RingFinger1_R",
                "RFinger31": "RingFinger2_R",
                "RFinger32": "RingFinger3_R",
                "RFinger4": "LittleFinger1_R",
                "RFinger41": "LittleFinger2_R",
                "RFinger42": "LittleFinger3_R",
            },
            "starts_with": {
                "_": "",
                "ValveBiped_": "",
                "Valvebiped_": "",
                "Bip1_": "Bip_",
                "Bip01_": "Bip_",
                "Bip01": "",
                "Bip001": "",
                "Bip02_": "Bip_",
                "Character1_": "",
                "HLP_": "",
                "JD_": "",
                "JU_": "",
                "Armature|": "",
                "Bone_": "",
                "C_": "",
                "Cf_S_": "",
                "Cf_J_": "",
                "G_": "",
                "Joint_": "",
                "Def_C_": "",
                "Def_": "",
                "DEF_": "",
                "Chr_": "",
                "B_": "",
            },
            "ends_with": {
                "_Bone": "",
                "_Bn": "",
                "_Le": "_L",
                "_Ri": "_R",
                "_": "",
            },
            "replaces": {
                " ": "_",
                "-": "_",
                ".": "_",
                ":": "_",
                "____": "_",
                "___": "_",
                "__": "_",
                "_Le_": "_L_",
                "_l": "_L",
                "_Ri_": "_R_",
                "_r": "_R",
                "_m": "_M",
                "LEFT": "Left",
                "RIGHT": "Right",
                "all": "All",
                "finger": "Finger",
                "part": "Part",
            },
        }
    elif game == "Honkai Star Rail":
        return {
            "bone_names": {
                "Root_M": "Hips",
                "Hip_L": "Left leg",
                "Hip_R": "Right leg",
                "HipPart1_R": "Right leg twist R",
                "HipPart1_L": "Left leg twist L",
                "Spine1_M": "Spine",
                "Spine2_M": "Chest",
                "Chest_M": "Upper Chest",
                "Shoulder_L": "Left arm",
                "Shoulder_R": "Right arm",
                "Scapula_R": "Right shoulder",
                "Scapula_L": "Left shoulder",
                "Neck_M": "Neck",
                "Head_M": "Head",
                "face": "Face",
                "Knee_L": "Left knee",
                "Knee_R": "Right knee",
                "Ankle_L": "Left ankle",
                "Ankle_R": "Right ankle",
                "Toes_L": "Left toe",
                "Toes_R": "Right toe",
                "Elbow_L": "Left elbow",
                "Elbow_R": "Right elbow",
                "Wrist_L": "Left wrist",
                "Wrist_R": "Right wrist",
            },
            "starts_with": {
                "_": "",
                "ValveBiped_": "",
                "Valvebiped_": "",
                "Bip1_": "Bip_",
                "Bip01_": "Bip_",
                "Bip001_": "Bip_",
                "Bip01": "",
                "Bip02_": "Bip_",
                "Character1_": "",
                "HLP_": "",
                "JD_": "",
                "JU_": "",
                "Armature|": "",
                "Bone_": "",
                "C_": "",
                "Cf_S_": "",
                "Cf_J_": "",
                "G_": "",
                "Joint_": "",
                "Def_C_": "",
                "Def_": "",
                "DEF_": "",
                "Chr_": "",
                "Chr_": "",
                "B_": "",
            },
            "ends_with": {
                "_Bone": "",
                "_Bn": "",
                "_Le": "_L",
                "_Ri": "_R",
                "_": "",
            },
            "replaces": {
                " ": "_",
                "-": "_",
                ".": "_",
                ":": "_",
                "____": "_",
                "___": "_",
                "__": "_",
                "_Le_": "_L_",
                "_l": "_L",
                "_Ri_": "_R_",
                "_r": "_R",
                "_m": "_M",
                "LEFT": "Left",
                "RIGHT": "Right",
                "all": "All",
                "finger": "Finger",
                "part": "Part",
            },
        }
    elif game == "Honkai Impact":
        return {
            "bone_names": {
                "Pelvis": "Hips",
                "LThigh": "Left leg",
                "RThigh": "Right leg",
                "LCalf": "Left knee",
                "RCalf": "Right knee",
                "LFoot": "Left ankle",
                "RFoot": "Right ankle",
                "LToe0": "Left toe",
                "RToe0": "Right toe",
                "LClavicle": "Left shoulder",
                "RClavicle": "Right shoulder",
                "LUpperArm": "Left arm",
                "RUpperArm": "Right arm",
                "LForearm": "Left elbow",
                "RForearm": "Right elbow",
                "LHand": "Left wrist",
                "RHand": "Right wrist",
                "LFinger5": "Thumb1_L",
                "LFinger51": "Thumb2_L",
                "LFinger52": "Thumb3_L",
                "LFinger1": "IndexFinger1_L",
                "LFinger11": "IndexFinger2_L",
                "LFinger12": "IndexFinger3_L",
                "LFinger2": "MiddleFinger1_L",
                "LFinger21": "MiddleFinger2_L",
                "LFinger22": "MiddleFinger3_L",
                "LFinger3": "RingFinger1_L",
                "LFinger31": "RingFinger2_L",
                "LFinger32": "RingFinger3_L",
                "LFinger4": "LittleFinger1_L",
                "LFinger41": "LittleFinger2_L",
                "LFinger42": "LittleFinger3_L",
                "RFinger5": "Thumb1_R",
                "RFinger51": "Thumb2_R",
                "RFinger52": "Thumb3_R",
                "RFinger1": "IndexFinger1_R",
                "RFinger11": "IndexFinger2_R",
                "RFinger12": "IndexFinger3_R",
                "RFinger2": "MiddleFinger1_R",
                "RFinger21": "MiddleFinger2_R",
                "RFinger22": "MiddleFinger3_R",
                "RFinger3": "RingFinger1_R",
                "RFinger31": "RingFinger2_R",
                "RFinger32": "RingFinger3_R",
                "RFinger4": "LittleFinger1_R",
                "RFinger41": "LittleFinger2_R",
                "RFinger42": "LittleFinger3_R",
            },
            "starts_with": {
                "_": "",
                "ValveBiped_": "",
                "Valvebiped_": "",
                "Bip1_": "Bip_",
                "Bip01_": "Bip_",
                "Bip001_": "Bip_",
                "Bip001": "",
                "Bip01": "",
                "Bip02_": "Bip_",
                "Character1_": "",
                "HLP_": "",
                "JD_": "",
                "JU_": "",
                "Armature|": "",
                "Bone_": "",
                "C_": "",
                "Cf_S_": "",
                "Cf_J_": "",
                "G_": "",
                "Joint_": "",
                "Def_C_": "",
                "Def_": "",
                "DEF_": "",
                "Chr_": "",
                "Chr_": "",
                "B_": "",
            },
            "ends_with": {
                "_Bone": "",
                "_Bn": "",
                "_Le": "_L",
                "_Ri": "_R",
                "_": "",
                "_End": "",
            },
            "replaces": {
                " ": "_",
                "-": "_",
                ".": "_",
                ":": "_",
                "____": "_",
                "___": "_",
                "__": "_",
                "_Le_": "_L_",
                "_l": "_L",
                "_Ri_": "_R_",
                "_r": "_R",
                "_m": "_M",
                "LEFT": "Left",
                "RIGHT": "Right",
                "all": "All",
                "finger": "Finger",
                "part": "Part",
            },
        }
    elif game == "NPC":
        return {
            "bone_names": {
                "Pelvis": "Hips",
                "LThigh": "Left leg",
                "RThigh": "Right leg",
                "LCalf": "Left knee",
                "RCalf": "Right knee",
                "LFoot": "Left ankle",
                "RFoot": "Right ankle",
                "LToe0": "Left toe",
                "RToe0": "Right toe",
                "LClavicle": "Left shoulder",
                "RClavicle": "Right shoulder",
                "LUpperArm": "Left arm",
                "RUpperArm": "Right arm",
                "LForearm": "Left elbow",
                "RForearm": "Right elbow",
                "LHand": "Left wrist",
                "RHand": "Right wrist",
                "LFinger0": "Thumb1_L",
                "LFinger01": "Thumb2_L",
                "LFinger02": "Thumb3_L",
                "LFinger1": "IndexFinger1_L",
                "LFinger11": "IndexFinger2_L",
                "LFinger12": "IndexFinger3_L",
                "LFinger2": "MiddleFinger1_L",
                "LFinger21": "MiddleFinger2_L",
                "LFinger22": "MiddleFinger3_L",
                "LFinger3": "RingFinger1_L",
                "LFinger31": "RingFinger2_L",
                "LFinger32": "RingFinger3_L",
                "LFinger4": "LittleFinger1_L",
                "LFinger41": "LittleFinger2_L",
                "LFinger42": "LittleFinger3_L",
                "RFinger0": "Thumb1_R",
                "RFinger01": "Thumb2_R",
                "RFinger02": "Thumb3_R",
                "RFinger1": "IndexFinger1_R",
                "RFinger11": "IndexFinger2_R",
                "RFinger12": "IndexFinger3_R",
                "RFinger2": "MiddleFinger1_R",
                "RFinger21": "MiddleFinger2_R",
                "RFinger22": "MiddleFinger3_R",
                "RFinger3": "RingFinger1_R",
                "RFinger31": "RingFinger2_R",
                "RFinger32": "RingFinger3_R",
                "RFinger4": "LittleFinger1_R",
                "RFinger41": "LittleFinger2_R",
                "RFinger42": "LittleFinger3_R",
                "Root_M": "Hips",
                "Hip_L": "Left leg",
                "Hip_R": "Right leg",
                "HipPart1_R": "Right leg twist R",
                "HipPart1_L": "Left leg twist L",
                "Spine1_M": "Spine",
                "Spine2_M": "Chest",
                "Chest_M": "Upper Chest",
                "Shoulder_L": "Left arm",
                "Shoulder_R": "Right arm",
                "Scapula_R": "Right shoulder",
                "Scapula_L": "Left shoulder",
                "Neck_M": "Neck",
                "Head_M": "Head",
                "face": "Face",
                "Knee_L": "Left knee",
                "Knee_R": "Right knee",
                "Ankle_L": "Left ankle",
                "Ankle_R": "Right ankle",
                "Toes_L": "Left toe",
                "Toes_R": "Right toe",
                "Elbow_L": "Left elbow",
                "Elbow_R": "Right elbow",
                "Wrist_L": "Left wrist",
                "Wrist_R": "Right wrist",
                "LFinger5": "Thumb1_L",
                "LFinger51": "Thumb2_L",
                "LFinger52": "Thumb3_L",
                "RFinger5": "Thumb1_R",
                "RFinger51": "Thumb2_R",
                "RFinger52": "Thumb3_R",
            },
            "starts_with": {
                "_": "",
                "ValveBiped_": "",
                "Valvebiped_": "",
                "Bip1_": "Bip_",
                "Bip01_": "Bip_",
                "Bip01": "",
                "Bip001": "",
                "Bip02_": "Bip_",
                "Character1_": "",
                "HLP_": "",
                "JD_": "",
                "JU_": "",
                "Armature|": "",
                "Bone_": "",
                "C_": "",
                "Cf_S_": "",
                "Cf_J_": "",
                "G_": "",
                "Joint_": "",
                "Def_C_": "",
                "Def_": "",
                "DEF_": "",
                "Chr_": "",
                "B_": "",
            },
            "ends_with": {
                "_Bone": "",
                "_Bn": "",
                "_Le": "_L",
                "_Ri": "_R",
                "_": "",
                "_End": "",
            },
            "replaces": {
                " ": "_",
                "-": "_",
                ".": "_",
                ":": "_",
                "____": "_",
                "___": "_",
                "__": "_",
                "_Le_": "_L_",
                "_l": "_L",
                "_Ri_": "_R_",
                "_r": "_R",
                "_m": "_M",
                "LEFT": "Left",
                "RIGHT": "Right",
                "all": "All",
                "finger": "Finger",
                "part": "Part",
            },
        }


def BoneExists(armature, bone_name):
    return bone_name in armature.data.edit_bones


def RenameBones(game, armature):

    game_data = GetGameData(game)

    if game_data is None:
        print("Invalid game")
        return

    armature = GetArmature()

    if game == "Honkai Impact":
        for bone in armature.pose.bones:
            bone.name = StripName(bone.name)

    if armature is not None:
        for bone in armature.pose.bones:
            bone.name = (
                re.sub(r"(?<=\w)([A-Z])", r" \1", bone.name).title().replace(" ", "")
            )

            for old, new in game_data["starts_with"].items():
                if bone.name.startswith(old):
                    bone.name = bone.name.replace(old, new, 1)
            for old, new in game_data["ends_with"].items():
                if bone.name.endswith(old):
                    bone.name = bone.name[: len(bone.name) - len(old)] + new
            for old, new in game_data["replaces"].items():
                bone.name = bone.name.replace(old, new)

            if bone.name in game_data["bone_names"]:
                bone.name = game_data["bone_names"][bone.name]

    else:
        print("Invalid game")


def CleanBones():
    # Define the bone names to remove
    bone_names = [
        "Bip001 Pelvis",
        "+EyeBone L A01",
        "+EyeBone R A01",
        "Bip002",
        "Bone_Eye_L_01",
        "Bone_Eye_R_01",
        "Skin_GRP",
        "Main",
    ]

    # Get the armature object
    armature = GetArmature()

    # Check if armature exists
    if armature is None:
        print("No armature found")
        return

    # Set the active object in the context
    bpy.context.view_layer.objects.active = armature

    # Switch to edit mode
    bpy.ops.object.mode_set(mode="EDIT")

    # Create a list of bones to remove
    bones_to_remove = [
        bone for bone in armature.data.edit_bones if bone.name in bone_names
    ]

    # Check if there are bones to remove
    if not bones_to_remove:
        print("No bones to remove found")
        return

    # Remove the bones
    for bone in bones_to_remove:
        armature.data.edit_bones.remove(bone)

    # Switch back to pose mode
    bpy.ops.object.mode_set(mode="OBJECT")


def SetHipAsParent(armature):
    if "Hips" in armature.data.edit_bones:
        hips = armature.data.edit_bones.get("Hips")
        hips.parent = None
        for bone in armature.data.edit_bones:
            if bone.parent is None:
                bone.parent = hips


def RenameSpines(armature, names):
    spines = [
        bone
        for bone in armature.data.edit_bones
        if re.match(r"spine\d*$", bone.name.lower())
    ]
    for i, spine in enumerate(spines):
        if i < len(names):
            spine.name = names[i]


def GetBones(armature, bone_names):
    return {
        name: armature.data.edit_bones.get(name)
        for name in bone_names
        if name in armature.data.edit_bones
    }


def FixHips(hips, right_leg, left_leg, spine, x_cord, y_cord, z_cord):
    # Put Hips in the center of the leg bones
    hips.head[x_cord] = (right_leg.head[x_cord] + left_leg.head[x_cord]) / 2

    # Adjust the y-coordinate of the hip bone
    hips.head[y_cord] = (right_leg.head[y_cord] + left_leg.head[y_cord]) / 2

    # Put Hips at 33% between spine and legs
    hips.head[z_cord] = (
        left_leg.head[z_cord] + (spine.head[z_cord] - left_leg.head[z_cord]) * 0.33
    )

    # If Hips are below or at the leg bones, put them above
    if hips.head[z_cord] <= right_leg.head[z_cord]:
        hips.head[z_cord] = right_leg.head[z_cord] + 0.1

    # Make Hips point straight up
    hips.tail[x_cord] = hips.head[x_cord]
    hips.tail[y_cord] = hips.head[y_cord]
    hips.tail[z_cord] = spine.head[z_cord]

    if hips.tail[z_cord] < hips.head[z_cord]:
        hips.tail[z_cord] = hips.tail[z_cord] + 0.1


def FixSpine(spine, hips, x_cord, y_cord, z_cord):
    # Fixing Spine
    spine.head[x_cord] = hips.tail[x_cord]
    spine.head[y_cord] = hips.tail[y_cord]
    spine.head[z_cord] = hips.tail[z_cord]

    # Make Spine point straight up
    spine.tail[x_cord] = spine.head[x_cord]
    spine.tail[y_cord] = spine.head[y_cord]  # Align tail with head on y-axis
    spine.tail[z_cord] = spine.head[z_cord] + 0.065


def FixChest(chest, spine, x_cord, y_cord, z_cord):
    chest.head[x_cord] = spine.tail[x_cord]
    chest.head[y_cord] = spine.tail[y_cord]
    chest.head[z_cord] = spine.tail[z_cord]

    chest.tail[x_cord] = chest.head[x_cord]
    chest.tail[y_cord] = chest.head[y_cord]
    chest.tail[z_cord] = chest.head[z_cord] + 0.065


def FixUpperChest(upperchest, chest, x_cord, y_cord, z_cord):
    upperchest.head[x_cord] = chest.tail[x_cord]
    upperchest.head[y_cord] = chest.tail[y_cord]
    upperchest.head[z_cord] = chest.tail[z_cord]

    upperchest.tail[x_cord] = upperchest.head[x_cord]
    upperchest.tail[y_cord] = upperchest.head[y_cord]
    upperchest.tail[z_cord] = upperchest.head[z_cord] + 0.1


def AdjustLegs(left_leg, right_leg, left_knee, right_knee, y_cord):
    left_leg.tail[y_cord] += -0.015
    left_knee.head[y_cord] += -0.015

    right_leg.tail[y_cord] += -0.015
    right_knee.head[y_cord] += -0.015


def StraightenHead(armature, head, x_cord, y_cord, z_cord):
    if "Head" in armature.data.edit_bones:
        head = armature.data.edit_bones.get("Head")
        head.tail[x_cord] = head.head[x_cord]
        head.tail[y_cord] = head.head[y_cord]
        if head.tail[z_cord] < head.head[z_cord]:
            head.tail[z_cord] = head.head[z_cord] + 0.1


def FixMissingNeck(armature, chest, head, x_cord, y_cord, z_cord):
    if "Neck" not in armature.data.edit_bones:
        if "Chest" in armature.data.edit_bones:
            if "Head" in armature.data.edit_bones:
                neck = armature.data.edit_bones.new("Neck")
                chest = armature.data.edit_bones.get("Chest")
                head = armature.data.edit_bones.get("Head")
                neck.head = chest.tail
                neck.tail = head.head

                if neck.head[z_cord] == neck.tail[z_cord]:
                    neck.tail[z_cord] += 0.1


def SetBoneRollToZero(armature):
    for bone in armature.data.edit_bones:
        bone.roll = 0


def attachfeets(armature, foot, toe):
    foot_bone = next(
        (bone for bone in armature.data.edit_bones if foot in bone.name), None
    )
    toe_bone = next(
        (bone for bone in armature.data.edit_bones if toe in bone.name), None
    )

    if foot_bone is None or toe_bone is None:
        print(f"Could not find bones for {foot} or {toe}")
        return

    foot_bone.tail.x = toe_bone.head.x
    foot_bone.tail.y = toe_bone.head.y
    foot_bone.tail.z = toe_bone.head.z


def attachbones(armature, bone_name1, bone_name2, exact_match=False):
    """Attach the tail of the first bone to the head of the second bone."""
    bones = armature.data.edit_bones
    if exact_match:
        bone1 = bones.get(bone_name1)
        bone2 = bones.get(bone_name2)
    else:
        bone1 = next((bone for bone in bones if bone_name1 in bone.name), None)
        bone2 = next((bone for bone in bones if bone_name2 in bone.name), None)

    if bone1 and bone2:
        bone1.tail = bone2.head
    else:
        print("Could not find matching bones.")


def attacheyes(armature, eye_bone_name, attach_to):
    if (
        eye_bone_name in armature.data.edit_bones
        and attach_to in armature.data.edit_bones
    ):
        eye_bone = armature.data.edit_bones[eye_bone_name]
        attach_to_bone = armature.data.edit_bones[attach_to]

        eye_bone.tail.x = eye_bone.head.x
        eye_bone.tail.y = eye_bone.head.y
        eye_bone.tail.z = attach_to_bone.head.z + 0.12


def MoveBone(armature, bone):
    bone.select = True
    bone.select_head = True
    bone.select_tail = True


def ContainsName(name):
    return any(name in bone.name for bone in bpy.context.object.data.bones)


def ToggleArmatureSelection(armature, select=True):
    for bone in armature.data.bones:
        bone.select = select


def MoveEyes(armature, eye_bone_name, BlenderVersion):
    if eye_bone_name not in armature.data.edit_bones:
        return

    attacheyes(armature, eye_bone_name, "Head")
    MoveBone(armature, armature.data.edit_bones[eye_bone_name])
    translate_params = {
        "value": (0, 0.025, 0),
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (True, True, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_elements": {"INCREMENT"},
        "use_snap_project": False,
        "snap_target": "CLOSEST",
        "use_snap_self": False,
        "use_snap_edit": False,
        "use_snap_nonedit": False,
        "use_snap_selectable": False,
    }
    if "LA" in eye_bone_name or "_L" in eye_bone_name:  # If it's the left eye
        translate_params["value"] = (0, 0, 0)
    if BlenderVersion < (3, 6, 2):
        translate_params["orient_axis_ortho"] = "X"
    bpy.ops.transform.translate(**translate_params)


def ReparentBone(armature, bone_name, parent_name):
    """Reparent a bone to another bone in the armature."""
    bone = armature.data.edit_bones.get(bone_name)
    parent_bone = armature.data.edit_bones.get(parent_name)
    if bone and parent_bone:
        bone.parent = parent_bone
    else:
        print(f"Could not find bone {bone_name} or parent bone {parent_name}")
