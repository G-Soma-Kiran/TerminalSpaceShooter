import Engine.helpers as h

class PauseScene:
    def renderBelow(self):
        return self.__renderBelow
                
    def updateBelow(self):
        return self.__updateBelow

    def __init__(self , * , windowHandler , assetManager , animationRegistry):
        self.__renderBelow = True
        self.__updateBelow = False

        self.__windowHandler = windowHandler
        self.__assetManager = assetManager
        self.__animationRegistry = animationRegistry

        self.__reqs = []
        

    def handleInput(self , * , input , time):
        pass

    def update(self , * , time):
        copy = self.__reqs[:]
        self.__reqs.clear()
        return copy

    def render(self):
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.border.getOccupiedCoords())
        self.__windowHandler.render()