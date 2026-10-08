import Engine.helpers as h
import Engine.scene as scene
from enum import Enum
import random as rnd
from math import ceil

_GAME_SCREEN_SIZE = (130 , 27)
_GAME_SCREEN_POS = ()

#Game object proportions , everything with respect to bird texture width.
_BIRD_WIDTH = 6

_PILLAR_WIDTH = int(1.5 * _BIRD_WIDTH)
_VERTICAL_SPACING = 2 * _BIRD_WIDTH
_HORIZONTAL_SPACING = 5 * _BIRD_WIDTH
_TOTAL_PILLAR_PAIRS = ceil(_GAME_SCREEN_SIZE[0]/(_PILLAR_WIDTH+_HORIZONTAL_SPACING))

class FlappyBird(scene.Scene): 

    def __setUpExtras(self):
        border = h.Sprite(h.rectangle(dimensions=(_GAME_SCREEN_SIZE[0] + 2, _GAME_SCREEN_SIZE[1] + 2)), colorRegister={}, textureRectPosition=(1, 1),
                                  dimensions=(_GAME_SCREEN_SIZE[0] + 2, _GAME_SCREEN_SIZE[1] + 2), zIndex=2)
        border.setTransparency(True)
        border.setPosition((_GAME_SCREEN_POS[0] - 1, _GAME_SCREEN_POS[1] - 1))
        self.__borderCoords = border.getOccupiedCoords()


        texture = []
        texture.append("┌" + "─"*(_PILLAR_WIDTH-2)+"┐\n")
        for _ in range(_GAME_SCREEN_SIZE[1] - 3):
            texture.append("│"+ " "*(_PILLAR_WIDTH-2) +"│\n")
        texture.append("│"+ "="*(_PILLAR_WIDTH-2) +"│\n")
        texture.append("="*_PILLAR_WIDTH+"\n")

        self.__upPillarTexture = ''.join(texture)
        texture.clear()



        texture.append("="*_PILLAR_WIDTH+"\n")
        texture.append("│"+ "="*(_PILLAR_WIDTH-2) +"│\n")

        for _ in range(_GAME_SCREEN_SIZE[1] - 3):
            texture.append("│"+ " "*(_PILLAR_WIDTH-2) +"│\n")
        texture.append("└" + "─"*(_PILLAR_WIDTH-2)+"┘\n")

        self.__downPillarTexture = ''.join(texture)

    def __getPillarHeight(self):
        return rnd.randint(_GAME_SCREEN_POS[0]-_GAME_SCREEN_SIZE[1] + 2 , _GAME_SCREEN_POS[0] - _VERTICAL_SPACING - 2)

    def __updatePillars(self):
        for i in range(_TOTAL_PILLAR_PAIRS):
            currPos = self.__pillars[i][0].getPosition()

            if(currPos[1] - 1 +_PILLAR_WIDTH <= _GAME_SCREEN_POS[1]-1 ):
                newY = _GAME_SCREEN_POS[1] + (_TOTAL_PILLAR_PAIRS-1)*(_PILLAR_WIDTH + _HORIZONTAL_SPACING) + _HORIZONTAL_SPACING
                newX = self.__getPillarHeight()
                self.__currPillarPair = (self.__currPillarPair+1)%_TOTAL_PILLAR_PAIRS

            else:
                newY = currPos[1]-1
                newX = currPos[0]

            self.__pillars[i][0].setPosition((newX , newY))
            self.__pillars[i][1].setPosition((newX+_VERTICAL_SPACING+_GAME_SCREEN_SIZE[1] , newY))

    def _onCreate(self):
        
        self.__windowHandler = self._systems.getWindow()
        self.__assetmanager = self._systems.getAssetManager()
        self.__animationsRegistry = self._systems.getAnimationRegistry()




        global _GAME_SCREEN_POS
        _GAME_SCREEN_POS=(
            (32//2) - (_GAME_SCREEN_SIZE[1] // 2),
            (162//2) - (_GAME_SCREEN_SIZE[0] // 2)
        )

        self.setView(view=h.View(viewPosition = (_GAME_SCREEN_POS[0]-1 , _GAME_SCREEN_POS[1]-1) , viewDimensions=(_GAME_SCREEN_SIZE[0]+2 , _GAME_SCREEN_SIZE[1]+2) , viewPortPos=(_GAME_SCREEN_POS[0]-1 , _GAME_SCREEN_POS[1]-1) , viewPortDimensions=(_GAME_SCREEN_SIZE[0]+2 , _GAME_SCREEN_SIZE[1]+2)))

        self.__setUpExtras()
        

        self.__bird = h.Sprite(self.__assetmanager.getTexture(textureName="FlappyBird") , colorRegister={} , textureRectPosition=(1,1) , dimensions=(6,3) , zIndex=1)
        self.__bird.setPosition(coords=(20 , 20))
        self.__bird.setCollisionRect(collisionRect=(2,1))
        self.__bird.setCollisionRectDimensions(dimensions=(6,2))

        self.__previousBirdDropTime = 0
        self.__previousPillarUpdateTime = 0

        self.__pillars = []
        self.__currPillarPair = 0
        for i in range(_TOTAL_PILLAR_PAIRS):
            self.__pillars.append(
                (
                    h.Sprite(texture=self.__upPillarTexture , colorRegister={} , textureRectPosition=(1,1) , dimensions=( _PILLAR_WIDTH , _GAME_SCREEN_SIZE[1]) , zIndex=1),
                    h.Sprite(texture=self.__downPillarTexture , colorRegister={} , textureRectPosition=(1,1) , dimensions=( _PILLAR_WIDTH , _GAME_SCREEN_SIZE[1]) , zIndex=1)
                ),
            )
            x = self.__getPillarHeight()
            y = _GAME_SCREEN_POS[1]+_GAME_SCREEN_SIZE[0]+ i*(_PILLAR_WIDTH + _HORIZONTAL_SPACING)
            self.__pillars[-1][0].setPosition((x , y))
            self.__pillars[-1][1].setPosition((x+_VERTICAL_SPACING+_GAME_SCREEN_SIZE[1] , y))

            self.__pillars[-1][0].setCollisionRect(collisionRect=(1,1))
            self.__pillars[-1][0].setCollisionRectDimensions(dimensions=(_PILLAR_WIDTH , _GAME_SCREEN_SIZE[1]))
            self.__pillars[-1][1].setCollisionRect(collisionRect=(1,1))
            self.__pillars[-1][1].setCollisionRectDimensions(dimensions=(_PILLAR_WIDTH , _GAME_SCREEN_SIZE[1]))
        

    def handleInput(self , * , input , time):

        if(input == b"p"):
            self.popAndSave()
            self.pushScene(sceneName="Tetris")
        
        elif(input == b'\x1b'):
            self.popScene()

        elif (input == b"resize"):
            currWindowSize = self.__windowHandler.getWindowSize()
            self.getView().setViewPortPosition(viewPortPosition=
                                            (
            (currWindowSize[1]//2) - (_GAME_SCREEN_SIZE[1] // 2)-1,
            (currWindowSize[0]//2) - (_GAME_SCREEN_SIZE[0] // 2)-1
        )
                                            )

        elif(input == b"m"):
            self.setPause(not self.getPause())

        elif(input == b" "):
            currPos = self.__bird.getPosition()
            self.__bird.setPosition((currPos[0]-2 , currPos[1]))
            self.__bird.setTextureRect(textureRectPosition=(5 ,1))
            self.__bird.setTextureRectDimensions(dimensions=(6,4))
            self.__previousBirdDropTime+=0.05

    def update(self , * , time):

        if(time - self.__previousPillarUpdateTime >= 0.015):
            self.__previousPillarUpdateTime = time
            self.__updatePillars()

        if(time - self.__previousBirdDropTime >= 0.1):
            self.__previousBirdDropTime = time
            currPos = self.__bird.getPosition()
            self.__bird.setPosition((currPos[0]+1, currPos[1]))
            self.__bird.setTextureRect(textureRectPosition=(1 ,1))
            self.__bird.setTextureRectDimensions(dimensions=(6,3))

        birdCollisionRectPos , birdCollisionRectDimensions = self.__bird.getWorldCollisionRect()
        pillar1CollisionRectPos , pillar1CollisionRectDimensions = self.__pillars[self.__currPillarPair][0].getWorldCollisionRect()
        pillar2CollisionRectPos , pillar2CollisionRectDimensions = self.__pillars[self.__currPillarPair][1].getWorldCollisionRect()

        if(
            self.__bird.getPosition()[0] >= _GAME_SCREEN_POS[0] + _GAME_SCREEN_SIZE[1] - self.__bird.getDimensions()[1]
            or
            self.__bird.getPosition()[0] < _GAME_SCREEN_POS[0]
            or
            h.isColliding(rect1Pos=birdCollisionRectPos , rect1Dimensions=birdCollisionRectDimensions , rect2Pos=pillar1CollisionRectPos , rect2Dimensions=pillar1CollisionRectDimensions)
            or
            h.isColliding(rect1Pos=birdCollisionRectPos , rect1Dimensions=birdCollisionRectDimensions , rect2Pos=pillar2CollisionRectPos , rect2Dimensions=pillar2CollisionRectDimensions)
            ):
            self.setPause(True)

    
    def render(self):
        self.__windowHandler.draw(occupiedCoords=self.__borderCoords)
        for i in range(_TOTAL_PILLAR_PAIRS):
            self.__windowHandler.draw(occupiedCoords=self.__pillars[i][0].getOccupiedCoords())
            self.__windowHandler.draw(occupiedCoords=self.__pillars[i][1].getOccupiedCoords())
        self.__windowHandler.draw(occupiedCoords=self.__bird.getOccupiedCoords())
