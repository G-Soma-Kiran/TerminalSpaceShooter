import helpers as h

class MainMenu: 

    def __init__(self ,* , windowHandler , assetManager , animationRegistry):
        self.flag = True
        self.__windowHandler = windowHandler
        self.__assetmanager = assetManager
        self.__animationsRegistry = animationRegistry
        temp = {}
        for i in range(1 , 33):
            for j in range(1 , 165): 
                temp[(i , j)] = "\x1b[0m"
      
        self.visual = h.Sprite(self.__assetmanager.getTexture(textureName="main_menu_nill") , colorRegister=temp , textureRectPosition=(1 , 1) , dimensions=(162 , 31) , zIndex=1)
        self.visual.setPosition((1 , 1))


        self.__arrow = h.Sprite(self.__assetmanager.getTexture(textureName="arrow") , colorRegister={} , textureRectPosition=(1 , 1) , dimensions=(7 , 1) , zIndex=2)
        self.__arrow.setPosition((12  , 59))
        temp={}
        for i in range(1 , 3):
            for j in range(1 , 8):
                temp[(i , j)] =  "\x1b[38;2;255;255;0m"
        self.__arrow.setColorRegister(colorRegister=temp)
        self.__lastVisibleTimeOfArrow = 0

    def handleInput(self , * , input , time):
        if(input == b"w"):
            self.__arrow.setPosition((12 , 59))
            self.__lastVisibleTimeOfArrow = time
        elif(input == b"s"):
            self.__arrow.setPosition((17 , 59))
            self.__lastVisibleTimeOfArrow = time
        elif(input == b"a"):
            self.__arrow.setTextureRect(textureRectPosition=(3 , 1))
            self.__lastVisibleTimeOfArrow = time
        elif(input == b"d"):
            self.__arrow.setTextureRect(textureRectPosition=(1 , 1))
            self.__lastVisibleTimeOfArrow = time
        
    def update(self , * , time):
        # self.__arrow.update(time=time)
        # if( time - self.__lastVisibleTimeOfArrow >= 0.59):
        #     self.__arrow.toggleVisibility()
        #     self.__lastVisibleTimeOfArrow = time
        currPos = self.__arrow.getPosition()
        if(currPos[1] >= 140):
            self.flag = False

        if(currPos[1]<=20):
            self.flag = True

        if(self.flag):
            self.__arrow.setTextureRect(textureRectPosition=(1 , 1))
            self.__arrow.setPosition((currPos[0] , currPos[1] + 1))
        else:
            self.__arrow.setPosition((currPos[0] , currPos[1] - 1))
            self.__arrow.setTextureRect(textureRectPosition=(3 , 1))

        self.__windowHandler.handleOccupiedCoords(occupiedCoords= self.visual.getOccupiedCoords())
        self.__windowHandler.handleOccupiedCoords(occupiedCoords= self.__arrow.getOccupiedCoords())
    def render(self):
        self.__windowHandler.render()

        
