# -*- coding: utf-8 -*-

import pymel.core as pm
import os
import subprocess

class GMK_Preview(object):
    
    def __init__(self):
        #self.FFmpeg = self.getRootPath() + '/ffmpeg/ffmpeg.exe'
        self.tempDir = 'D:/tempPreview/'
        
    def getScene(self):
        path = pm.sceneName()
        if path == '':
            path = 'untitled'
        scFullName = os.path.basename(path)
        scName = os.path.splitext(scFullName)[0]
        print path, scFullName, scName
        return scName
    
    def getRootPath(self):
        utilsPath = __file__.replace("\\", "/")
        rootPath = utilsPath.rpartition("/")[0].rpartition("/")[0]
        return rootPath
    
    def makePreviwe(self, percent, width, height):
        fileName = self.tempDir + self.getScene() + '.mov'
        aPlayBackSliderPython = pm.mel.eval('$tmpVar=$gPlayBackSlider')
        soundFile = pm.timeControl( aPlayBackSliderPython, q=True, sound=True)
        previewFile = pm.playblast(fp=4, 
                               format='qt', 
                               sound = soundFile,
                               forceOverwrite=True, 
                               percent=percent, 
                               filename = fileName , 
                               viewer=0, 
                               quality=100, 
                               widthHeight=(width, height),
                               compression="PNG")
        qtPath = 'C:\\Program Files (x86)\\QuickTime\\QuickTimePlayer.exe'        
        subprocess.Popen([qtPath, previewFile])
        #self.aviToMov(aviFile)
    '''
    def aviToMov(self, inputFile):
        outputFile = inputFile.replace('.avi','.mov')
        try:
            os.system("%s -i %s -c:v libx264 -crf 18 -g 1 -tune animation -pass 1 -c:a aac -strict experimental -b:a 192k -ac 2 -y %s" %(self.FFmpeg, inputFile,outputFile))
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"
        #os.remove(inputFile)
        
        qtPath = 'C:\\Program Files (x86)\\QuickTime\\QuickTimePlayer.exe'        
        subprocess.Popen([qtPath, outputFile])
        return outputFile
    '''


