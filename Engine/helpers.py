#width  is number of charecters horizontally
#height is number of charecters vertically

class Sprite:

    class __TextureData:
        def __init__(self, texture , * ,  colorRegister , textureRectPositionInTexture , dimensions):
            self.texture = texture
            self.dimensions = (dimensions[0] , dimensions[1])
            self.textureRectPosition = textureRectPositionInTexture
            self.colorRegister = colorRegister




    def __init__(self , texture  , * , colorRegister  , textureRectPosition ,  dimensions , zIndex):
        self.__texture =  self.__TextureData( texture , colorRegister=colorRegister, textureRectPositionInTexture=textureRectPosition , dimensions=dimensions) 

        self.__position = None

        self.__visible = True
        self.__transparent = False

        self.__currentAnimation = None
        self.__currentAnimationSpeed = 24
        self.__previousFrameRenderTime = 0
        self.__currentAnimationFrameNumber = 0

        self.__zIndex = zIndex

        self.__collisionRect = None
        self.__collisionRectDimensions = None

    def setPosition(self , coords : tuple[float, float]) -> None:
        self.__position = coords

    def getPosition(self):
        return self.__position

    def setTexture(self , texture):
        self.__texture.texture = texture


    def setTextureRect(self , * , textureRectPosition):
        self.__texture.textureRectPosition = textureRectPosition


    def setTextureRectDimensions(self , * , dimensions : tuple):
        self.__texture.dimensions = (dimensions[0] , dimensions[1])

    def getDimensions(self):
        return self.__texture.dimensions

    def setColorRegister(self , * , colorRegister : dict  , defaultColor : str ="\x1b[0m"):
        for i in range(1 , self.__texture.dimensions[1]+1):
            for j in range(1 , self.__texture.dimensions[0]+1):
                if(colorRegister.get((i , j)) == None):
                    colorRegister[(i , j)] = defaultColor

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

    def setTransparency(self , boolean):
        self.__transparent = boolean


    def getOccupiedCoords(self):
        occupiedCoords = {}
        row , col = self.__texture.textureRectPosition
        width , height= self.__texture.dimensions
        row-=1
        col-=1
        texture2dArray = self.__texture.texture.splitlines()
        for i in range(row , row + height ):
            for j in range(col , col + width ):
                if(self.__visible and (not self.__transparent or texture2dArray[i][j] != " ")):
                    occupiedCoords[(self.__position[0]+i - row , self.__position[1]+j - col)] = (texture2dArray[i][j] , self.__texture.colorRegister.get((i - row + 1, j - col + 1) ,"\x1b[0m") , self.__zIndex ) 

        return occupiedCoords


    def setCollisionRect(self , * , collisionRect : tuple):
        self.__collisionRect = collisionRect

    def setCollisionRectDimensions(self , * , dimensions : tuple):
        self.__collisionRectDimensions = dimensions

    def hasCollision(self):
        if(self.__collisionRect == None or self.__collisionRectDimensions == None) : return False
        return True

    def getWorldCollisionRect(self):
        return (  (self.__collisionRect[0] + self.__position[0] - 1 , self.__collisionRect[1] + self.__position[1] - 1) , (self.__collisionRectDimensions[0]  , self.__collisionRectDimensions[1])   )

    def getLocalCollisionRect(self):
        return (self.__collisionRect , self.__collisionRectDimensions)

def isColliding(* , rect1Pos , rect1Dimensions , rect2Pos , rect2Dimensions ):
    #Pos = (row , column)
    #dimension = (width , height)

    flag1 = abs(rect1Pos[0] - rect2Pos[0]) < (rect1Dimensions[1] if(rect1Pos[0] <= rect2Pos[0]) else rect2Dimensions[1])
    flag2 = abs(rect1Pos[1] - rect2Pos[1]) < (rect1Dimensions[0] if(rect1Pos[1] <= rect2Pos[1]) else rect2Dimensions[0])

    return flag1 and flag2

def color(R ,G , B):
    return f"\x1b[38;2;{R};{G};{B}m"


def rectangle(* , dimensions):
    boxWidth = dimensions[0]
    boxHeight = dimensions[1]
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



class View:

    def __init__(self , * , viewPosition , viewDimensions , viewPortPos , viewPortDimensions):
        self.__viewPosition = viewPosition
        self.__viewDimensions = viewDimensions
        self.__viewPortPos = viewPortPos
        self.__viewPortDimensions = viewPortDimensions

    def getViewPosition(self):
        return self.__viewPosition
    
    def getViewDimensions(self):
        return self.__viewDimensions
    
    def getViewPortPosition(self):
        return self.__viewPortPos
    
    def getViewPortDimensions(self):
        return self.__viewPortDimensions

    def setViewPosition(self , * , viewPosition):
        self.__viewPosition = viewPosition

    def setViewPortPosition(self ,* , viewPortPosition) :
        self.__viewPortPos = viewPortPosition

    def setViewDimensions(self , * , viewDimensions):
        self.__viewDimensions = viewDimensions

    def setViewPortDimensions(self , * , viewPortDimensions):
        self.__viewPortDimensions = viewPortDimensions

    def moveView(self , * , dx , dy):
        currViewPos = self.__viewPosition
        self.setViewPosition(viewPosition=(currViewPos[0] + dx , currViewPos[1] + dy))

    def moveViewPort(self , * , dx , dy):
        currViewPortPos = self.__viewPortPos
        self.setViewPortPosition(viewPortPosition=(currViewPortPos[0] + dx , currViewPortPos[1] + dy))

