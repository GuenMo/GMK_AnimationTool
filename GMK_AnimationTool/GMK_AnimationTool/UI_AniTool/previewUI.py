# -*- coding:utf-8 -*-

try:
    import PySide
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except:
    import PySide2
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance


import maya.OpenMayaUI as OpenMayaUI

import GMK_PreviewTab as PreviewTab
reload(PreviewTab)

__version__ = "1.3.0"

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QWidget )

class MainWindow(QMainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_Layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_Layout)
        
        self.previewTab = PreviewTab.GMK_PreviewTab()
        self.main_Layout.addWidget(self.previewTab)
        
        self.setFixedWidth(250)
        self.setWindowTitle("Preview Tool Window")
         
def main():
    global win
    
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    
    win = MainWindow()
    win.show()

main()


        
