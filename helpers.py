class Sprite:

    class __TextureData:
        def __init__(self, texture , * ,  colorRegister , textureRectPositionInTexture , dimensions):
            self.texture = texture
            self.dimensions = (dimensions[0] - 1 , dimensions[1])
            self.textureRectPosition = textureRectPositionInTexture
            self.colorRegister = colorRegister




    def __init__(self , texture  , * , colorRegister  , textureRectPosition ,  dimensions , zIndex):
        self.__texture =  self.__TextureData( texture , colorRegister=colorRegister, textureRectPositionInTexture=textureRectPosition , dimensions=dimensions) 

        self.__position = None

        self.__visible = True

        self.__currentAnimation = None
        self.__currentAnimationSpeed = 24
        self.__previousFrameRenderTime = 0
        self.__currentAnimationFrameNumber = 0

        self.__zIndex = zIndex

    def setPosition(self , coords):

        if (self.__position != coords):
            self.__position = coords
        else:
            return

    def getPosition(self):
        return self.__position

    def setTexture(self , texture):
        self.__texture.texture = texture


    def setTextureRect(self , * , textureRectPosition):
        self.__texture.textureRectPosition = textureRectPosition


    def setTextureRectDimensions(self , * , dimensions):
        self.__texture.dimensions = (dimensions[0] - 1 , dimensions[1])

    def setColorRegister(self , * , colorRegister):
        self.__texture.colorRegister = colorRegister

    def setAnimation(self , * , animation):

        self.__currentAnimationName = animation
        self.__currentAnimationFrameNumber = 0

    def setAnimationSpeed(self, * , speedInFps):

        self.__currentAnimationSpeed = speedInFps
        self.__currentAnimationFrameTime = 1/speedInFps

    def playAnimation(self , * , time):

        if(self.__currentAnimationName == None):
            raise ValueError(f"No animation was set")

        if(time - self.__previousFrameRenderTime >= self.__currentAnimationFrameTime):
            totalFrames = len(self.__currentAnimation)
            self.__currentAnimationFrameNumber = (self.__currentAnimationFrameNumber + 1)% totalFrames
            currentFrame = self.__currentAnimation[self.__currentAnimationFrameNumber]
            self.setTexture(currentFrame[0])
            self.setColorRegister(colorRegister=currentFrame[1])
            self.setTextureRect(textureRectPosition=currentFrame[2])
            self.setTextureRectDimensions(dimensions=currentFrame[3])
            self.__previousFrameRenderTime = time

        return self.__currentAnimationFrameNumber


    def setVisibility(self , boolean):
        self.__visible = boolean 

    def getVisibility(self):
        return self.__visible


    def getOccupiedCoords(self):
        occupiedCoords = {}
        row , col = self.__texture.textureRectPosition
        width , height= self.__texture.dimensions
        row-=1
        col-=1
        texture2dArray = self.__texture.texture.splitlines()
        for i in range(row , row + height + 1 ):
            for j in range(col , col + width + 1):
                if(self.__visible):
                    occupiedCoords[(self.__position[0]+i - row , self.__position[1]+j - col)] = (texture2dArray[i][j] , self.__texture.colorRegister.get((i - row + 1, j - col + 1) ,"\x1b[0m") , self.__zIndex ) 

        return occupiedCoords



