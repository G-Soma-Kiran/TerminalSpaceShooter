import helpers as h
from enum import Enum
import random as rnd

_GRID_SIZE = (40 , 26)
# _GRID_POS = ( (32//2) - (_GRID_SIZE[1]//2) , (162//2) - (_GRID_SIZE[0]//2) )
_GRID_POS = ()

COLORS = [
    h.color(0, 220, 220),
    h.color(245, 220, 0),
    h.color(160, 60, 220),
    h.color(0, 200, 80),
    h.color(220, 40, 50),
    h.color(40, 90, 220),
    h.color(245, 130, 20),
]

class Tetris:

    class BlockType(Enum):
        L=1
        J=2
        Z=3
        S=4
        I=5
        T=6
        O=7


    class Block:

        class CollisionType(Enum):
            RightOutOfBounds = 1
            LeftOutOfBounds = -1
            BottomOutOfBounds = 0
            BlockCollision = 101
            NoCollision = -10
        
        def __createBlock(self , color , blockType):
            self.__individualSprites = []
            for _ in range(4):
                self.__individualSprites.append(h.Sprite(texture="██" , colorRegister={} , textureRectPosition=(1,1) , dimensions=(2 ,1) , zIndex=1))
                self.__individualSprites[-1].setColorRegister(colorRegister={} , defaultColor=color)

            if(blockType == Tetris.BlockType.L):
                self.__individualPositions = [(-1 , 0) , (0 , 0) , (1 , 0) , (1 , 2)]
            elif(blockType == Tetris.BlockType.J):
                self.__individualPositions = [(-1 , 0) , (0 , 0) , (1 , 0) , (1 , -2)]
            elif(blockType == Tetris.BlockType.Z):
                self.__individualPositions = [(0 , -2) , (0 , 0) , (1 , 0) , (1 , 2)]
            elif(blockType == Tetris.BlockType.S):
                self.__individualPositions = [(0 , 0) , (0 , 2) , (1 , -2) ,(1 , 0)]
            elif(blockType == Tetris.BlockType.I):
                self.__individualPositions = [(-1 , 0) , (0 , 0) ,(1 , 0) , (2 , 0)]
            elif(blockType == Tetris.BlockType.T):
                self.__individualPositions = [(0 , -2) , (0 , 0) , (0 , 2) , (1 , 0)]
            elif(blockType == Tetris.BlockType.O):
                self.__individualPositions = [(0 , 0) , (0 , -2) , (1 , -2) , (1 , 0)]
        
        def __init__(self ,grid ,color , blockType):
            self.__individualSprites = []
            self.__individualPositions = []
            self.__createBlock(color , blockType)
            self.__gameGrid = grid
            self.__blockType = blockType
            self.__position = (_GRID_POS[0]-2 , _GRID_POS[1] + (_GRID_SIZE[0]//2))
            self.__settled = False
            self.color = color

        def getGlobalPositions(self):
            globalPositions = []
            for position in self.__individualPositions:
                pos = (position[0]+self.__position[0] , position[1] + self.__position[1])
                globalPositions.append(pos)
            return globalPositions

        def __isValid(self , positions):
            for position in positions:
                if(position[1] > _GRID_POS[1] + _GRID_SIZE[0] - 2):
                    return self.CollisionType.RightOutOfBounds

                if(position[1] < _GRID_POS[1]):
                    return self.CollisionType.LeftOutOfBounds

                if(position[0] > _GRID_POS[0] + _GRID_SIZE[1]-1):
                    return self.CollisionType.BottomOutOfBounds

                if(position[0] >= _GRID_POS[0] and self.__gameGrid[position[0] - _GRID_POS[0]][(position[1] - _GRID_POS[1])//2] is not None):
                    return self.CollisionType.BlockCollision

            return self.CollisionType.NoCollision
                
        def update(self):
            pos = self.getGlobalPositions()
            for i in range(4):
                self.__individualSprites[i].setPosition(pos[i])

            return self.__settled

        def rotateLeft(self):
            if(self.__blockType == Tetris.BlockType.O):
                return
            for i in range(4):
                pos = self.__individualPositions[i]
                self.__individualPositions[i] = (-pos[1]//2 , pos[0]*2)

        def tryToMove(self , input):
            currentPos = self.__position
            currentPositionsOfBlocks = self.__individualPositions.copy()
            if(input == b"d"):
                self.__position = (currentPos[0] , currentPos[1]+2)
                res = self.__isValid(self.getGlobalPositions())

                if(res == self.CollisionType.NoCollision):
                    return
                elif(res == self.CollisionType.RightOutOfBounds or res == self.CollisionType.LeftOutOfBounds):
                    self.__position = currentPos
                elif(res == self.CollisionType.BlockCollision or res == self.CollisionType.BottomOutOfBounds):
                    #initiate countdown
                    self.__position = currentPos
                    self.__settled = True

            elif(input == b"a"):
                self.__position = (currentPos[0] , currentPos[1]-2)
                res = self.__isValid(self.getGlobalPositions())

                if(res == self.CollisionType.NoCollision):
                    return
                elif(res == self.CollisionType.RightOutOfBounds or res == self.CollisionType.LeftOutOfBounds):
                    self.__position = currentPos
                elif(res == self.CollisionType.BlockCollision or res == self.CollisionType.BottomOutOfBounds):
                    #initiate countdown
                    self.__position = currentPos
                    self.__settled = True

            elif(input == b"r"):
                self.rotateLeft()
                res = self.__isValid(self.getGlobalPositions())
                
                if(res == self.CollisionType.NoCollision):
                    return
                elif(res == self.CollisionType.RightOutOfBounds or res == self.CollisionType.LeftOutOfBounds):
                    self.__individualPositions = currentPositionsOfBlocks
                elif(res == self.CollisionType.BlockCollision or res == self.CollisionType.BottomOutOfBounds):
                    #initiate countdown
                    self.__individualPositions = currentPositionsOfBlocks
                    self.__settled = True

        def tryToMoveDown(self):
            currentPos = self.__position
            self.__position = (currentPos[0]+1 , currentPos[1])
            res = self.__isValid(self.getGlobalPositions())
            if(res == self.CollisionType.NoCollision):
                return
            elif(res == self.CollisionType.RightOutOfBounds or res == self.CollisionType.LeftOutOfBounds):
                self.__position = currentPos
            elif(res == self.CollisionType.BlockCollision or self.CollisionType.BottomOutOfBounds):
                #initiate countdown
                self.__position = currentPos
                self.__settled = True

        def getOccupiedCoords(self):
            coords = []
            for sprite in self.__individualSprites:
                coords.append(sprite.getOccupiedCoords())
            return coords

    def renderBelow(self):
        return self.__renderBelow

    def updateBelow(self):
        return self.__updateBelow

    def updateGrid(self):

        newRenderTexture = ""
        newColorRegister = {}
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid[0])):
                if(self.__grid[i][j] is None):
                    newRenderTexture+="  "
                else:
                    newRenderTexture+="██"
                    newColorRegister[(i+1 , 2*j+1)] = self.__grid[i][j]
                    newColorRegister[(i+1 , 2*j+2)] = self.__grid[i][j]
            newRenderTexture+="\n"

        self.__renderSprite.setTexture(texture=newRenderTexture)
        self.__renderSprite.setColorRegister(colorRegister=newColorRegister)

    def __setupExtras(self):
        self.__border = h.Sprite(h.rectangle(dimensions=(_GRID_SIZE[0]+2 , _GRID_SIZE[1]+2)) , colorRegister={} , textureRectPosition=(1,1) , dimensions=(_GRID_SIZE[0]+2 , _GRID_SIZE[1]+2) , zIndex=1)
        self.__border.setTransparency(True)
        self.__border.setPosition((_GRID_POS[0]-1 , _GRID_POS[1]-1))
        
    def __newBlock(self , color , blockType):
        return self.Block(self.__grid , color , blockType)

    def __init__(self , * , windowHandler , assetManager , animationRegistry):
        self.__windowHandler = windowHandler
        self.__assetManager = assetManager
        self.__animationRegistry = animationRegistry

        self.__reqs = []
        self.__renderBelow = False
        self.__updateBelow = False

        self.__previousTime = 0


        global _GRID_POS

        _GRID_POS = (  
            (self.__windowHandler.getWindowSize()[1]//2) - (_GRID_SIZE[1]//2),
            (self.__windowHandler.getWindowSize()[0]//2) - (_GRID_SIZE[0]//2)
        )



        self.__setupExtras()




        self.__grid = [[None]*(_GRID_SIZE[0]//2) for _ in range(_GRID_SIZE[1])]
        renderTexture = ""
        for _ in range(_GRID_SIZE[1]):
            renderTexture+=" "*_GRID_SIZE[0]
            renderTexture+="\n"

        self.__renderSprite = h.Sprite(texture=renderTexture , colorRegister={} , textureRectPosition=(1,1) , dimensions=_GRID_SIZE , zIndex=1)
        self.__renderSprite.setPosition(coords=_GRID_POS)
        self.__renderSprite.setTransparency(True)


        self.__activeBlock = self.__newBlock(rnd.choice(COLORS) , rnd.choice(list(self.BlockType)))

    def handleInput(self , * , input , time):
        if(input == b"p"):
            self.__reqs.append((h.Request.popAndSave , None))
            self.__reqs.append((h.Request.push , "TikTakToe"))

        if(input == b'\x1b'):
            self.__reqs.append((h.Request.pop,None))

        if(self.__activeBlock is not None):
            self.__activeBlock.tryToMove(input)

    def update(self , * , time):

        if(self.__activeBlock is None):
            self.__activeBlock = self.__newBlock(rnd.choice(COLORS) , rnd.choice(list(self.BlockType)))

        if(time - self.__previousTime >= 0.3):
            self.__activeBlock.tryToMoveDown()
            self.__previousTime = time


        isSettled = self.__activeBlock.update()
        if(isSettled):
            pos = self.__activeBlock.getGlobalPositions()
            for p in pos:
                self.__grid[p[0] - _GRID_POS[0]][(p[1] - _GRID_POS[1])//2] = self.__activeBlock.color
            self.__activeBlock = None
            
            self.updateGrid()

        copy = self.__reqs[:]
        self.__reqs.clear()
        return copy

    def render(self):    

        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__border.getOccupiedCoords())
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__renderSprite.getOccupiedCoords())

        if(self.__activeBlock is not None):
            coords = self.__activeBlock.getOccupiedCoords()
            for coord in coords:
                self.__windowHandler.handleOccupiedCoords(occupiedCoords=coord)

        self.__windowHandler.render()
