import helpers as h
from enum import Enum
import time as T

class TikTakToe:

    class State(Enum):
        gameplay = 1,
        gameend=2,
    class Turn(Enum):
        X = 1,
        O = 2

    def makeBox(self , * ,boxDimensions):
        boxWidth = boxDimensions[0]
        boxHeight = boxDimensions[1]

        texture = "┌"
        texture += (boxWidth - 2) * "─"
        texture += "┐\n"
        for i in range(boxHeight - 2):
            texture+="│"
            texture+=(boxWidth - 2) *" "
            texture+="│\n"
        texture += "└"
        texture += (boxWidth - 2) * "─"
        texture += "┘\n"

        return texture
    
    def makeBoard(self , * ,cellDimensions , boardStartPosition ):
        # cellWidth = cellDimensions[0]
        # cellHeight = cellDimensions[1]

        # texture = "┌"
        # texture += (cellWidth - 2) * "─"
        # texture += "┐\n"
        # for i in range(cellHeight - 2):
        #     texture+="│"
        #     texture+=(cellWidth - 2) *" "
        #     texture+="│\n"
        # texture += "└"
        # texture += (cellWidth - 2) * "─"
        # texture += "┘\n"

        cellTexture = self.makeBox(boxDimensions=cellDimensions)

        self.__cells = []

        for i in range(3):
            self.__cells.append([])

        for i in range(3):
            for j in range(3):
                self.__cells[i].append(h.Sprite(texture=cellTexture , colorRegister={} , textureRectPosition=(1,1) , dimensions=(cellDimensions[0] , cellDimensions[1]) , zIndex=1))
                self.__cells[i][j].setPosition((boardStartPosition[0] + i*cellDimensions[1] , boardStartPosition[1]+ j*cellDimensions[0]))
                self.__cells[i][j].setColorRegister(colorRegister={} , defaultColor=h.color(100, 120, 150))

    def makeX(self , * , position):
        X = h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(39,1) , dimensions=(4 , 2) , zIndex=1)
        X.setPosition(coords=position)
        return X

    def makeO(self , * , position):
        O = h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(43,1) , dimensions=(4 , 2) , zIndex=1)
        O.setPosition(coords=position)
        return O

    def checkWin(self):
        way1 = self.__occupiedCells[0][0][0] and self.__occupiedCells[0][1][0] and self.__occupiedCells[0][2][0] and (self.__occupiedCells[0][0][1] == self.__occupiedCells[0][1][1] == self.__occupiedCells[0][2][1])
        way2 = self.__occupiedCells[1][0][0] and self.__occupiedCells[1][1][0] and self.__occupiedCells[1][2][0] and (self.__occupiedCells[1][0][1] == self.__occupiedCells[1][1][1] == self.__occupiedCells[1][2][1])
        way3 = self.__occupiedCells[2][0][0] and self.__occupiedCells[2][1][0] and self.__occupiedCells[2][2][0] and (self.__occupiedCells[2][0][1] == self.__occupiedCells[2][1][1] == self.__occupiedCells[2][2][1])

        way4 = self.__occupiedCells[0][0][0] and self.__occupiedCells[1][0][0] and self.__occupiedCells[2][0][0] and (self.__occupiedCells[0][0][1] == self.__occupiedCells[1][0][1] == self.__occupiedCells[2][0][1])
        way5 = self.__occupiedCells[0][1][0] and self.__occupiedCells[1][1][0] and self.__occupiedCells[2][1][0] and (self.__occupiedCells[0][1][1] == self.__occupiedCells[1][1][1] == self.__occupiedCells[2][1][1])
        way6 = self.__occupiedCells[0][2][0] and self.__occupiedCells[1][2][0] and self.__occupiedCells[2][2][0] and (self.__occupiedCells[0][2][1] == self.__occupiedCells[1][2][1] == self.__occupiedCells[2][2][1])
        
        way7 = self.__occupiedCells[0][0][0] and self.__occupiedCells[1][1][0] and self.__occupiedCells[2][2][0] and (self.__occupiedCells[0][0][1] == self.__occupiedCells[1][1][1] == self.__occupiedCells[2][2][1])
        way8 = self.__occupiedCells[0][2][0] and self.__occupiedCells[1][1][0] and self.__occupiedCells[2][0][0] and (self.__occupiedCells[0][2][1] == self.__occupiedCells[1][1][1] == self.__occupiedCells[2][0][1])

        return way1 or way2 or way3 or way4 or way5 or way6 or way7 or way8

    def makeEndGameScreen(self , * , screenDimensions):
        texture = self.makeBox(boxDimensions=screenDimensions)

        self.__endScreenEntities.append(h.Sprite(texture=texture , colorRegister={} , textureRectPosition=(1,1) , dimensions=screenDimensions , zIndex=2))
        self.__endScreenEntities[-1].setPosition((14 , 63))
        self.__endScreenEntities.append(h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(49,1) , dimensions=(26 , 2) , zIndex=2))
        self.__endScreenEntities[-1].setPosition((15 , 64))
        self.__endScreenEntities.append(h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(53,1) , dimensions=(13 , 2) , zIndex=2))
        self.__endScreenEntities[-1].setPosition((18 , 64))

        for item in self.__endScreenEntities:
            item.setVisibility(boolean=False)
        
    def reset(self):
        self.__gameState = self.State.gameplay
        self.__currentTurn = self.Turn.X
        self.__selectedStatus = h.color(80 , 200 , 140)
        self.__selectedCell = (0 , 0)
        self.__entities.clear() 
        self.__isWin = False
        self.__occupiedCells.clear() 
        
        for i in range(3):
            self.__occupiedCells.append([(False , None) for j in range(3)])

        for item in self.__endScreenEntities:
            item.setVisibility(boolean=False)

    def __init__(self , * , windowHandler , assetManager , animationRegistry):
        self.__windowHandler = windowHandler
        self.__assetManager = assetManager
        self.__animationRegistry = animationRegistry

        self.border = h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(1 ,1) ,dimensions=(162 , 32) , zIndex=1)
        self.border.setPosition(coords=(1,1))
        self.border.setColorRegister(colorRegister={} ,defaultColor=h.color(100, 210, 230))

        self.makeBoard(cellDimensions=(12 , 6) , boardStartPosition=(10 , 62))
        self.__gameState = self.State.gameplay

        self.__currentTurn = self.Turn.X

        self.__selectedStatus = h.color(80 , 200 , 140)

        self.__selectedCell = (0 , 0)

        self.__entities = []
        self.__isWin = False

        # self.X = h.Sprite(texture=self.__assetManager.getTexture(textureName="tic") , colorRegister={} , textureRectPosition=(34,1) , dimensions=(4 , 4) , zIndex=1)
        # self.X.setPosition((boardStartPosition[0]+1 ,boardStartPosition[1]+4))

        # self.makeX(position=(boardStartPosition[0]+2 ,boardStartPosition[1]+4))
        # self.makeO(position=(boardStartPosition[0]+2 ,boardStartPosition[1]+4+cellWidth))

        self.__occupiedCells = []

        for i in range(3):
            self.__occupiedCells.append([(False , None) for j in range(3)])



        self.__endScreenEntities = []
        self.makeEndGameScreen(screenDimensions=(28,7))

    def handleInput(self , * , input , time):
        if(self.__gameState == self.State.gameplay):
            if(input == b"w"):
                currCell = self.__selectedCell
                self.__selectedCell = ((currCell[0] - 1)%3 , currCell[1])
            elif(input == b"s"):
                currCell = self.__selectedCell
                self.__selectedCell = ((currCell[0] + 1)%3 , currCell[1])
            elif(input == b"d"):
                currCell = self.__selectedCell
                self.__selectedCell = (currCell[0] , (currCell[1] + 1)%3)
            elif(input == b"a"):
                currCell = self.__selectedCell
                self.__selectedCell = (currCell[0] , (currCell[1] - 1)%3)
            elif(input == b"\r"):
                currCell = self.__selectedCell
                pos = self.__cells[currCell[0]][currCell[1]].getPosition()

                if(self.__occupiedCells[currCell[0]][currCell[1]][0] == False):
                    if(self.__currentTurn == self.Turn.X):
                        self.__entities.append(self.makeX(position=(pos[0]+2 , pos[1]+4)))
                        self.__entities[-1].setColorRegister(colorRegister={} , defaultColor = h.color(100, 170, 255))
                        self.__currentTurn = self.Turn.O
                        self.__occupiedCells[currCell[0]][currCell[1]] = (True , self.Turn.X)
                    else:
                        self.__entities.append(self.makeO(position=(pos[0]+2 , pos[1]+4)))
                        self.__entities[-1].setColorRegister(colorRegister={} , defaultColor = h.color(230, 120, 170))
                        self.__currentTurn = self.Turn.X
                        self.__occupiedCells[currCell[0]][currCell[1]] = (True , self.Turn.O)
                else:
                    pass
        elif(self.__gameState == self.State.gameend):
            if(input == b"\r"):
                self.reset()
            
    def update(self , * , time):

        self.__isWin = self.checkWin()
        if(self.__isWin):
            self.__gameState = self.State.gameend
            for item in self.__endScreenEntities:
                item.setVisibility(boolean=True)



        for cellRow in self.__cells:
            for cell in cellRow:
                cell.setColorRegister(colorRegister={} , defaultColor=h.color(100 , 120 , 150))
        currCell = self.__selectedCell
        self.__cells[currCell[0]][currCell[1]].setColorRegister(colorRegister={} , defaultColor=self.__selectedStatus)


        for i in range(3):
            for j in range(3):
                self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__cells[i][j].getOccupiedCoords())

        for entity in self.__entities:
            self.__windowHandler.handleOccupiedCoords(occupiedCoords=entity.getOccupiedCoords())

        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.border.getOccupiedCoords())

        for item in self.__endScreenEntities:
            self.__windowHandler.handleOccupiedCoords(occupiedCoords=item.getOccupiedCoords())

    def render(self):
        self.__windowHandler.render()
    