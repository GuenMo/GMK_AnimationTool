# -*- coding: utf-8 -*-

import pymel.core as pm
import os
from time import gmtime, strftime

class GMK_HUD(object):
    
    def __init__(self):
        self.setResolution()
        self.deleteDefaultHUD()
    
    def deleteDefaultHUD(self):
        pm.mel.setSelectDetailsVisibility(False)
        pm.mel.setObjectDetailsVisibility(False)
        pm.mel.setParticleCountVisibility(False)
        pm.mel.setPolyCountVisibility(False)
        pm.mel.setAnimationDetailsVisibility(False)
        pm.mel.setHikDetailsVisibility(False)
        pm.mel.setFrameRateVisibility(False)
        pm.mel.setCurrentFrameVisibility(False)
        pm.mel.setSceneTimecodeVisibility(False)
        pm.mel.setCurrentContainerVisibility(False)
        pm.mel.setCameraNamesVisibility(False)
        pm.mel.setFocalLengthVisibility(False)
        pm.mel.setViewAxisVisibility(False)
        pm.toggleAxis(o=False)
    
    def deleteHUD(self):
        if pm.headsUpDisplay('frameCounterHUD',exists=True):
            pm.headsUpDisplay('frameCounterHUD', rem=True)              
        if pm.headsUpDisplay('artistNameHUD',exists=True):
            pm.headsUpDisplay('artistNameHUD', rem=True)
        if pm.headsUpDisplay('dateNameHUD',exists=True):
            pm.headsUpDisplay('dateNameHUD', rem=True)
        if pm.headsUpDisplay('cameraFocalHUD',exists=True):
            pm.headsUpDisplay('cameraFocalHUD', rem=True) 
    
    def showHUD(self, name):
        self.deleteHUD()
        self.artilstName = name 
        pm.headsUpDisplay('frameCounterHUD', allowOverlap=1, l=u"■", b=4, s=5, dataFontSize='small', blockSize='small', dataWidth=5,
                           preset="currentFrame")
        
        pm.headsUpDisplay('artistNameHUD', l=u"■", allowOverlap=1, b=3, s=5, dataFontSize='small', blockSize='small',
                           command=self.getArtist, event = 'timeChanged')
        
        pm.headsUpDisplay('dateNameHUD', l=u"■", allowOverlap=1, b=2, s=5, dataFontSize='small', blockSize='small',
                           command=self.getData, event = 'timeChanged')

        pm.headsUpDisplay('cameraFocalHUD', l=u"■", allowOverlap=1, b=1, s=5, dataFontSize='small', blockSize='small',
                           command=self.getScene, event = 'timeChanged')
        
    def getArtist(self, *args):
        return self.artilstName
    
    def getData(self, *args):
        return strftime("%Y-%m-%d", gmtime())
    
    def getScene(self, *args):
        path = pm.sceneName()
        scFullName = os.path.basename(path)
        scName = os.path.splitext(scFullName)[0]
        
        validSCName = ''
        if not scName.find('_') == -1 and not scName.split('_')[1] == '':
            validSCName = scName.split('_')[0] +'_'+scName.split('_')[1] 
        else:
            validSCName = scName
            
        focal = ''
        if pm.objExists('Rcam'):
            rcam = pm.PyNode('Rcam')
            focal = str(int(rcam.focalLength.get()))
        else:
            focal = '"Rcam" does not exist.'
        return validSCName +' / '+ focal
    
    def setResolution(self):
        Resolution = pm.PyNode('defaultResolution')
        Resolution.width.set(1280)
        Resolution.height.set(720)
        
