import time as T
import msvcrt as Input
import _main_menu as m
import helpers as h
import sys
from enum import Enum
import shutil as shell

class Game:

    class GameState(Enum):
        MainMenu = 1,
        Gameplay = 2,
        Pause = 3, 
    
    def __init__(self):
        self.__frameNumber = 0
        self.importTextures(arrow="Arrow.txt" , main_menu_nill="MainMenuNill.txt")
        # h.Sprite.createAnimation(animationName="LeftRight")
        # h.Sprite.addFrame(animationName="LeftRight" , textureName="arrow" , colorRegister={} , textureRect=(1 ,1) , dimensions=(7 , 1))
        # h.Sprite.addFrame(animationName="LeftRight" , textureName="arrow" , colorRegister={} , textureRect=(3 ,1) , dimensions=(7 , 1))
        self.__gameState = self.GameState.MainMenu
        self.__gameStateToScenes = {}
        self.__gameStateToScenes[self.GameState.MainMenu] = m.MainMenu()

    def getCurrentScene(self):
        return self.__gameStateToScenes[self.__gameState]
    
    def importTextures(self , **kwargs):
        for textureName , filepath in kwargs.items():
            if( textureName in h.Sprite.allTextures ):
                raise ValueError(f"{textureName} is already h.Sprite __allTextures")


            temp = h.Sprite.allTexturesByPath.get(filepath)

            if( temp != None ):
                h.Sprite.allTextures[textureName] = h.Sprite.allTexturesByPath[filepath]
                continue

            with open(filepath , "r" , encoding="utf-8") as file:
                temp = file.read()
                h.Sprite.allTextures[textureName] = temp
                h.Sprite.allTexturesByPath[filepath] = temp


    def run(self):
        loopStart = T.perf_counter()
        previousTime = loopStart
        while(True):
            frameStart = T.perf_counter()
            currentTime = frameStart
            dt = currentTime - previousTime
            previousTime = currentTime

            resize=h.Sprite.handleTerminalSizeChange(terminalSize=tuple(shell.get_terminal_size()) , time=(T.perf_counter() - loopStart) )
            while( Input.kbhit()):
                key = Input.getch()
                if( key == b'\x1b'):
                    print("\033[H\033[J", end="")
                    return
                self.getCurrentScene().handleInput(input=key , time=(T.perf_counter() - loopStart))
            self.getCurrentScene().update(time=(T.perf_counter()- loopStart))
            self.getCurrentScene().render(forced=resize)
            print(f"\x1b[162;1H", end="")
            if(self.__frameNumber%60 == 0):
                print(f"{1/dt : .2f}" , end="")
            sys.stdout.flush()

            frameEnd = T.perf_counter()
            
            if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.016 ):
                T.sleep(0.016 - (frameEnd - frameStart))
            self.__frameNumber+=1



sample = Game()
sample.run()



