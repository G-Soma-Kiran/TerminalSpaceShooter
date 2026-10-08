import Engine._sceneEnums as enm


class SceneManager:
        
        def __init__(self , * ,defaultScene, subsystems):
            self.__windowHandler = subsystems.getWindow()
            self.__assetManager = subsystems.getAssetManager()
            self.__animationRegistry = subsystems.getAnimationRegistry()
            self.__sceneStack = []
            self.__requests = [(enm.Request.push , defaultScene)]
            self.__sceneRegistry = {}
            self.__persistentScenes = {}
            self.__subsystems = subsystems

        def registerScene(self , *args):
            for scene in args:
                if(scene.__name__ in self.__sceneRegistry.keys()):
                    raise ValueError(f"{scene} already exists in sceneRegistry")
                self.__sceneRegistry[scene.__name__] = scene
            

        def __createScene(self , * , sceneName):
            return self.__sceneRegistry[sceneName](sceneInit=self.__subsystems)
        
        def __push(self , * , sceneName):
            if(self.__persistentScenes.get(sceneName) != None ):
                self.__sceneStack.append(self.__persistentScenes.pop(sceneName))
            else:
                self.__sceneStack.append(self.__createScene(sceneName=sceneName))

        def __pop(self):
            self.__sceneStack.pop()

        def __saveAndPop(self):
            self.__persistentScenes[type(self.__sceneStack[-1]).__name__] = self.__sceneStack[-1]
            self.__sceneStack.pop()

        def __replaceWith(self , * , sceneName):
            self.__pop()
            self.__push(sceneName=sceneName)

        def __switchTo(self , *,sceneName):
            self.__saveAndPop()
            self.__push(sceneName=sceneName)

        def completeRequests(self):
            for request , scene in self.__requests:
                if(request == enm.Request.push):
                    self.__push(sceneName=scene)
                elif(request == enm.Request.pop):
                    self.__pop()
                elif(request == enm.Request.popAndSave ):
                    self.__saveAndPop()
                elif(request == enm.Request.replaceWith):
                    self.__replaceWith(sceneName=scene)
                elif(request == enm.Request.switchTo):
                    self.__switchTo(sceneName=scene)
                else:
                    raise ValueError(f"Unknown scene request: {request}")

            self.__requests.clear()

        def updateScene(self , * , keys , time):
            for key , t in keys:
                self.__sceneStack[-1].handleInput(input=key , time=t)


            i=len(self.__sceneStack)-1
            while(i > 0 and self.__sceneStack[i].updateBelow()):
                i=i-1
            while(i < len(self.__sceneStack)-1):
                self.__sceneStack[i].updateHook(time=time)
                i+=1
            reqs = self.__sceneStack[-1].updateHook(time = time)
            self.__requests.extend(reqs)

            i=len(self.__sceneStack)-1
            while(i > 0 and self.__sceneStack[i].renderBelow()):
                i-=1
            while(i < len(self.__sceneStack)):
                if(self.__sceneStack[i].getView() is None):
                    self.__windowHandler._WindowHandler__setView(view=self.__windowHandler.getDefaultView())
                else:
                    self.__windowHandler._WindowHandler__setView(view=self.__sceneStack[i].getView())


                self.__sceneStack[i].render()
                i+=1

            self.__windowHandler._WindowHandler__show()
            self.__windowHandler._WindowHandler__setView(view=self.__windowHandler.getDefaultView())


        def isSceneStackEmpty(self):
            return len(self.__sceneStack) == 0