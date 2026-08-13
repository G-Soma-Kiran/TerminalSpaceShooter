import time as T
import msvcrt as Input
import _main_menu as m
import helpers as h
import sys
from enum import Enum


class Game:

    class GameState(Enum):
        MainMenu = 1,
        Gameplay = 2,
        Pause = 3, 
    
    def __init__(self):
        self.__gameState = self.GameState.MainMenu


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
        self.importTextures(arrow="Arrow.txt" , main_menu_nill="MainMenuNill.txt")
        main_menu = m.MainMenu()
        loopStart = T.perf_counter()
        while(True):
            frameStart = T.perf_counter()

            while( Input.kbhit()):
                key = Input.getch()
                if( key == b'\x1b'):
                    print("\033[H\033[J", end="")
                    return
                main_menu.handleInput(input=key , time=(T.perf_counter() - loopStart))

            main_menu.update(time=(T.perf_counter()- loopStart))
            main_menu.render()
            print(f"\x1b[162;1H", end="")
            sys.stdout.flush()
            frameEnd = T.perf_counter()
            if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.016 ):
                T.sleep(0.016 - (frameEnd - frameStart))



sample = Game()
sample.run()



