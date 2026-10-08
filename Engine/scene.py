from abc import ABC , abstractmethod
import Engine._sceneEnums as enm
import Engine._subsystem as subsystem
import Engine.helpers as h

class Scene(ABC):
    def __init__(self, * ,sceneInit:subsystem.SubSystems):
        self.__renderBelow = False
        self.__updateBelow = False

        self.__isPaused= False

        self.__reqs = []

        self.__view = None

        self._systems:subsystem.SubSystems = sceneInit
        self._onCreate()

    @abstractmethod
    def _onCreate(self):
        pass

    def setRenderBelow(self , boolean):
        self.__renderBelow = boolean

    def setUpdateBelow(self , boolean):
        self.__updateBelow = boolean



    def setPause(self , boolean):
        self.__isPaused = boolean
    def getPause(self):
        return self.__isPaused


    def pushScene(self , * , sceneName):
        self.__reqs.append((enm.Request.push , sceneName))

    def popScene(self):
        self.__reqs.append((enm.Request.pop , None))

    def popAndSave(self):
        self.__reqs.append((enm.Request.popAndSave ,None))

    def replaceSceneWith(self,* , sceneName):
        self.__reqs.append((enm.Request.replaceWith , sceneName))

    def switchToScene(self ,* , sceneName):
        self.__reqs.append((enm.Request.switchTo , sceneName))



    def updateHook(self , * , time):
        if(self.__isPaused):
            copy = self.__reqs[:]
            self.__reqs.clear()
            return copy

        self.update(time=time)

        copy = self.__reqs[:]
        self.__reqs.clear()
        return copy

    @abstractmethod
    def update(self , * , time):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handleInput(self , * , input , time):
        pass


    def setView(self , * ,  view):
        self.__view = view

    def getView(self)->h.View:
        return self.__view