import Engine.helpers as h
from enum import Enum

class windowState(Enum):
    ResizingStart=0
    isResizing=1
    ResizingEnd=2
    NoResize=3

class WindowHandler:
    def __init__(self , * , viewSize):  
        self.__previousRenderMap = None
        self.__currentRenderMap = {}
        # self.__desiredTerminalSize = (162 , 32)
        self.__currentTerminalSize = None
        self.__cooldownTimeForRedraw = None
        self.__hold = False
        self.__view : h.View = h.View(viewPosition=(1,1) , viewDimensions=viewSize , viewPortPos=(1,1) , viewPortDimensions=viewSize)

    def __setView(self , * , view):
        self.__view = view

    def __getView(self):
        return self.__view

    def getDefaultView(self):
        return h.View(viewPosition=(1,1) , viewDimensions=self.__currentTerminalSize , viewPortPos=(1,1) , viewPortDimensions=self.__currentTerminalSize)
    
    def getWindowSize(self):
        return self.__currentTerminalSize

    def draw(self , * , occupiedCoords):
        currentWidth , currentHeight = self.__currentTerminalSize

        viewPos = self.__view.getViewPosition()
        viewDims = self.__view.getViewDimensions()
        viewPortPos =self.__view.getViewPortPosition()
        viewPortDims = self.__view.getViewPortDimensions()

        for coord , val in occupiedCoords.items():
            viewSpaceX = coord[0] - viewPos[0] + 1
            viewSpaceY = coord[1] - viewPos[1] + 1

            if(viewSpaceX <= 0 or viewSpaceX > viewDims[1]): continue
            if(viewSpaceY <= 0 or viewSpaceY >  viewDims[0]): continue


            if(viewSpaceX > viewPortDims[1] or viewSpaceY > viewPortDims[0]): continue

            viewPortSpaceX = viewSpaceX - 1 + viewPortPos[0]
            viewPortSpaceY = viewSpaceY - 1 + viewPortPos[1]

            if(viewPortSpaceX <= 0 or viewPortSpaceX > (currentHeight)): continue
            if(viewPortSpaceY <= 0 or viewPortSpaceY > (currentWidth)): continue

            key = (viewPortSpaceX , viewPortSpaceY)
            existing = self.__currentRenderMap.get(key)
            if(existing is None or existing[2] <= val[2]):
                self.__currentRenderMap[key] = val  
    
    
    
    def __handleTerminalSizeChange(self , * ,  terminalSize , time):
        if(terminalSize != self.__currentTerminalSize):
            self.__currentTerminalSize = terminalSize
            self.__hold = True
            self.__cooldownTimeForRedraw = None
            print("\033[H\033[J", end="" , flush=True)
            self.__previousRenderMap = None
            return windowState.ResizingStart
        elif(self.__hold and self.__cooldownTimeForRedraw == None):
            self.__cooldownTimeForRedraw = time
            return windowState.isResizing
        elif(self.__hold ):
            if(time - self.__cooldownTimeForRedraw >= 0.2):
                self.__hold = False
                self.__cooldownTimeForRedraw = None
                return windowState.ResizingEnd
            return windowState.isResizing
        return windowState.NoResize

    def __show(self):
        needToRender = {}

        if(self.__previousRenderMap == None):
            needToRender = self.__currentRenderMap
        else:
            for coord in self.__previousRenderMap:
                if(coord not in self.__currentRenderMap):
                    needToRender[coord] = (" " , "\x1b[0m" , 100)

            for coord , val in  self.__currentRenderMap.items():
                if(self.__previousRenderMap.get(coord) != val):
                    needToRender[coord] = val

        stringToPrintThisFrame = ""
        for coord , val in needToRender.items():
            stringToPrintThisFrame += f"\x1b[{coord[0]};{coord[1]}H"
            stringToPrintThisFrame += f"{val[1]}"
            stringToPrintThisFrame += f"{val[0]}"
            stringToPrintThisFrame += "\x1b[0m"
        self.__previousRenderMap = self.__currentRenderMap
        self.__currentRenderMap = {}

        print(stringToPrintThisFrame , end="")