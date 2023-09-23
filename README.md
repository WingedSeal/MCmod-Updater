# MCmod-Updater
Manager for your Minecraft mods from Github

Create `mcmu.txt` next to `mcmu.py` with contents being
```txt
PATH_TO_MOD_FOLDER
pre GITHUB_URL
pre GITHUB_URL
pre GITHUB_URL
url CUSTOM_URL
url CUSTOM_URL
url CUSTOM_URL
GITHUB_URL
GITHUB_URL
GITHUB_URL
neu
```

`pre` is for downloading pre release of the mod

`neu` is customized for [NEU](https://github.com/Moulberry/NotEnoughUpdates/releases), popular Hypixel Skyblock mod, since they do not release their mod on Github

## Example
```txt
C:\Users\User\AppData\Roaming\.minecraft\mods
pre https://github.com/symt/BazaarNotifier
pre https://github.com/Quantizr/DungeonRoomsMod
pre https://github.com/BiscuitDevelopment/SkyblockAddons
pre https://github.com/Skytils/SkytilsMod
pre https://github.com/Soopyboo32/SoopyV2Forge
pre https://github.com/hannibal002/SkyHanni
neu
```

## Download Link: 
https://github.com/WingedSeal/MCmod-Updater/releases/download/v0.1.0/mcmu.py

## Note:
This program requires `requests` python library

```
pip install requests
```
