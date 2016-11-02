# -*- coding:utf-8 -*-

def GMK_AniTool_run():
    try:
        filePath = __file__
        GMK_AniTool_Path = filePath.rpartition("\\")[0]
    except:
        print "Environ Value 'GMK_AniTool_Path' not exist."
    
    else:
        import sys
        path = GMK_AniTool_Path
        
        if not path in sys.path:
            sys.path.append(path)
        
        import UI_AniTool.previewUI as PreviewUI
        reload(PreviewUI)
        
        PreviewUI.main()
    
if __name__ == "GMK_AniTool_run":    
    GMK_AniTool_run()    