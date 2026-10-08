class Animations:
        def __init__(self):
            self.__allAnimations= {}

        def createAnimation(self , * , animationName ):
            if(animationName in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is already in animationRegistry.allAnimations")
    
            self.__allAnimations[animationName] = []

        def addFrame(self , * , animationName , texture , colorRegister , textureRect , dimensions):
            if(animationName not in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is not in animationRegistry.addFrame")
            self.__allAnimations[animationName].append((texture , colorRegister , textureRect , dimensions))

        def getAnimation(self , * , animationName):
            if(animationName not in self.__allAnimations.keys()):
                raise ValueError(f"{animationName} is not in animationRegistry.addFrame")
            return tuple(self.__allAnimations[animationName])