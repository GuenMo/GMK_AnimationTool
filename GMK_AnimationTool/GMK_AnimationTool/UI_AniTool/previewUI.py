# -*- coding:utf-8 -*-

from PySide import QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken import wrapInstance
import stylesheet
reload(stylesheet)

import UI_AniTool.GMK_PreviewTab as PreviewTab
reload(PreviewTab)

__version__ = "1.3.0"

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QtGui.QWidget )

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(MainWindow, self).__init__(parent)
        self.stylData  = stylesheet.darkorange
        self.initUI()
        
    def initUI(self):
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_Layout = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.main_Layout)
        
        self.previewTab = PreviewTab.GMK_PreviewTab()
        self.main_Layout.addWidget(self.previewTab)
        
        self.setFixedWidth(250)
        self.setStyleSheet(self.stylData)
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




        
