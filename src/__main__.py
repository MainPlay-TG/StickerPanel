import gc
from _lib import *
from PyQt6.QtWidgets import QWidget
from traceback import print_exc
MAIN_WIN_SIZE=QSize(800,600)
PACK_BTN_SIZE=QSize(50,50)
STICKER_SIZE=QSize(100,100)
STICKERS_IN_ROW=MAIN_WIN_SIZE.width()//STICKER_SIZE.width()
class StickerButton(QPushButton):
  def __init__(self,sticker:Sticker,parent:QWidget):
    QPushButton.__init__(self,parent)
    self.setFixedSize(STICKER_SIZE)
    self.setIcon(sticker.get_qicon(STICKER_SIZE))
    self.setIconSize(STICKER_SIZE)
    self.sticker=sticker
  def mousePressEvent(self,event:QMouseEvent):
    if event.button()==Qt.MouseButton.RightButton:
      cb=QApplication.clipboard()
      cb.setImage(self.sticker.get_qimage(TARGET_SIZE))
  def mouseMoveEvent(self,event:QMouseEvent):
    drag=QDrag(self)
    img=self.sticker.get_qimage(TARGET_SIZE)
    mime=QMimeData()
    mime.setImageData(img)
    drag.setMimeData(mime)
    drag.exec(Qt.DropAction.CopyAction)
class PackButton(QPushButton):
  STICKER_PANEL:QScrollArea=None
  def __init__(self,pack:Pack,parent:QWidget):
    QPushButton.__init__(self,parent)
    def on_click(a0):
      STICKER_PANEL:StickerPanel=self.STICKER_PANEL
      if pack.name==STICKER_PANEL.current:
        return
      STICKER_PANEL.current=pack.name
      layout=QGridLayout()
      layout.setContentsMargins(0,0,0,0)
      layout.setSpacing(0)
      panel=QWidget()
      size_x,size_y=STICKERS_IN_ROW,len(pack.stickers)//STICKERS_IN_ROW
      if len(pack.stickers)%STICKERS_IN_ROW>0:
        size_y+=1
      panel.setFixedHeight(STICKER_SIZE.height()*size_y)
      panel.setFixedWidth(STICKER_SIZE.width()*size_x)
      panel.setLayout(layout)
      x,y=0,0
      for sticker in pack.stickers:
        try:
          btn=StickerButton(sticker,panel)
        except Exception:
          log("Failed to create StickerButton for sticker %s",sticker)
          print_exc()
          continue
        if x==size_x:
          x=0
          y+=1
        layout.addWidget(btn,y,x)
        x+=1
      STICKER_PANEL.setWidget(panel)
      gc.collect()
    self.clicked.connect(on_click)
    self.setFixedSize(PACK_BTN_SIZE)
    self.setIconSize(PACK_BTN_SIZE)
    self.setIcon(pack.icon.get_qicon(PACK_BTN_SIZE))
class PackPanel(QScrollArea):
  def __init__(self,packs:list[Pack],parent:QWidget):
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
    widget.setFixedSize(QSize(PACK_BTN_SIZE.width()*len(packs),PACK_BTN_SIZE.height()))
    widget.setLayout(layout)
    column=0
    for pack in packs:
      try:
        btn=PackButton(pack,self)
      except Exception:
        log("Failed to create PackButton for pack %s",pack)
        print_exc()
        continue
      layout.addWidget(btn,0,column)
      column+=1
class StickerPanel(QScrollArea):
  current=""
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
    self.setWindowTitle("StickerPanel от MainPlay TG")
    sticker_panel=StickerPanel(self)
    PackButton.STICKER_PANEL=sticker_panel
    layout.addWidget(PackPanel(load_stickers(cfg["stickers.dir"]),self),0,0)
    layout.addWidget(sticker_panel,1,0)
    self.show()
@ms.utils.main_func(__name__)
def main():
  app=QApplication(sys.argv)
  mw=MainWindow()
  return app.exec()
