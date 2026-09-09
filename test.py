import time as T
import msvcrt as Input
import _main_menu as m
import helpers as h
import sys
from enum import Enum
import shutil as shell
import window_handler as window
import collisionTest as collision
import BrickBreaker as brick
import TicTacToe as tik


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

        




    def __init__(self):
        self.__frameNumber = 0

        self.assetManager = self.AssetManager()
        self.windowHandler = window.WindowHandler()
        self.animationRegistry = self.Animations()
        # self.sceneManager = self.SceneManager(defaultScene=None , windowHandler=self.windowHandler , assetManager=self.assetManager , animationRegistry=self.animationRegistry)

        self.assetManager.importTextures(arrow="./Arrow.txt" , main_menu_nill="./MainMenuNill.txt" , BB="./brickBreaker.txt" , tic="./tictactoe.txt")
        # h.Sprite.createAnimation(animationName="LeftRight")
        # h.Sprite.addFrame(animationName="LeftRight" , textureName="arrow" , colorRegister={} , textureRect=(1 ,1) , dimensions=(7 , 1))
        # h.Sprite.addFrame(animationName="LeftRight" , textureName="arrow" , colorRegister={} , textureRect=(3 ,1) , dimensions=(7 , 1))
        self.__gameStates = [self.GameState.TicTacToe ,self.GameState.BrickBreaker , self.GameState.MainMenu , self.GameState.Collision]
        self.__gameStateIdx = 0
        self.__gameStateToScenes = {}
        self.__gameStateToScenes[self.GameState.MainMenu] = m.MainMenu(windowHandler=self.windowHandler , assetManager=self.assetManager , animationRegistry=self.animationRegistry)
        self.__gameStateToScenes[self.GameState.Collision] = collision.collisionTest(windowHandler=self.windowHandler)
        self.__gameStateToScenes[self.GameState.BrickBreaker] = brick.BrickBreaker(windowHandler=self.windowHandler , assetManager=self.assetManager)
        self.__gameStateToScenes[self.GameState.TicTacToe] = tik.TikTakToe(windowHandler=self.windowHandler , assetManager=self.assetManager , animationRegistry=self.animationRegistry)

    def getCurrentScene(self):
        return self.__gameStateToScenes[self.__gameStates[self.__gameStateIdx]]

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
            while( Input.kbhit()):
                key = Input.getch()
                if( key == b'\x1b'):
                    # print("\033[H\033[J", end="")
                    print("\033[?1049l", end="")
                    print("\x1b[?25h", end="")
                    return
                elif( key == b'p'):
                    # if(self.__gameState == self.GameState.MainMenu):
                    #     self.__gameState = self.GameState.Collision
                    # else:
                    #     self.__gameState = self.GameState.MainMenu
                    self.__gameStateIdx = (self.__gameStateIdx + 1)%len(self.__gameStates)
                elif ( key == b'r'):
                    if(self.__gameStates[self.__gameStateIdx] == self.GameState.BrickBreaker):
                        self.__gameStateToScenes[self.GameState.BrickBreaker] = brick.BrickBreaker(windowHandler=self.windowHandler , assetManager=self.assetManager)
                self.getCurrentScene().handleInput(input=key , time=(T.perf_counter() - loopStart))
            self.getCurrentScene().update(time=(T.perf_counter()- loopStart))
            self.getCurrentScene().render()
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



