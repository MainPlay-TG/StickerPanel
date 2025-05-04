import os
import shutil
import subprocess
import sys
from MainPlaySoft import MPSoft
from MainShortcuts2 import ms
mps=MPSoft("MainPlay TG","StickerPanel")
cfg=ms.cfg(mps.dir.data+"/cfg.json",type="json")
cfg.default["stickers.dir"]=mps.dir.data+"/stickers"
cfg.dload(True)
ms.dir.create(cfg["stickers.dir"])
print(cfg["stickers.dir"])
if "--open" in sys.argv:
  dir=os.path.realpath(cfg["stickers.dir"])
  if sys.platform=="win32":
    subprocess.call(["explorer.exe",dir.replace("/","\\")])
  elif shutil.which("thunar"):
    subprocess.call(["thunar",dir])
  else:
    print("Failed to find a compatible file manager to open the folder",file=sys.stderr)