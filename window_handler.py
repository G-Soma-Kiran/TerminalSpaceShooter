class WindowHandler:
    def __init__(self):
        self.__previousRenderMap = None
        self.__currentRenderMap = {}
        self.__desiredTerminalSize = (162 , 32)
        self.__currentTerminalSize = None
        self.__cooldownTimeForRedraw = None
        self.__hold = False

    def handleOccupiedCoords(self , * , occupiedCoords):
        terminalOffsetX , terminalOffsetY = (self.__desiredTerminalSize[0] - self.__currentTerminalSize[0] , self.__desiredTerminalSize[1] - self.__currentTerminalSize[1])
        for coord , val in occupiedCoords.items():
            terminalRelatedX = coord[0] - terminalOffsetY
            terminalRelatedY = coord[1] - terminalOffsetX

            if( terminalRelatedX <= 0 or terminalRelatedY <= 0) : continue

            if( self.__currentRenderMap.get((terminalRelatedX , terminalRelatedY)) != None ):
                if(self.__currentRenderMap.get((terminalRelatedX , terminalRelatedY))[2] <= val[2]):
                    self.__currentRenderMap[(terminalRelatedX , terminalRelatedY)] = val
            else:
                self.__currentRenderMap[(terminalRelatedX , terminalRelatedY)] = val
            
    
    
    
    def handleTerminalSizeChange(self , * ,  terminalSize , time):
        if(terminalSize != self.__currentTerminalSize):
            self.__currentTerminalSize = terminalSize
            self.__hold = True
            self.__cooldownTimeForRedraw = None
            print("\033[H\033[J", end="")
            self.__previousRenderMap = None
        elif(self.__hold and self.__cooldownTimeForRedraw == None):
            self.__cooldownTimeForRedraw = time
        elif(self.__hold ):
            if(time - self.__cooldownTimeForRedraw >= 0.2):
                self.__hold = False
                self.__cooldownTimeForRedraw = None
                return True
        return False

    def render(self):
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