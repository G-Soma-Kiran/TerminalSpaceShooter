import helpers as h

class MainMenu:
    class __Arrow:
        def __loadAssets(self):
            with open("Arrow.txt" , "r" , encoding="utf-8") as file:
                self.visual.addTexture("arrow" , file.read() , dimensions=(7 , 1))
                self.visual.setPosition((12 , 59))
                self.visual.setTexture("arrow")

        def __initTrackerVariables(self):  
            self.__lastVisibleTime = 0  
            # self.__renderData = [
            #     [(59 , 12) , (66 , 13) , "\x1b[38;2;255;255;0m"],
            #     [(59 , 17) , (66 , 18) , "\x1b[38;2;255;255;0m"]
                
            # ]

        def __init__(self):
            self.visual = h.Sprite()
            self.__loadAssets()
            self.__initTrackerVariables()

        def handleInput(self , * ,input , time):
            if(input == b"w"):
                self.visual.setPosition((12 , 59))
                self.__lastVisibleTime = time
            elif(input == b"s"):
                self.visual.setPosition((17 , 59))
                self.__lastVisibleTime = time

        def update(self , * , time):
            if( time - self.__lastVisibleTime >= 0.59):
                self.visual.toggleVisibility()
                self.__lastVisibleTime = time

        def render(self):
            self.visual.render() 


                    





        

        
    def __loadAssets(self):
        with open("MainMenuNill.txt" , "r" , encoding="utf-8") as file:
            self.__nillTexture = file.read()
        

    def __init__(self):
        self.__loadAssets()
        self.__arrow = self.__Arrow()
        self.__notRenderedEvenOnce = True

    def handleInput(self , * , input , time):
        self.__arrow.handleInput(input=input , time=time)
        
    def update(self , * , time):
        self.__arrow.update(time=time)

    def render(self):
        if( self.__notRenderedEvenOnce ):
            print("\033[H\033[J", end="")
            print(self.__nillTexture , end="")
            self.__notRenderedEvenOnce = False

        self.__arrow.render()
