import helpers as h

class collisionTest:

    class __rectangle:
        def __init__(self  ,width , height):
            self.width = width
            self.height= height
            self.__goRight = True
            texture = "┌"
            texture += (width - 2) * "─"
            texture += "┐\n"

            for i in range(height - 2):
                texture+="│"
                texture+=(width - 2) *" "
                texture+="│\n"

            texture += "└"
            texture += (width - 2) * "─"
            texture += "┘\n"
            self.height = height
            self.visual = h.Sprite(texture=texture , colorRegister={} , textureRectPosition=(1 , 1)  , dimensions=(width , height) , zIndex = 1)
            self.visual.setPosition((1 , 1))
            self.visual.setCollisionRect(collisionRect=(1 , 1))
            self.visual.setCollisionRectDimensions(dimensions=(width , height))

        def handleInput(self , * , input , time):

            if(input == b"w"):
                currPos = self.visual.getPosition()
                self.visual.setPosition((max(1 , currPos[0] - 1) , currPos[1]))

            elif(input == b"s"):
                currPos = self.visual.getPosition()
                self.visual.setPosition((min(32 - (self.height) + 1 , currPos[0] + 1) , currPos[1]))

        def update(self , * , time):
            currPos = self.visual.getPosition()

            if( currPos[1] >= (162 - (self.width) + 1 ) ):
                self.__goRight = False

            if(currPos[1] <= 1):
                self.__goRight = True

            if(self.__goRight):
                self.visual.setPosition((currPos[0] , currPos[1] + 1))
            else:
                self.visual.setPosition((currPos[0] , currPos[1] - 1))


            return self.visual.getOccupiedCoords()


    def __init__(self , * , windowHandler):
        self.__windowHandler = windowHandler
        self.__box1 = self.__rectangle(4, 2)
        self.__box2 = self.__rectangle(32 , 16)
        self.__box2.visual.setPosition((33 - self.__box2.height , 163 - self.__box2.width))
        self.__selectedBox = 1

    def handleInput(self , * , input , time):

        if(input == b"c"):
            if(self.__selectedBox == 1):
                self.__selectedBox = 2
            elif(self.__selectedBox == 2):
                self.__selectedBox = 1

        else:
            if(self.__selectedBox == 1):
                self.__box1.handleInput(input=input , time=time)
            elif(self.__selectedBox == 2):
                self.__box2.handleInput(input=input , time=time)

    def update(self , * , time):

        coordMap1 = self.__box1.update(time=time)
        coordMap2 = self.__box2.update(time=time)
        self.__box1.visual.setColorRegister(colorRegister={})
        self.__box2.visual.setColorRegister(colorRegister={})

        val1 = self.__box1.visual.getWorldCollisionRect()
        val2 = self.__box2.visual.getWorldCollisionRect()
        boolean = h.isColliding(rect1Pos=val1[0] , rect1Dimensions=val1[1] , rect2Pos=val2[0] , rect2Dimensions=val2[1])
        if(boolean):
            if(self.__selectedBox == 1):
                temp = {}
                for i in range(1 , self.__box1.height + 1):
                    for j in range(1 , self.__box1.width + 1):
                        temp[(i , j)] = "\x1b[38;2;0;0;255m"
                self.__box1.visual.setColorRegister(colorRegister=temp)
            elif(self.__selectedBox == 2):
                temp = {}
                for i in range(1 , self.__box2.height + 1):
                    for j in range(1 , self.__box2.width + 1):
                        temp[(i , j)] = "\x1b[38;2;0;0;255m"
                self.__box2.visual.setColorRegister(colorRegister=temp)

        # handleOccupiedCoords(self , * , occupiedCoords)
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=coordMap1)
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=coordMap2)

    def render(self):
        self.__windowHandler.render()




        




            


        
