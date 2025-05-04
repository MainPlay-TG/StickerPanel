"""_lib.py"""
import gc
import natsort
import sys
from hashlib import sha256
from MainPlaySoft import MPSoft
from MainPlaySoft.lang import texts as LANG_TEXTS
from MainShortcuts2 import ms
from PIL import Image
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from traceback import print_exc
cache={}
mps=MPSoft("MainPlay TG","StickerPanel")
cfg=ms.cfg(mps.dir.data+"/cfg.json",type="json")
# cfg.default["sticker.format"]="WEBP"
cfg.default["lang.code"]="ru"
cfg.default["sticker.size"]=[512,512]
cfg.default["stickers.dir"]=mps.dir.data+"/stickers"
cfg.dload(True)
LANG_DEFAULT={"window/title":"StickerPanel от MainPlay TG","init/lang_not_found":"Предупреждение: языковой файл не найден"}
for k,v in LANG_DEFAULT.items():
  LANG_TEXTS["ru"][k]=v
lang=mps.lang
lang.code=cfg["lang.code"]
TARGET_EXT=".png"
#TARGET_EXT="."+cfg["sticker.format"].lower()
TARGET_SIZE=cfg["sticker.size"][0],cfg["sticker.size"][1]
if ms.path.exists(ms.MAIN_DIR+"/lang/"+lang.code+".json"):
  for k,v in ms.json.read(ms.MAIN_DIR+"/lang/"+lang.code+".json").items():
    lang[k]=v
else:
  print(lang["init/lang_not_found"],file=sys.stderr)
def log(text:str,*values,**kw):
  kw.setdefault("file",sys.stderr)
  if len(values)==0:
    return print(text,**kw)
  if len(values)==1:
    values=values[0]
  print(text%values,**kw)
def resize_img(img:Image.Image)->Image.Image:
  if img.size==TARGET_SIZE:
    return img
  if img.size[0]==img.size[1]:
    return img.resize(TARGET_SIZE)
  size,pos=None,None
  if img.size[0]>img.size[1]:
    size=TARGET_SIZE[0],int(TARGET_SIZE[1]*(img.size[1]/img.size[0]))
    pos=0,int((TARGET_SIZE[1]-size[1])/2)
  if img.size[0]<img.size[1]:
    size=int(TARGET_SIZE[0]*(img.size[0]/img.size[1])),TARGET_SIZE[1]
    pos=int((TARGET_SIZE[0]-size[0])/2),0
  nimg=Image.new("RGBA",TARGET_SIZE,(0,0,0,0))
  nimg.paste(img.resize(size),pos)
  return nimg
def load_stickers():
  cache.clear()
  dir=cfg["stickers.dir"]
  tmp_dir=mps.dir.localdata+"/sticker_cache/{}x{}".format(*TARGET_SIZE)
  ms.dir.create(dir)
  ms.dir.create(tmp_dir)
  for pack in ms.dir.list_iter(dir,type="dir"):
    stickers=[]
    for sticker in ms.dir.list_iter(pack,exts=Image.registered_extensions().keys(),type="file"):
      sticker_name=pack.full_name+"/"+sticker.full_name
      try:
        item={}
        item["path"]=sticker
        hash=sha256()
        with open(sticker.path,"rb") as f:
          for chunk in f:
            hash.update(chunk)
        item["sha256"]=hash.digest()
        item["sticker"]=ms.path.Path(tmp_dir+"/"+hash.hexdigest()+TARGET_EXT)
        if not ms.path.exists(item["sticker"]):
          log('Caching "%s"',sticker_name)
          with Image.open(sticker.path) as img:
            with resize_img(img) as nimg:
              nimg.save(item["sticker"].path,compress_level=0)
        stickers.append(item)
      except Exception as err:
        log('Error on loading "%s"',sticker_name)
        print_exc()
    if len(stickers)>0:
      cache[pack.full_name]={}
      cache[pack.full_name]["name"]=pack.full_name
      cache[pack.full_name]["path"]=pack
      cache[pack.full_name]["stickers"]=natsort.os_sorted(stickers,key=lambda i:i["path"].base_name)
      cache[pack.full_name]["url"]=None
      if ms.path.exists(pack.path+"/info.json"):
        info=ms.json.read(pack.path+"/info.json")
        if "name" in info:
          cache[pack.full_name]["name"]=info["name"]
        if "title" in info:
          cache[pack.full_name]["name"]=info["title"]
        if "url" in info:
          cache[pack.full_name]["url"]=info["url"]
