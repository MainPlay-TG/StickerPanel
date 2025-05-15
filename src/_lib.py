import sys
from hashlib import sha256
from MainPlaySoft import MPSoft
from MainShortcuts2 import ms
from PIL import Image
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
try:
  import natsort
except Exception:
  natsort=None
mps=MPSoft("MainPlay TG","StickerPanel")
cfg=ms.cfg(mps.dir.data+"/cfg.json",type="json")
cfg.default["sticker.size"]=[512,512]
cfg.default["stickers.blacklisted"]=[]
cfg.default["stickers.dir"]=mps.dir.data+"/stickers"
cfg.dload(True)
CACHE_DIR=mps.dir.localdata+"/sticker_cache/"
TARGET_SIZE=cfg["sticker.size"][0],cfg["sticker.size"][1]
def log(text:str,*values,**kw):
  kw.setdefault("file",sys.stderr)
  if len(values)==0:
    return print(text,**kw)
  if len(values)==1:
    values=values[0]
  print(text%values,**kw)
def resize_img(img:Image.Image,size:tuple[int,int],**kw)->Image.Image:
  if img.size==size:
    return img
  if img.size[0]==img.size[1]:
    kw["size"]=size
    return img.resize(**kw)
  nimg=Image.new("RGBA",size,(0,0,0,0))
  pos=None
  if img.size[0]>img.size[1]:
    kw["size"]=size[0],int(size[1]*(img.size[1]/img.size[0]))
    pos=0,int((size[1]-kw["size"][1])/2)
  if img.size[0]<img.size[1]:
    kw["size"]=int(size[0]*(img.size[0]/img.size[1])),size[1]
    pos=int((size[0]-kw["size"][0])/2),0
  nimg.paste(img.resize(**kw),pos)
  return nimg
def os_sorted(paths,**kw):
  kw.setdefault("key",lambda i:i.full_name)
  if natsort is None:
    return sorted(paths,**kw)
  return natsort.os_sorted(paths,**kw)
class Pack:
  def __init__(self,dir:str):
    self.dir=ms.path.Path(dir)
    self.name=self.dir.full_name
    self.stickers:list[Sticker]=[]
    self.url:None=None
    if ms.path.exists(self.dir.path+"/info.json"):
      info=ms.json.read(self.dir.path+"/info.json")
      if info.get("name"):
        self.name=info["name"]
      if info.get("title"):
        self.name=info["title"]
      if info.get("url"):
        self.url:str=info["url"]
    for file in os_sorted(ms.dir.list_iter(self.dir,exts=list(Image.registered_extensions()),type="file")):
      sticker=Sticker(self,file)
      self.stickers.append(sticker)
  def __bool__(self):
    return len(self.stickers)>0
  def __str__(self):
    return self.name
  @property
  def icon(self):
    return self.stickers[0]
class Sticker:
  def __init__(self,pack:Pack,file:str):
    self._sha256=None
    self.file=ms.path.Path(file)
    self.name=self.file.base_name
    self.pack=pack
  def __str__(self):
    return "%s/%s"%(self.pack.name,self.name)
  @property
  def sha256(self)->str:
    if self._sha256 is None:
      with open(self.file,"rb") as f:
        hash=sha256()
        for i in f:
          hash.update(i)
      self._sha256=hash.hexdigest()
    return self._sha256
  def get_cache(self,size:tuple[int,int]|QSize):
    if isinstance(size,QSize):
      size=size.width(),size.height()
    path=CACHE_DIR+"%s_%sx%s.png"%(self.sha256,*size)
    if not ms.path.exists(path):
      log("Caching %s for size %sx%s",self,*size)
      with Image.open(self.file.path) as img:
        resize_img(img,size).save(path,"PNG",compress_level=0)
    return path
  def get_qicon(self,size):
    return QIcon(self.get_cache(size))
  def get_qimage(self,size):
    return QImage(self.get_cache(size))
  def get_qpixmap(self,size):
    return QPixmap(self.get_cache(size))
def load_stickers(dir:str)->list[Pack]:
  dir=ms.path.Path(dir)
  ms.dir.create(CACHE_DIR)
  ms.dir.create(dir)
  packs=[]
  for pack_dir in os_sorted(ms.dir.list_iter(dir,type="dir")):
    pack=Pack(pack_dir)
    if pack:
      packs.append(pack)
  return packs
for dir in ms.dir.list_iter(CACHE_DIR,type="dir"):
  log("Deleting old cache dir: %s",dir.full_name)
  ms.dir.delete(dir)