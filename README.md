<br>
<p align="center">
    <a href="https://github.com/Melioli/Hoyo2VRC"><img src="https://melioli.moe/yej7m.png" alt="Hoyo2VRC"/></a>
</p><br>

<p align="center">
    <a href="https://github.com/Melioli/Hoyo2VRC/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/badge/License-GPL--3.0-702963?style=for-the-badge"></a><br>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Melioli/Hoyo2VRC?style=for-the-badge"
"></a>
    <img alt="Discord" src="https://img.shields.io/discord/1129811149416824934?style=for-the-badge"
"></a>
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Melioli/Hoyo2VRC?style=for-the-badge"
"></a>
</p>


---

## Important Information
> [!WARNING]
> * This Addon is made for Blender 3.3.0 and above. It may not work with older versions of Blender.
> * This Addon is only for Hoyoverse datamined assets. MMD or other sources will not work properly with this Addon. However, we do not condone datamining and encourage users to respect the intellectual property rights of the original creators.
> * The Addon comes with a custom BetterFBX and CATS fork. If you have either of these addons installed, please disable them before using Hoyo2VRC.
> Only the following models are supported:
> - Playable Characters from Genshin Impact, Honkai Impact and Honkai Star Rail
> - NPC/Monsters from Genshin Impact, Honkai Impact and Honkai Star Rail

The models will have to come from the game files. as their naming scheme are important for the addon to work properly. The naming schemes are as follows:

| Genshin Impact | Honkai Impact | Honkai Star Rail |
| :-----: | :--: | :--------------------: | 
| Avatar_Boy_Sword_Bennet |  Avatar_Fuka_C1  | Avatar_Arlan_00 |
| Cs_Avatar_Lady_Claymore_Dehya | Avatar_Seele_C3 | Art_DanHengIL_00 |
| NPC_Avatar_Lady_Bow_Ganyu | Avatar_Kiana_C6_MH | NPC_Avatar_Lady_Kafka_00 |
| Avatar_Loli_Catalyst_Klee | Avatar_Fuka_C1 | Avatar_Maid_Seele_00|
| Avatar_Pole_Zhongli | Avatar_Elysia_C1_GS | Art_Avatar_Kid_Bailu_25 |


## Features
> [!IMPORTANT]
> * Built-in support for [HoyoToon](https://github.com/Melioli/HoyoToon). Your models will always be in the perfect state for use with [HoyoToon](https://github.com/Melioli/HoyoToon).
> * Automatic conversion from raw datamined assets to VRChat avatars.
> * Applying lots of fixes that would save you around 20 minutes of work in simple seconds.
> * All the features of BetterFBX and CATS, but with a custom fork that is optimized for use with Hoyo2VRC.
> * Correct Importing of the models with the perfect settings that you'd have to set yourself in BetterFBX normally.
> * The current fixes and features that the Convert buttons do are as follows:

| Convert HSR Avatar | Convert GI Avatar | Convert HI3 Avatar | Convert NPC |
| :-----: | :--: | :--------------------: | :--------------------: |
| Scale model to correct size | Scale model to correct size | Scale model to correct size | Scale model to correct size |
| Remove all Empties | Remove all Empties | Remove all Empties | Remove all Empties |
| Clear unwanted rotations| Clear unwanted rotations| Clear unwanted rotations| Clear unwanted rotations|
| Remove unused meshes | Remove unused meshes | Remove unused meshes | Remove unused meshes |
| Remove zero weight bones | Remove zero weight bones | Remove zero weight bones | Remove zero weight bones |
| Merge Meshes | Merge Meshes | Merge Meshes | Merge Meshes |
| Reset to A pose | Reset to A pose | Reset to A pose | Reset to A pose |
| Fix Hips, Chest and Spine bones | Fix Hips, Chest and Spine bones | Fix Hips, Chest and Spine bones | Fix Hips, Chest and Spine bones |
| Remove Rolls of important humanoid bones | Remove Rolls of important humanoid bones | Remove Rolls of important humanoid bones | Remove Rolls of important humanoid bones |
| Apply Transforms | Apply Transforms | Apply Transforms | Apply Transforms |
| Reposition Eyes for VRChat EyeTracking | Reposition Eyes for VRChat EyeTracking | Reposition Eyes for VRChat EyeTracking | Reposition Eyes for VRChat EyeTracking |
| Mass Rename Bones | Generate VRC Shapekeys from GI model | Rename Eye Bones |  |
| Generate Shapekeys from Facerig (*If imported with face animations*) | | | |


## Installation
> [!IMPORTANT]
> You can download the addon from the [Releases](https://github.com/Melioli/Hoyo2VRC/releases) page. Please do not download the source code unless you know what you are doing. 
> After downloading the addon, you can install it by following the steps >below:
> 1. Open Blender and go to `Edit > Preferences > Add-ons`.
> 2. Click on the `Install` button at the top right of the window.
> 3. Navigate to the folder where you downloaded the addon and select the `Hoyo2VRC.zip` file.
> 4. Click on the `Install Add-on` button at the bottom right of the window.
> 5. Enable the addon by clicking on the checkbox next to it.

## Usage
> [!IMPORTANT]
> You can find the Hoyo2VRC panel on the side panel of the 3D Viewport. If you can't see it, press `N` to open it.
> On the first run, You'll want to press the Install Dependancies button which is located under the settings tabs. This will install the required dependencies for the addon to work properly. 
> After that, you can use the addon by following the steps below:
> 1. Click on the `Import Model` button.
> 2. Navigate to the folder where you downloaded the model and select the `FBX` file that matches the naming scheme shown above.
> 3. Click on the `Better FBX Import` button.
> 4. Once it's imported in the scene select the armature object in the Outliner. ![icon](https://github.com/Melioli/Hoyo2VRC/assets/31974197/f7773a92-b168-4d34-9513-22306a7f2838)
>
> 5. If the correct models are imported it'll show an additonal button that can either be Convert HSR Avatar ![hsr](https://github.com/Melioli/Hoyo2VRC/assets/31974197/13f7d791-c5e2-479d-b8de-eedce3be0e5d), Convert GI Avatar ![GI](https://github.com/Melioli/Hoyo2VRC/assets/31974197/18701bd5-cad0-4b11-b126-b6c9a680c258) or Convert HI3 Avatar ![hi3](https://github.com/Melioli/Hoyo2VRC/assets/31974197/ff2c6e95-a54d-4d79-8aa5-6bc827f16b57). Otherwise it'll say Convert NPC. ![npc](https://github.com/Melioli/Hoyo2VRC/assets/31974197/6c77ae80-2c98-4856-a001-77b028498a6c)
>
> 7. Click on the button that matches the model you imported.
> 8. Once it's done, you can export the model by clicking on the `Export Model` button.

## Contact
- [Discord server](https://discord.gg/meliverse)
- [Meliodas's Twitter](https://twitter.com/Meliodas7DL)

## Issues
- If you encounter any issues while using Hoyo2VRC, please don't hesitate to reach out to me. You can contact me directly on Discord, or you can [create an issue](https://github.com/Melioli/Hoyo2VRC/issues/new/choose) on my GitHub repository. I am always happy to help and will do my best to resolve any problems you may have.

## Rules
- The [GPL-3.0 License](https://github.com/Melioli/Hoyo2VRC/blob/main/LICENSE) applies.
- In compliance with the license, you are free to redistribute the files as long as you attach a link to the source repository.
- You are not allowed to sell the files or any derivative works.


## Contributing
I welcome contributions to the Hoyo2VRC project! If you notice any issues or have ideas for new features, please feel free to create a pull request. I appreciate any help I can get, and I will do my best to review and merge your contributions as soon as possible.

## Special thanks and Credits
All of this wouldn't be possible if it weren't for:
- [Meliodas](https://github.com/Melioli)
- [Mken](https://github.com/michael-gh1)

