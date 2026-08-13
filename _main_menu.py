import helpers as h

class MainMenu:
    class __Arrow:

        def __initTrackerVariables(self):  
            self.__lastVisibleTime = 0  

        def __init__(self):
            self.visual = h.Sprite("arrow" , colorRegister={} , textureRectPosition=(1 , 1) , dimensions=(7 , 1))
            self.visual.setPosition((12  , 59))
            temp={}
            for i in range(1 , 3):
                for j in range(1 , 8):
                    temp[(i , j)] =  "\x1b[38;2;255;255;0m"
            self.visual.setColorRegister(colorRegister=temp)
            self.__initTrackerVariables()

        def handleInput(self , * ,input , time):
            if(input == b"w"):
                self.visual.setPosition((12 , 59))
                self.__lastVisibleTime = time
            elif(input == b"s"):
                self.visual.setPosition((17 , 59))
                self.__lastVisibleTime = time
            elif(input == b"a"):
                self.visual.setTextureRect(textureRectPosition=(3 , 1))
            elif(input == b"d"):
                self.visual.setTextureRect(textureRectPosition=(1 , 1))
                

        def update(self , * , time):
            if( time - self.__lastVisibleTime >= 0.59):
                self.visual.toggleVisibility()
                self.__lastVisibleTime = time

        def render(self):
            self.visual.render() 


                    





        

    def __init__(self):
        temp = {}
        for i in range(1 , 33):
            for j in range(1 , 165):
                temp[(i , j)] = "\x1b[0m"
      
        self.visual = h.Sprite("main_menu_nill" , colorRegister=temp , textureRectPosition=(1 , 1) , dimensions=(162 , 31))
        self.visual.setPosition((1 , 1))
        self.__arrow = self.__Arrow()

    def handleInput(self , * , input , time):
        self.__arrow.handleInput(input=input , time=time)
        
    def update(self , * , time):
        self.__arrow.update(time=time)

    def render(self):
        self.visual.render()
        self.__arrow.render()
