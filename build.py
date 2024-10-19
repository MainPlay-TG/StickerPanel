import os
import subprocess
import sys
import shutil
from MainShortcuts2 import ms
NAME="StickerPanel"
def __main__():
  args=["pyinstaller","--onedir"]
  args+=["--name",NAME]
  args+=["--workpath",".build"]
  if ms.path.exists("icon.ico"):
    args+=["--icon","icon.ico"]
  if ms.path.exists("splash.png"):
    args+=["--splash","splash.png"]
  if sys.platform=="win32":
    args.append("--windowed")
  args.append("src/__main__.py")
  ms.path.cwd(ms.MAIN_DIR)
  ms.path.delete("dist")
  subprocess.call(args)
  for i in ms.dir.list("assets"):
    i.copy(f"dist/{NAME}/{i.full_name}")
  if sys.platform=="win32":
    shutil.make_archive(f"dist/{NAME}Windows","zip",f"dist/{NAME}")
  return 0
if __name__=="__main__":
  sys.exit(__main__())