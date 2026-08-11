
class MainMenu:
    class __Arrow:
        def __loadAssets(self):
            with open("Arrow.txt" , "r" , encoding="utf-8") as file:
                self.__texture = file.read()

        def __initTrackerVariables(self):
            self.__visible = True
            self.__changed = True
            self.__isPointingStart = True  
            self.__lastVisibleTime = 0  

            self.__renderData = [
                [(59 , 12) , (66 , 13) , "\x1b[38;2;255;255;0m"],
                [(59 , 17) , (66 , 18) , "\x1b[38;2;255;255;0m"]
                
            ]

        def __init__(self):
            self.__loadAssets()
            self.__initTrackerVariables()

        def handleInput(self , * ,input , time):
            if(input == b"w" and not (self.__isPointingStart)):
                self.__changed = True
                self.__visible = True
                self.__lastVisibleTime = time
                self.__isPointingStart = True

            elif( input == b"s" and self.__isPointingStart):
                self.__changed = True
                self.__visible = True
                self.__lastVisibleTime = time
                self.__isPointingStart = False

        def update(self , * , time):
            if( time - self.__lastVisibleTime >= 0.53):
                self.__visible = not self.__visible
                self.__lastVisibleTime = time
                self.__changed = True

        def render(self):
            if( self.__visible and self.__changed ):
                if( self.__isPointingStart ):
                    # print("hola1")
                    start = self.__renderData[0][0]
                    end   = self.__renderData[0][1]
                    color = self.__renderData[0][2]

                    width  = end[0] - start[0]
                    height = end[1] - start[1]

                    print(f"\x1b[{start[1]};{start[0]}H" , end = "")
                    print(f"{color}" , end = "")

                    # for i in range(height + 1):
                    #     for j in range(width + 1):
                    #         print(f"\x1b[{start[1] + j};{start[0] + i}H" , end = "")
                    #         print(self.__texture[width*i + j])
                    for i, line in enumerate(self.__texture.splitlines()):
                        print(f"\x1b[{start[1]+i};{start[0]}H{line}", end="")
                    
                    print("\x1b[0m" , end="")

                else:
                    # print("hola2")
                    start = self.__renderData[1][0]
                    end   = self.__renderData[1][1]
                    color = self.__renderData[1][2]

                    width  = end[0] - start[0]
                    height = end[1] - start[1]

                    print(f"\x1b[{start[1]};{start[0]}H" , end = "")
                    print(f"{color}" , end = "")

                    # for i in range(height + 1):
                    #     for j in range(width + 1):
                    #         print(f"\x1b[{start[1] + j};{start[0] + i}H" , end = "")
                    #         print(self.__texture[width*i + j])
                    for i, line in enumerate(self.__texture.splitlines()):
                        print(f"\x1b[{start[1]+i};{start[0]}H{line}", end="")
                    
                    print("\x1b[0m" , end="")

            elif(not self.__visible and self.__changed):
                if( self.__isPointingStart ):
                    # print("hola3")
                    start = self.__renderData[0][0]
                    end   = self.__renderData[0][1]
                    color = self.__renderData[0][2]

                    width  = end[0] - start[0]
                    height = end[1] - start[1]

                    print(f"\x1b[{start[1]};{start[0]}H" , end = "")
                    print("\x1b[38;2;24;24;24m" , end = "")

                    # for i in range(height + 1):
                    #     for j in range(width + 1):
                    #         print(f"\x1b[{start[1] + j};{start[0] + i}H" , end = "")
                    #         print(" " , end = "")
                    for i, line in enumerate(self.__texture.splitlines()):
                        print(f"\x1b[{start[1]+i};{start[0]}H{line}", end="")

                    print("\x1b[0m" , end="")

                else:
                    # print("hola4")
                    start = self.__renderData[1][0]
                    end   = self.__renderData[1][1]
                    color = self.__renderData[1][2]

                    width  = end[0] - start[0]
                    height = end[1] - start[1]

                    print(f"\x1b[{start[1]};{start[0]}H" , end = "")
                    print("\x1b[38;2;24;24;24m" , end = "")

                    # for i in range(height + 1):
                    #     for j in range(width + 1):
                    #         print(f"\x1b[{start[1] + j};{start[0] + i}H" , end = "")
                    #         print(" " , end = "")
                    for i, line in enumerate(self.__texture.splitlines()):
                        print(f"\x1b[{start[1]+i};{start[0]}H{line}", end="")

                    print("\x1b[0m" , end="")

            self.__changed = False 


                    





        

        
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
