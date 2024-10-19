from MainPlaySoft import MPSoft
from MainShortcuts2 import ms
mps=MPSoft("MainPlay TG","StickerPanel")
cfg=ms.cfg(mps.dir.data+"/cfg.json",type="json")
cfg.default["stickers.dir"]=mps.dir.data+"/stickers"
cfg.dload(True)
ms.dir.create(cfg["stickers.dir"])
print(cfg["stickers.dir"])