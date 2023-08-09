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
```

`pre` is for downloading full release of the mod

## Example
```txt
C:\Users\User\AppData\Roaming\.minecraft\mods
pre https://github.com/symt/BazaarNotifier
pre https://github.com/Quantizr/DungeonRoomsMod
pre https://github.com/BiscuitDevelopment/SkyblockAddons
pre https://github.com/Skytils/SkytilsMod
pre https://github.com/Soopyboo32/SoopyV2Forge
pre https://github.com/hannibal002/SkyHanni
url https://cdn.discordapp.com/attachments/952944284150149151/1137619027791974430/SkyblockExtras-2.2.0-pre16-RELEASE.jar
url https://cdn.discordapp.com/attachments/1028896920346841118/1134499760989020332/NotEnoughUpdates-2.1.1-Alpha-19.jar
```