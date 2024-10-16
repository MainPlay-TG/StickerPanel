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
    pack_bar=QToolBar(self)
    pack_bar.setFixedSize(800,50)
    pack_bar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
    pack_bar.setMovable(False)
    pack_bar.setIconSize(QSize(50,50))
    for pack_id,pack in cache.items():
      pack["icon"]=QIcon(pack["stickers"][0]["sticker"].path)
      btn=PackButton(pack,pack_bar)
      pack_bar.addWidget(btn)
if __name__=="__main__":
  app=QApplication(sys.argv)
  mw=MainWindow()
  mw.show()
  sys.exit(app.exec())