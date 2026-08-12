class Sprite:

    class __TextureData:
        def __init__(self, texture , colorRegister=None , * , dimensions):
            self.texture = texture
            self.dimensions = dimensions

            if colorRegister is None:
                self.colorRegister = {}
            else:
                self.colorRegister = colorRegister




    def __init__(self):
        self.__position = None
        self.__previousRenderPosition = None
        self.__textures = {}
        self.__changed = True
        self.__currentTexture = None
        self.__previousTexture = None
        self.__visible = True
        self.__visibilityChanged = True

    def addTexture(self , name , texture , colorRegister=None , * , dimensions):
        self.__textures[name] = self.__TextureData(texture , colorRegister , dimensions=dimensions)

    def setPosition(self , coords):
        if (self.__position != coords):
            self.__previousRenderPosition = self.__position
            self.__position = coords
            self.__changed = True
        else:
            return

    def setTexture(self , textureName):
        if(self.__currentTexture != textureName):
            self.__previousTexture = self.__currentTexture
            self.__currentTexture = textureName
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
            

        if(self.__previousTexture == None):
            self.__previousTexture = self.__currentTexture
            return

        print(f"\x1b[{self.__previousRenderPosition[0]};{self.__previousRenderPosition[1]}H" , end = "")


        print("\x1b[38;2;24;24;24m" , end = "")
        for i, line in enumerate(self.__textures[self.__previousTexture].texture.splitlines() ):
            print(f"\x1b[{self.__previousRenderPosition[0]+i};{self.__previousRenderPosition[1]}H{line}", end="")
        print("\x1b[0m" , end="")

    def eraseCurrent(self):
        print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
        print("\x1b[38;2;24;24;24m" , end = "")
        for i, line in enumerate(self.__textures[self.__currentTexture].texture.splitlines() ):
            print(f"\x1b[{self.__position[0]+i};{self.__position[1]}H{line}", end="")
        print("\x1b[0m" , end="")



    def render(self , forced=False): 
        if( forced or self.__changed ):

            if(self.__changed):
                self.erasePrevious()

            print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
            for row, line in enumerate(self.__textures[self.__currentTexture].texture.splitlines()):
                print(f"\x1b[{self.__position[0]+row};{self.__position[1]}H" , end="")
                for col , char in enumerate(line):
                    # print(f"{self.__textures[self.__currentTexture].colorRegister.get((row,col) ,"\x1b[0m" ) }{char}\x1b[0m",end="")
                    print(f"{self.__textures[self.__currentTexture].colorRegister.get((row,col) , "\x1b[38;2;255;255;0m" ) }{char}\x1b[0m",end="")
            self.__changed = False 
            self.__visible = True

        elif(forced or self.__visibilityChanged):
            if(self.__visible):
                print(f"\x1b[{self.__position[0]};{self.__position[1]}H" , end = "")
                for row, line in enumerate(self.__textures[self.__currentTexture].texture.splitlines()):
                    print(f"\x1b[{self.__position[0]+row};{self.__position[1]}H" , end="")
                    for col , char in enumerate(line):
                        # print(f"{self.__textures[self.__currentTexture].colorRegister.get((row,col) ,"\x1b[0m" ) }{char}\x1b[0m",end="")
                        print(f"{self.__textures[self.__currentTexture].colorRegister.get((row,col) , "\x1b[38;2;255;255;0m" ) }{char}\x1b[0m",end="")
            else:
                self.eraseCurrent()

            self.__visibilityChanged = False    


