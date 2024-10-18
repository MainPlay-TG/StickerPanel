"""__main__.py"""
from PyQt5.QtWidgets import QWidget
from _lib import *
ICONS={}
MAIN_WIN_SIZE=QSize(800,600)
PACK_BTN_SIZE=QSize(50,50)
STICKER_SIZE=QSize(100,100)
STICKERS_IN_ROW=MAIN_WIN_SIZE.width()//STICKER_SIZE.width()
class StickerButton(QPushButton):
  def __init__(self,sticker:dict,parent:QWidget):
    QPushButton.__init__(self,parent)
    imgpath=sticker["sticker"].path
    self.setFixedSize(STICKER_SIZE)
    self.setIconSize(STICKER_SIZE)
    if not imgpath in ICONS:
      ICONS[imgpath]=QIcon(imgpath)
    self.setIcon(ICONS[imgpath])
class PackButton(QPushButton):
  STICKER_PANEL:QScrollArea=None
  def __init__(self,pack_id:str,pack:dict,parent:QWidget):
    QPushButton.__init__(self,parent)
    def on_click(a0):
      print(pack_id)
      STICKER_PANEL:QScrollArea=self.STICKER_PANEL
      layout=QGridLayout()
      layout.setContentsMargins(0,0,0,0)
      layout.setSpacing(0)
      panel=QWidget()
      size_x,size_y=STICKERS_IN_ROW,len(pack["stickers"])//STICKERS_IN_ROW
      if len(pack["stickers"])%STICKERS_IN_ROW>0:
        size_y+=1
      panel.setFixedHeight(STICKER_SIZE.height()*size_y)
      panel.setFixedWidth(STICKER_SIZE.width()*size_x)
      panel.setLayout(layout)
      x,y=0,0
      for i in pack["stickers"]:
        if x==size_x:
          x=0
          y+=1
        btn=StickerButton(i,panel)
        layout.addWidget(btn,y,x)
        x+=1
      STICKER_PANEL.setWidget(panel)
    self.clicked.connect(on_click)
    self.setFixedSize(PACK_BTN_SIZE)
    self.setIcon(pack["icon"])
    self.setIconSize(PACK_BTN_SIZE)
class PackPanel(QScrollArea):
  def __init__(self,parent:QWidget):
    QScrollArea.__init__(self,parent)
    layout=QGridLayout()
    scroll_bar=QScrollBar(Qt.Orientation.Horizontal,self)
    widget=QWidget()
    layout.setContentsMargins(0,0,0,0)
    layout.setSpacing(0)
    self.setFixedSize(MAIN_WIN_SIZE.width(),PACK_BTN_SIZE.height()+scroll_bar.size().height())
    self.setHorizontalScrollBar(scroll_bar)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setWidget(widget)
    self.setWidgetResizable(True)
    widget.setFixedSize(QSize(PACK_BTN_SIZE.width()*len(cache),PACK_BTN_SIZE.height()))
    widget.setLayout(layout)
    column=0
    for pack_id,pack in natsort.os_sorted(cache.items(),key=lambda i:i[0]):
      pack["icon"]=QIcon(pack["stickers"][0]["sticker"].path)
      btn=PackButton(pack_id,pack,self)
      layout.addWidget(btn,0,column)
      column+=1
class StickerPanel(QScrollArea):
  def __init__(self,parent:QWidget):
    QScrollArea.__init__(self,parent)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.setWidgetResizable(True)
class MainWindow(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    layout=QGridLayout(self)
    layout.setContentsMargins(0,0,0,0)
    layout.setSpacing(0)
    cw=QWidget(self)
    cw.setLayout(layout)
    self.setCentralWidget(cw)
    self.setFixedSize(MAIN_WIN_SIZE)
    self.setWindowTitle(lang["window/title"])
    load_stickers()
    pack_bar=PackPanel(self)
    sticker_panel=StickerPanel(self)
    PackButton.STICKER_PANEL=sticker_panel
    layout.addWidget(pack_bar,0,0)
    layout.addWidget(sticker_panel,1,0)
def __main__():
  app=QApplication(sys.argv)
  mw=MainWindow()
  mw.show()
  return app.exec()
if __name__=="__main__":
  sys.exit(__main__())
