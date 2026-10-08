class AssetManager:

        def __init__(self):
            self.__allTextures = {}
            self.__allTexturesByPath = {}

        def importTextures(self , **kwargs):
            for textureName , filepath in kwargs.items():
                if( textureName in self.__allTextures ):
                    raise ValueError(f"{textureName} is already assetManager.__allTextures")


                temp = self.__allTexturesByPath.get(filepath)

                if( temp != None ):
                    self.__allTextures[textureName] = self.__allTexturesByPath[filepath]
                    continue

                with open(filepath , "r" , encoding="utf-8") as file:
                    temp = file.read()
                    self.__allTextures[textureName] = temp
                    self.__allTexturesByPath[filepath] = temp

        def getTexture(self , * , textureName):
            val = self.__allTextures.get(textureName)

            if(val == None):
                raise ValueError(f"{textureName} is not present => getTexture()")
            
            return val
        