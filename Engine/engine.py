import time as T
import msvcrt as Input
import Engine.helpers as h
import sys
import shutil as shell
import Engine._window_handler as window
import Engine._asset_manager as asset
import Engine._animation_registry as animations
import Engine._scenemanager as sm
import Engine._subsystem as subsystem

class Game:

    def __init__(self , * , defaultScene , viewSize):
        self.__frameNumber = 0

        self.__assetManager = asset.AssetManager()
        self.__windowHandler = window.WindowHandler(viewSize=viewSize)
        self.__animationRegistry = animations.Animations()
        self.subsystems:subsystem.SubSystems = subsystem.SubSystems(windowHandler=self.__windowHandler , assetManager=self.__assetManager , animationRegistry=self.__animationRegistry)

        self.__sceneManager = sm.SceneManager(defaultScene=defaultScene ,subsystems=self.subsystems)

    def registerScene(self , *args):
        self.__sceneManager.registerScene(*args)

    def getSceneInit(self)->subsystem.SubSystems:
        return self.subsystems

    def run(self):
        print("\033[?1049h", end="")
        print("\x1b[?25l", end="")
        loopStart = T.perf_counter()
        previousTime = loopStart
        while(True):
            frameStart = T.perf_counter()
            currentTime = frameStart
            dt = currentTime - previousTime
            previousTime = currentTime
            windowstate = self.__windowHandler._WindowHandler__handleTerminalSizeChange(terminalSize=tuple(shell.get_terminal_size()) , time=(T.perf_counter() - loopStart) )
            self.__sceneManager.completeRequests()
            if(self.__sceneManager.isSceneStackEmpty()):
                print("\033[?1049l", end="")
                print("\x1b[?25h", end="")
                return
            keys=[]

            if(windowstate == window.windowState.ResizingEnd):
                keys.append((b"resize" , T.perf_counter() - loopStart))

            while( Input.kbhit()):
                input = Input.getch()
                if(windowstate == window.windowState.NoResize or windowstate == window.windowState.ResizingEnd):
                    keys.append((input , T.perf_counter() - loopStart))

            if(windowstate != window.windowState.NoResize and windowstate != window.windowState.ResizingEnd):
                T.sleep(0.033)
                continue
            self.__sceneManager.updateScene(keys=keys , time=(T.perf_counter()- loopStart))


            print(f"\x1b[31;3H", end="")
            if(self.__frameNumber%60 == 0):
                print(f"{1/dt : .2f}" , end="")
            sys.stdout.flush()

            frameEnd = T.perf_counter()
            
            if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.033 ):
                T.sleep(0.033 - (frameEnd - frameStart))
            self.__frameNumber+=1


