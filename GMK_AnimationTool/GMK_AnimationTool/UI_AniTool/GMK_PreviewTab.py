# -*- coding:utf-8 -*-
from PySide.QtCore import * 
from PySide.QtGui import *
import os
import subprocess

import Core_AniTool.GMK_AniTool_Utils as utils
reload(utils)
import Core_AniTool.GMK_HUD as HUD
reload(HUD)
import Core_AniTool.GMK_Preview as Preview
reload(Preview)


class GMK_PreviewTab(QWidget):
    def __init__(self, parent=None):
        super(GMK_PreviewTab, self).__init__(parent)
        self.initUI()
        self.connectSignals()
        self.setHUDLabelColor(17)
        self.setHUDFondColor(16)
        #self.setTimeUnit("NTSC(30 fps)")
        
    def initUI(self):
        # Create Widget
        self.main_Layout = QVBoxLayout()
        self.setLayout(self.main_Layout)
        
        # HUD
        self.hud_GroupBox = QGroupBox('HUD')
        self.hud_Layout = QVBoxLayout()
        self.hud_GroupBox.setLayout(self.hud_Layout)
        
        self.color_Layout = QGridLayout()
        self.labelColor_Label = QLabel('Label color')
        self.labelColor_Label.setFixedWidth(62)
        self.labelColor_Slider = QSlider(Qt.Horizontal)
        self.labelColor_Slider.setRange(1,23)
        self.labelColor_Slider.setValue(17)
        self.labelColorView_Label = QLabel()
        self.labelColorView_Label.setFixedSize(20,12)
        self.fontColor_Label = QLabel('Font color')
        self.fontColor_Slider = QSlider(Qt.Horizontal)
        self.fontColor_Slider.setRange(1,23)
        self.fontColor_Slider.setValue(16)
        self.fontColorView_Label = QLabel()
        self.fontColorView_Label.setFixedSize(20,12)
        self.color_Layout.addWidget(self.labelColor_Label,      0,0)
        self.color_Layout.addWidget(self.labelColor_Slider,     0,1)
        self.color_Layout.addWidget(self.labelColorView_Label,  0,2)
        self.color_Layout.addWidget(self.fontColor_Label,       1,0)
        self.color_Layout.addWidget(self.fontColor_Slider,      1,1)
        self.color_Layout.addWidget(self.fontColorView_Label,   1,2)
        
        self.name_Layout = QHBoxLayout()
        self.name_Label = QLabel('Artist Name:')
        self.name_Text = QLineEdit()
        self.name_Layout.addWidget(self.name_Label)
        self.name_Layout.addWidget(self.name_Text)
        
        self.hudButtons_Layout = QHBoxLayout()
        self.on_Button = QPushButton('On')
        self.off_Button = QPushButton('Off')
        self.hudButtons_Layout.addWidget(self.on_Button)
        self.hudButtons_Layout.addWidget(self.off_Button)
        
        self.hud_Layout.addLayout(self.color_Layout)
        self.hud_Layout.addLayout(self.name_Layout)
        self.hud_Layout.addLayout(self.hudButtons_Layout)
        

        # Preview
        self.preview_GroupBox = QGroupBox('Playblast')
        self.preview_Layout = QGridLayout()
        self.preview_GroupBox.setLayout(self.preview_Layout)
        
        self.timeUnit_Label = QLabel('Time')
        self.timeUnit_ComboBox = QComboBox()
        self.timeUnit_ComboBox.addItem("Film(24 fps)")
        self.timeUnit_ComboBox.addItem("PAL(25 fps)")
        self.timeUnit_ComboBox.addItem("NTSC(30 fps)")
        self.timeUnit_ComboBox.addItem("Game(15 fps)")
        self.timeUnit_ComboBox.setCurrentIndex(0)
        
        self.safeAction_CheckBox = QCheckBox('Safe Action')
        self.resolution_CheckBox = QCheckBox('Resolution Gate')
        
        self.size_Layout = QHBoxLayout()
        self.width_Label = QLabel('Width:')
        self.width_Text = QLineEdit()
        self.width_Text.setText('960')
        self.width_Text.setValidator(QIntValidator(1,10000))
        self.height_Label = QLabel('Height:')
        self.height_Text = QLineEdit()
        self.height_Text.setText('540')
        self.height_Text.setValidator(QIntValidator(1,10000))
        self.size_Layout.addWidget(self.width_Label)
        self.size_Layout.addWidget(self.width_Text)
        self.size_Layout.addWidget(self.height_Label)
        self.size_Layout.addWidget(self.height_Text)
        
        self.scale_Layout = QHBoxLayout()
        self.scale_Label = QLabel('Scale:')
        self.scale_Label.setFixedWidth(32)
        self.scale_Text = QLineEdit()
        self.scale_Text.setFixedWidth(50)
        self.scale_Text.setText('1.00')
        self.scale_Slider = QSlider(Qt.Horizontal)
        self.scale_Slider.setRange(10,100)
        self.scale_Slider.setValue(50)
        self.scale_Layout.addWidget(self.scale_Label)
        self.scale_Layout.addWidget(self.scale_Text)
        self.scale_Layout.addWidget(self.scale_Slider)
        
        self.previewButtons_Layout = QHBoxLayout()
        self.make_Button = QPushButton('Preview')
        self.open_Button = QPushButton('Folder')
        self.previewButtons_Layout.addWidget(self.make_Button)
        self.previewButtons_Layout.addWidget(self.open_Button)
        
        self.preview_Layout.addWidget(self.timeUnit_Label, 0,0, 1,1)
        self.preview_Layout.addWidget(self.timeUnit_ComboBox, 0,1, 1,3)
        self.preview_Layout.addWidget(self.safeAction_CheckBox, 1,0, 1,4)
        self.preview_Layout.addWidget(self.resolution_CheckBox, 2,0, 1,4)
        self.preview_Layout.addLayout(self.size_Layout, 3,0, 1,4)
        self.preview_Layout.addLayout(self.scale_Layout, 4,0, 1,4)
        self.preview_Layout.addLayout(self.previewButtons_Layout, 5,0, 1,4)
        
        # Set Layout
        self.main_Layout.addWidget(self.hud_GroupBox)
        self.main_Layout.addWidget(self.preview_GroupBox)
        #self.main_Layout.addStretch()

        # Set Widget
        self.setWindowTitle("Preview Tab")
        
    def connectSignals(self):
        self.labelColor_Slider.valueChanged[int].connect(self.setHUDLabelColor)
        self.fontColor_Slider.valueChanged[int].connect(self.setHUDFondColor)
        self.on_Button.clicked.connect(self.onHUD)
        self.off_Button.clicked.connect(self.offHUD)
        
        self.timeUnit_ComboBox.activated[str].connect(self.setTimeUnit)
        self.safeAction_CheckBox.stateChanged.connect(self.setSafeAction)
        self.resolution_CheckBox.stateChanged.connect(self.setResolutionGate)
        self.scale_Slider.valueChanged[int].connect(self.setScaleText)
        self.scale_Text.editingFinished.connect(self.setScaleValue)
        self.make_Button.clicked.connect(self.makePreview)
        self.open_Button.clicked.connect(self.openFolder)
        
    def intToQColor(self, colorId):
        
        if colorId == 1: return QColor(0, 0, 0)
        if colorId == 2: return QColor(64, 64, 64)
        if colorId == 3: return QColor(128, 128, 128)
        if colorId == 4: return QColor(155, 0, 40)
        if colorId == 5: return QColor(0, 4, 96)
        if colorId == 6: return QColor(0, 0, 255)
        if colorId == 7: return QColor(0, 70, 25)
        if colorId == 8: return QColor(38, 0, 67)
        if colorId == 9: return QColor(200, 0, 200)
        if colorId == 10:return QColor(138, 72, 51)
        if colorId == 11:return QColor(63, 35, 31)
        if colorId == 12:return QColor(153, 38, 0)
        if colorId == 13:return QColor(255, 0, 0)
        if colorId == 14:return QColor(0, 255, 0)
        if colorId == 15:return QColor(0, 65, 153)
        if colorId == 16:return QColor(255, 255, 255)
        if colorId == 17:return QColor(255, 255, 0)
        if colorId == 18:return QColor(100, 0, 0)
        if colorId == 19:return QColor(67, 255, 163)
        if colorId == 20:return QColor(255, 176, 176)
        if colorId == 21:return QColor(228, 172, 121)
        if colorId == 22:return QColor(255, 255, 99)
        if colorId == 23:return QColor(0, 153, 84)
        
    def setHUDLabelColor(self, colorID):
        self.labelColorView_Label.setAutoFillBackground(True)
        #colorID = self.labelColor_Slider.value()
        color  = self.intToQColor(colorID)
        alpha  = 255
        values = "{r}, {g}, {b}, {a}".format(r = color.red(),
                                             g = color.green(),
                                             b = color.blue(),
                                             a = alpha
                                             )
        self.labelColorView_Label.setStyleSheet("QLabel { background-color: rgba("+values+"); }")
        utils.setHUDLabelColor(colorID)
        
    def setHUDFondColor(self, colorID):
        self.fontColorView_Label.setAutoFillBackground(True)
        #colorID = self.fontColor_Slider.value()
        color  = self.intToQColor(colorID)
        alpha  = 255
        values = "{r}, {g}, {b}, {a}".format(r = color.red(),
                                             g = color.green(),
                                             b = color.blue(),
                                             a = alpha
                                             )
        self.fontColorView_Label.setStyleSheet("QLabel { background-color: rgba("+values+"); }")
        utils.setHUDFondColor(colorID)
        
    def onHUD(self):
        hud = HUD.GMK_HUD()
        artistName = ''
        if self.name_Text.text() == '':
            artistName = os.getenv('USERNAME')
        else:
            artistName = self.name_Text.text()
        hud.showHUD(artistName)
    
    def offHUD(self):
        hud = HUD.GMK_HUD()
        hud.deleteHUD()
    
    def setTimeUnit(self, value):
        utils.setTimeUnit(value)
    
    def setSafeAction(self, state):
        utils.setSafeAction(state)
    
    def setResolutionGate(self, state):
        utils.setResolutionGate(state)
    
    def setScaleText(self, value):
        self.scale_Text.setText(str(value/100.0))
        
    def setScaleValue(self):
        value = self.scale_Text.text()
        floatValue = 0.0
        try:
            if float(value) < 0.1:
                floatValue = 0.1
            elif float(value) >= 0.1 and float(value) <= 1.0:
                floatValue = float(value)
            elif float(value) > 1.0:
                floatValue = 1.0
        except:
            floatValue = 0.5
        self.scale_Slider.setValue(floatValue*100)
        self.scale_Text.setText(("%.2f" %floatValue))
        
    def makePreview(self):
        percent = self.scale_Slider.value()
        width = float(self.width_Text.text())
        height = float(self.height_Text.text())
        
        preview = Preview.GMK_Preview()
        preview.makePreviwe(percent, width, height)
        
    def openFolder(self):
        subprocess.call(['explorer', 'D:\\tempPreview'])
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = GMK_PreviewTab()
    ui.show()
    sys.exit(app.exec_())
