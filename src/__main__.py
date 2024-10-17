"""__main__.py"""
from PyQt5.QtWidgets import QWidget
from _lib import *
class PackButton(QToolButton):
  def __init__(self,pack:dict,parent:QWidget):
    QToolButton.__init__(self,parent)
    def on_click(a):
      print(pack["name"])
    self.clicked.connect(on_click)
    self.setIcon(pack["icon"])
    self.setIconSize(QSize(50,50))
class PackPanel(QScrollArea):
  def __init__(self,parent:QWidget):
    QScrollArea.__init__(self,parent)
    layout=QGridLayout()
    widget=QWidget()
    widget.setFixedSize(QSize(50*len(cache),50))
    widget.setLayout(layout)
    self.setFixedSize(800,50)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setWidgetResizable(True)
    self.setWidget(widget)
    column=0
    for pack_id,pack in cache.items():
      pack["icon"]=QIcon(pack["stickers"][0]["sticker"].path)
      btn=PackButton(pack,self)
      layout.addWidget(btn,0,column)
      column+=1
class MainWindow(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.setFixedSize(800,600)
    self.setWindowTitle(lang["window/title"])
    layout=QGridLayout(self)
    cw=QWidget(self)
    cw.setLayout(layout)
    self.setCentralWidget(cw)
    load_stickers()
    pack_bar=PackPanel(self)
if __name__=="__main__":
  app=QApplication(sys.argv)
  mw=MainWindow()
  mw.show()
  sys.exit(app.exec())
