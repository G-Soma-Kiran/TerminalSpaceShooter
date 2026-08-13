class Sprite:

    allTextures = {}
    allTexturesByPath = {}

    class __TextureData:
        def __init__(self, texture , * ,  colorRegister , textureRectPositionInTexture , dimensions):
            self.texture = texture
            self.dimensions = (dimensions[0] - 1 , dimensions[1]) #For convinience . just go to the end of line and enter the col - 1 which would be width +1 .so -1 is needed
            self.textureRectPosition = textureRectPositionInTexture

            if colorRegister is None:
                self.colorRegister = {}
            else:
                self.colorRegister = colorRegister




    def __init__(self , name  , * , colorRegister  , textureRectPosition ,  dimensions):
        self.__texture =  self.__TextureData( Sprite.allTextures[name] , colorRegister=colorRegister, textureRectPositionInTexture=textureRectPosition , dimensions=dimensions) 

        self.__position = None
        self.__previousRenderPosition = None

        self.__changed = True

        self.__currentTextureName = name
        self.__previousTextureName = None

        self.__previousTextureRect = None
        self.__previousTextureRectDimensions = None

        self.__previousColorRegister = None

        self.__visible = True
        self.__visibilityChanged = True

    def setPosition(self , coords):
        if (self.__position != coords):
            self.__previousRenderPosition = self.__position
            self.__position = coords
            self.__changed = True
        else:
            return

    def setTexture(self , textureName):
        if(self.__currentTextureName != textureName):
            self.__previousTextureName = self.__currentTextureName
            self.__currentTextureName = textureName
            self.__texture.texture = Sprite.allTextures[textureName]
            self.__changed = True
        else:
            return


    def setTextureRect(self , * , textureRectPosition):
        if( self.__texture.textureRectPosition != textureRectPosition ):
            self.__previousTextureRect = self.__texture.textureRectPosition
            self.__texture.textureRectPosition = textureRectPosition
            self.__changed = True
        else:
            return


    def setTextureRectDimensions(self , * , dimensions):
        if( self.__texture.dimensions != (dimensions[0]-1 , dimensions[1]) ):
            self.__previousTextureRectDimensions = self.__texture.dimensions
            self.__texture.dimensions = (dimensions[0] - 1 , dimensions[1])
            self.__changed = True
        else:
            return

    def setColorRegister(self , * , colorRegister):
        if( self.__texture.colorRegister != colorRegister ):
            self.__previousColorRegister = self.__texture.colorRegister
            self.__texture.colorRegister = colorRegister
            self.__changed = True
        else:
            return

    def toggleVisibility(self):
        self.__visible = not self.__visible
        self.__visibilityChanged = True

    def visibilityHasChanged(self):
        return self.__visibilityChanged


    def erasePrevious(self):
        if(self.__previousRenderPosition == None) : 
            self.__previousRenderPosition = self.__position
            
        if(self.__previousTextureName == None):
            self.__previousTextureName = self.__currentTextureName

        if( self.__previousTextureRect == None):
            self.__previousTextureRect = self.__texture.textureRectPosition

        if( self.__previousTextureRectDimensions == None ):
            self.__previousTextureRectDimensions = self.__texture.dimensions

        if(self.__previousColorRegister == None):
            self.__previousColorRegister = self.__texture.colorRegister
            return

        print(f"\x1b[{self.__previousRenderPosition[0]};{self.__previousRenderPosition[1]}H" , end = "")


        print("\x1b[38;2;24;24;24m" , end = "")

        row , col =  self.__previousTextureRect
        width , height= self.__previousTextureRectDimensions
        row-=1
        col-=1
        texture2dArray = Sprite.allTextures[self.__previousTextureName].splitlines()
        for i in range(row , row + height + 1 ):
            print(f"\x1b[{self.__previousRenderPosition[0]+i - row};{self.__previousRenderPosition[1]}H", end="")
            for j in range(col , col + width + 1):
                print(texture2dArray[i][j] , end="")
        print("\x1b[0m" , end="")

    def eraseCurrent(self):

        print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
        print("\x1b[38;2;24;24;24m" , end = "")
        row , col = self.__texture.textureRectPosition
        width , height= self.__texture.dimensions
        row-=1
        col-=1
        texture2dArray = self.__texture.texture.splitlines()
        for i in range(row , row + height + 1 ):
            print(f"\x1b[{self.__position[0]+i - row};{self.__position[1]}H", end="")
            for j in range(col , col + width + 1):
                print(texture2dArray[i][j] , end="")
        print("\x1b[0m" , end="")


    def render(self , forced=False): 
        if( forced or self.__changed ):

            if(self.__changed):
                self.erasePrevious()

            print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
            row , col = self.__texture.textureRectPosition
            width , height= self.__texture.dimensions
            row-=1
            col-=1
            texture2dArray = self.__texture.texture.splitlines()
            for i in range(row , row + height + 1 ):
                print(f"\x1b[{self.__position[0]+i - row};{self.__position[1]}H", end="")
                for j in range(col , col + width + 1):
                    print(f"{self.__texture.colorRegister.get((i - row + 1 , j - col + 1) ,"\x1b[0m" ) }{texture2dArray[i][j]}\x1b[0m",end="")


            self.__changed = False 
            self.__visible = True

        elif(forced or self.__visibilityChanged):
            if(self.__visible):
                print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
                row , col = self.__texture.textureRectPosition
                width , height= self.__texture.dimensions
                row-=1
                col-=1
                texture2dArray = self.__texture.texture.splitlines()
                for i in range(row , row + height + 1 ):
                    print(f"\x1b[{self.__position[0]+i - row};{self.__position[1]}H", end="")
                    for j in range(col , col + width + 1):
                        print(f"{self.__texture.colorRegister.get((i - row + 1, j - col + 1) ,"\x1b[0m" ) }{texture2dArray[i][j]}\x1b[0m",end="")
            else:
                self.eraseCurrent()

            self.__visibilityChanged = False    


