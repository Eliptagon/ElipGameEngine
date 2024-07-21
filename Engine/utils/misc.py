import Engine.utils.global_data as global_data
import sys, traceback

def getTraceback(exc):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback_list = traceback.format_exception(exc_type, exc_value, exc_tb)
    return ''.join(traceback_list)

def quitGame():
    global_data.flags['running'] = False
    global_data.flags['logger'].log('Game closing', 'INFO')
    sys.exit()


def collectMeshesOnRenderLayer():
    pass
