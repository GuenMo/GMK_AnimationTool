# -*- coding:utf-8 -*-

# Maya module
import maya.OpenMayaUI as OMUI
import pymel.core as pm
import maya.cmds as cmds

# PySide module
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
    
# Python module
import collections
from datetime import datetime

def getMayaWindow():
    ptr = OMUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)

def getRootPath():
    utilsPath = __file__.replace("\\", "/")
    rootPath = utilsPath.rpartition("/")[0].rpartition("/")[0]
    print rootPath
    return rootPath

def getIconPath():
    return getRootPath() + "/icons" 

def findAllModuel(relativeDirectory):
    # relativeDirectory 경로에 모든 모듈(.py)를 검색해 리턴한다.
    allPyFiles = findAllFile( relativeDirectory, ".py" )
    returnModules = []
    
    for f in allPyFiles:
        if f != "__init__":
            returnModules.append(f)

    return returnModules

def findAllFile(relativeDirectory, fileExtension):
    # 주어진 확장자를 가지는 모든 파일을 찾아서 리턴 한다.
    import os
    
    fileDirectory = getRootPath()  + relativeDirectory + "/"
    allFiles = os.listdir(fileDirectory)
    returnFiles = []
    
    for f in allFiles:
        splitString = str(f).rpartition(fileExtension)
        if not splitString[1] == "" and splitString[2] == "":
            returnFiles.append(splitString[0])
        
    return returnFiles

def list_duplicates(seq):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)

def versionCheck():
    currentVersion = pm.versions.current()
    
    if '2014' in str(currentVersion): 
        return True
    elif '2016' in str(currentVersion): 
        return True
    else:
        return False    

    
def dateCheck():
    limitsDate = datetime(2015,12,31)
    currentDate = datetime.now()
    
    if currentDate <  limitsDate:
        return True
    else:
        return False
        
def checkSystem():
    verStat = versionCheck()
    dateStat = dateCheck()
    
    if verStat and dateStat:
        return True
    else:
        return False
    
def getSelectObject():
    sels = pm.ls(sl=True)
    selList = []
    for sel in sels:
        selList.append(sel.name())
    
    selStr = ','.join(selList)
    return selStr

def setHUDLabelColor(colorID):
    pm.displayColor('headsUpDisplayLabels',colorID,dormant=1)

def setHUDFondColor(colorID):
    pm.displayColor('headsUpDisplayValues',colorID,dormant=1)
    
def setTimeUnit(unit):
    timeType = unit.partition('(')[0].lower()
    pm.currentUnit(time=timeType)
    
def setSafeAction(state):
    on_off = False
    if state == 0:
        on_off = False
    elif state == 2:
        on_off = True
        
    perspCam = pm.PyNode('perspShape')
    perspCam.displaySafeAction.set(on_off)
    
    if pm.objExists('Rcam'):
        rCam = pm.PyNode('RcamShape')
        rCam.displaySafeAction.set(on_off)
        
def setResolutionGate(state):
    on_off = False
    if state == 0:
        on_off = False
    elif state == 2:
        on_off = True
        
    perspCam = pm.PyNode('perspShape')
    perspCam.displayResolution.set(on_off)
    perspCam.overscan.set(1.0)
    
    if pm.objExists('Rcam'):
        rCam = pm.PyNode('RcamShape')
        rCam.displayResolution.set(on_off)
        rCam.overscan.set(1.0)

def bakeWheel():
    selList = ["*:*wh_l_b_J", "*:*wh_G_RO", "*:*wh_l_b_J_mov01", "*:*wh_l_b_J_mov02",
           "*:*wh_r_b_J", "*:*wh_r_b_J_mov01", "*:*wh_r_b_J_mov02", "*:*wh_l_f_J",
           "*:*wh_l_f_J_mov", "*:*wh_l_f_J_mov01", "*:*wh_l_f_J_mov02", "*:*wh_r_f_J",
           "*:*wh_r_f_J_mov", "*:*wh_r_f_J_mov01", "*:*wh_r_f_J_mov02", "*:*_bake"]

    pm.select(cl=True)
    for sel in selList:
        try:
            pm.select(sel, add=True)
        except:
            pass
            
    startFrame = pm.playbackOptions(q=True, min=True)
    endFrmae = pm.playbackOptions(q=True, max=True)
    
    sel = pm.ls(sl=True)
    pm.bakeResults(sel,    sparseAnimCurveBake=False,
                   removeBakedAttributeFromLayer=False,
                   bakeOnOverrideLayer=False,
                   preserveOutsideKeys=True,
                   simulation=True,
                   sampleBy=1,
                   t=(str(startFrame) , str(endFrmae)),
                   disableImplicitControl=True,
                   at=["tx", "ty", "tz", "rx", "ry", "rz"])
    
def toggleWheel():
    if pm.softSelect(q=True, sse=1):
        pm.softSelect(sse=0)
        pm.select(cl=True)
    else:
        pm.softSelect(sse=1)
        pm.select(cl=True)
        pm.select("*:*Wheel_*"+".vtx[0:7]")  
        
def getTimeRange():  
    startFrame = pm.playbackOptions(q=True, min=True)
    endFrmae = pm.playbackOptions(q=True, max=True)
    return (startFrame, endFrmae)

def GMK_AnimCurve(startFrame, endFrame, speed, angle, ch):
    allCH = []
    if ch == 'All':
        pm.select( ('*:CH') , r=True)
        allCH = pm.ls(sl=True)
    elif ch =='Sel':
        allCH = pm.ls(sl=1)
        
    for ch in allCH:
        if ch.hasAttr('wheelSize'):
            namespae = ch.name().partition(':')[0]
            Selcha = []
            for attr in ['wh_r_f_J_mov02.rotateX', 'wh_r_b_J_mov02.rotateX', 'wh_l_f_J_mov02.rotateX', 'wh_l_b_J_mov02.rotateX']:
                attrNode = pm.PyNode(namespae + ':' + attr)
                Selcha.append(attrNode)
            
            pm.select( Selcha , r=True)
            pm.runtime.GraphEditor()
            pm.selectKey(Selcha, add=1, k=1, t=(startFrame + 1, endFrame - 1))
            pm.cutKey(clear=1,animation='keys')
            pm.selectKey(Selcha, add=1, k=1,t=(startFrame, startFrame))
            pm.keyframe(valueChange=0, animation='keys',absolute=1)
            pm.select(cl=True)
            
            wheelAnimNode = []
            for wheel in Selcha:
                wheelAnimNode.append(wheel.inputs()[0])
            
            tran_ctr = pm.PyNode(namespae + ':tran_ctr')
            animCurveTL = tran_ctr.tz.inputs()[0]
            
            numKey = animCurveTL.numKeys()
            holdFrame = []
            moveFrame = []
            
            for i in range(numKey):
                if i == numKey - 1:
                    holdFrame.append( [endFrame, endFrame, i])
                    break
                currentValue = animCurveTL.getValue(i)
                nextValue    = animCurveTL.getValue(i+1)
                if currentValue == nextValue:
                    holdFrame.append( [float(animCurveTL.getTime(i)), float(animCurveTL.getTime(i+1)) , i] ) 
                else:
                    increment = 1
                    if (nextValue - currentValue) < 0:
                        increment = -1
                    
                    moveFrame.append( [float(animCurveTL.getTime(i+1)), i+1, increment ])
    
                    
            for frame in holdFrame:
                for wheelAnim in wheelAnimNode:
                    pm.setKeyframe( wheelAnim, t=frame[0], v=0 )
                    pm.setKeyframe( wheelAnim, t=frame[1], v=0 )
                    
            holdRange = 0
            for hold in holdFrame:
                holdRange += (hold[1]-hold[0])
            angleN = (endFrame - startFrame - holdRange) * angle * speed
    
            count = 1
            for frame in moveFrame:
                for wheel in wheelAnimNode:
                    pm.keyframe(wheel, index = frame[1], absolute=True, valueChange=angleN*count*frame[2])
                count += 1
            del holdFrame[-1]
    
            for frame in holdFrame:
                for wheel in wheelAnimNode:
                    value = wheel.getValue(frame[2])
                    wheel.setValue(frame[2]+1, value)
            

def ScaleE(startFrame, endFrame, speed, angle, ch, clearSel):

    if clearSel == 'On':
        GMK_AnimCurve(startFrame, endFrame, speed, angle, ch)
        pm.select("*:*wh*mov02.rx", r=1)
        
    elif ch == 'All' and clearSel == 'Off':
        pm.mel.GraphEditor()
        pm.select("*:*wh*mov02.rx", r=1)
        Selcha=pm.ls(sl=1)
        pm.select(Selcha,r=1)
        for cha in Selcha:
            pm.scaleKey(cha,
                        valuePivot=0,
                        timeScale=1,
                        hierarchy='none',
                        float=(startFrame - 5 , endFrame),
                        floatPivot=0,
                        valueScale=speed,
                        timePivot=0,
                        scaleSpecifiedKeys=1,
                        shape=1,
                        time=(startFrame - 5 ,endFrame),
                        floatScale=1,
                        controlPoints=0)
    
    elif ch =='Sel' and clearSel == 'Off':
        Selcha=pm.ls(sl=1)
        #PrefixName=[]
        PrefixName=Selcha[0].split(":")
        pm.mel.GraphEditor()
        pm.select(PrefixName[0] + "*:*wh*mov02.rx",r=1)
        pm.scaleKey([PrefixName[0] + "*:*wh_l_f_J_mov02.rx",
                     PrefixName[0] + "*:*wh_r_f_J_mov02.rx",
                     PrefixName[0] + "*:*wh_l_b_J_mov02.rx",
                     PrefixName[0] + "*:*wh_r_b_J_mov02.rx"],
                    valuePivot=0,
                    timeScale=1,
                    hierarchy='none',
                    float=(startFrame - 5 , endFrame),
                    floatPivot=0,
                    valueScale=speed,
                    timePivot=0,
                    scaleSpecifiedKeys=1,
                    shape=1,
                    time=(startFrame - 5 ,endFrame),
                    floatScale=1,
                    controlPoints=0)
            
def wheel_key_scale(rott):
    
    #time value
    ctmd = int (cmds.playbackOptions (q= 1, min =1) )
    ctmc = int (cmds.currentTime (q=1))
    key_z_ = ctmc - ctmd
    key_z_2 = key_z_ + 1

    # select joint

    sel_t_ = cmds.ls (sl =1)[0]
    #sel_t_z = str (sel_t_[0].encode())
    sel_t_st = sel_t_.split(':')

    # key value
    aniCurve = cmds.listConnections( sel_t_ + '.rx', d=False, s=True )[0]
    jaj = cmds.getAttr(aniCurve +'.ktv[%s].kv' % key_z_)
    jaj2 = cmds.getAttr(aniCurve +'.ktv[%s].kv' % key_z_2)

    sbb_ = jaj2-jaj
    sbb_x = sbb_ *.01
    sbb_xp = sbb_ *.01

    if sbb_ > 0:
        
        scalv= []
        if sbb_ < rott:
            print "## no change ##"
        else:
            while sbb_x <= rott:
                sbb_x = sbb_x+sbb_xp
                scalv.append(sbb_x)
                print sbb_x
            scalvv = (len(scalv)+1)*.01
            cmds.scaleKey(sel_t_st[0]+':wh_l_f_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_r_f_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_l_b_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_r_b_J_mov02.rx', valueScale = scalvv)

    else:
        
        sbb_ = abs(sbb_)
        sbb_x = abs(sbb_x)
        sbb_xp = abs(sbb_xp)
        scalv= []
        if sbb_ < rott:
            print "## no change ##"
        else:
            while sbb_x <= rott:
                sbb_x = sbb_x+sbb_xp
                scalv.append(sbb_x)
                print sbb_x
            scalvv = (len(scalv)+1)*.01
            cmds.scaleKey(sel_t_st[0]+':wh_l_f_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_r_f_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_l_b_J_mov02.rx', valueScale = scalvv)
            cmds.scaleKey(sel_t_st[0]+':wh_r_b_J_mov02.rx', valueScale = scalvv)        

    
    
    
    
