import time as T
import msvcrt as Input
import Games._main_menu as m
import Engine.helpers as h
import sys
from enum import Enum
import shutil as shell
import Engine.window_handler as window
import Games.collisionTest as collision
import Games.BrickBreaker as brick
import Games.TicTacToe as tik
import Games.pauseScene as p
import Games.Tetris as tetris

class Game:

    class GameState(Enum):
        MainMenu = 1,
        Gameplay = 2,
        Pause = 3, 
        Collision = 4,
        BrickBreaker=5,
        TicTacToe = 6,

    class AssetManager:

        def __init__(self):
            self.__allTextures = {}
            self.__allTexturesByPath = {}

        def importTextures(self , **kwargs):
            for textureName , filepath in kwargs.items():
                if( textureName in self.__allTextures ):
                    raise ValueError(f"{textureName} is already assetManager.__allTextures")


                temp = self.__allTexturesByPath.get(filepath)

                if( temp != None ):
                    self.__allTextures[textureName] = self.__allTexturesByPath[filepath]
                    continue

                with open(filepath , "r" , encoding="utf-8") as file:
                    temp = file.read()
                    self.__allTextures[textureName] = temp
                    self.__allTexturesByPath[filepath] = temp

        def getTexture(self , * , textureName):
            val = self.__allTextures.get(textureName)

            if(val == None):
                raise ValueError(f"{textureName} is not present => getTexture()")
            
            return val
        
    class Animations:
        def __init__(self):
            self.__allAnimations= {}

        def createAnimation(self , * , animationName ):
            if(animationName in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is already in animationRegistry.allAnimations")
    
            self.__allAnimations[animationName] = []

        def addFrame(self , * , animationName , texture , colorRegister , textureRect , dimensions):
            if(animationName not in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is not in animationRegistry.addFrame")
            self.__allAnimations[animationName].append((texture , colorRegister , textureRect , dimensions))

        def getAnimation(self , * , animationName):
            if(animationName not in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is not in animationRegistry.addFrame")
            return tuple(self.__allAnimations[animationName])

    class SceneManager:
        
        def __init__(self , * , defaultScene  , windowHandler , assetManager , animationRegistry):
            self.__windowHandler = windowHandler 
            self.__assetManager = assetManager
            self.__animationRegistry = animationRegistry
            self.__sceneStack = []
            self.__requests = [(h.Request.push , defaultScene)]
            self.__sceneRegistry = {}
            self.__persistentScenes = {}

        def registerScene(self , *args):
            for scene in args:
                if(scene.__name__ in self.__sceneRegistry.keys()):
                    raise ValueError(f"{scene} already exists in sceneRegistry")
                self.__sceneRegistry[scene.__name__] = scene
            

        def __createScene(self , * , sceneName):
            return self.__sceneRegistry[sceneName](windowHandler=self.__windowHandler , assetManager=self.__assetManager , animationRegistry=self.__animationRegistry)
        
        def __push(self , * , sceneName):
            if(self.__persistentScenes.get(sceneName) != None ):
                self.__sceneStack.append(self.__persistentScenes.pop(sceneName))
            else:
                self.__sceneStack.append(self.__createScene(sceneName=sceneName))

        def __pop(self):
            self.__sceneStack.pop()

        def __saveAndPop(self):
            self.__persistentScenes[type(self.__sceneStack[-1]).__name__] = self.__sceneStack[-1]
            self.__sceneStack.pop()

        def __replaceWith(self , * , sceneName):
            self.__pop()
            self.__push(sceneName=sceneName)

        def __switchTo(self , *,sceneName):
            self.__saveAndPop()
            self.__push(sceneName=sceneName)

        def completeRequests(self):
            for request , scene in self.__requests:
                if(request == h.Request.push):
                    self.__push(sceneName=scene)
                elif(request == h.Request.pop):
                    self.__pop()
                elif(request == h.Request.popAndSave ):
                    self.__saveAndPop()
                elif(request == h.Request.replaceWith):
                    self.__replaceWith(sceneName=scene)
                elif(request == h.Request.switchTo):
                    self.__switchTo(sceneName=scene)
                else:
                    raise ValueError(f"Unknown scene request: {request}")

            self.__requests.clear()

        def updateScene(self , * , keys , time):
            for key , t in keys:
                self.__sceneStack[-1].handleInput(input=key , time=t)


            i=len(self.__sceneStack)-1
            while(i > 0 and self.__sceneStack[i].updateBelow()):
                i=i-1
            while(i < len(self.__sceneStack)-1):
                self.__sceneStack[i].update(time=time)
                i+=1
            reqs = self.__sceneStack[-1].update(time = time)
            self.__requests.extend(reqs)

            i=len(self.__sceneStack)-1
            while(i > 0 and self.__sceneStack[i].renderBelow()):
                i-=1
            while(i < len(self.__sceneStack)-1):
                self.__sceneStack[i].render()
                i+=1

            self.__sceneStack[-1].render()

        def isSceneStackEmpty(self):
            return len(self.__sceneStack) == 0

    def __init__(self):
        self.__frameNumber = 0

        self.assetManager = self.AssetManager()
        self.windowHandler = window.WindowHandler()
        self.animationRegistry = self.Animations()
        self.sceneManager = self.SceneManager(defaultScene="Tetris" , windowHandler=self.windowHandler , assetManager=self.assetManager , animationRegistry=self.animationRegistry)

        self.assetManager.importTextures(arrow="./Assets/Textures/Arrow.txt" , main_menu_nill="./Assets/Textures/MainMenuNill.txt" , BB="./Assets/Textures/brickBreaker.txt" , tic="./Assets/Textures/tictactoe.txt" , pause="./Assets/Textures/pause.txt" )
        self.sceneManager.registerScene(tik.TikTakToe , m.MainMenu , collision.collisionTest , brick.BrickBreaker , p.PauseScene , tetris.Tetris)

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
            self.windowHandler.handleTerminalSizeChange(terminalSize=tuple(shell.get_terminal_size()) , time=(T.perf_counter() - loopStart) )
            self.sceneManager.completeRequests()
            if(self.sceneManager.isSceneStackEmpty()):
                print("\033[?1049l", end="")
                print("\x1b[?25h", end="")
                return
            keys=[]
            while( Input.kbhit()):
                keys.append((Input.getch() , T.perf_counter() - loopStart))

            self.sceneManager.updateScene(keys=keys , time=(T.perf_counter()- loopStart))


            print(f"\x1b[31;3H", end="")
            if(self.__frameNumber%60 == 0):
                print(f"{1/dt : .2f}" , end="")
            sys.stdout.flush()

            frameEnd = T.perf_counter()
            
            if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.033 ):
                T.sleep(0.033 - (frameEnd - frameStart))
            self.__frameNumber+=1
        



sample = Game()
sample.run()



