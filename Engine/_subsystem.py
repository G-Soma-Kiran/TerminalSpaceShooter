import Engine._window_handler as window
import Engine._asset_manager as asset
import Engine._animation_registry as animations

class SubSystems:
    def __init__(self , * , windowHandler:window.WindowHandler , assetManager:asset.AssetManager , animationRegistry:animations.Animations):
        self.__windowHandler = windowHandler
        self.__assetmanager = assetManager
        self.__animationsRegistry = animationRegistry 

    def getWindow(self)->window.WindowHandler:
        return self.__windowHandler

    def getAssetManager(self)->asset.AssetManager:
        return self.__assetmanager

    def getAnimationRegistry(self)->animations.Animations:
        return self.__animationsRegistry
