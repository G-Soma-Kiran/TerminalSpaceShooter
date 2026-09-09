import helpers as h
import random
import sys

BRICK_TEXTURE_RECT_POS = (1,1)
BALL_TEXTURE_RECT_POS = (2,1)
PADDLE_TEXTURE_RECT_POS = (3 , 1)

class BrickBreaker:


    class Brick:
        def __init__(self , * , texture , width , height , color , position , hitpoints):
            temp={}
            for i in range(1 , height + 1):
                for j in range(1 , width + 1):
                    temp[(i , j)] = f"{color}"

            self.visual = h.Sprite(texture=texture  , colorRegister=temp, textureRectPosition=BRICK_TEXTURE_RECT_POS , dimensions=(width , height) , zIndex = 1)
            self.visual.setPosition(position)
            self.visual.setCollisionRect(collisionRect=(1 , 1))
            self.visual.setCollisionRectDimensions(dimensions=(width , height))
            self.__hitpoints = hitpoints

        def isAlive(self):
            return self.__hitpoints > 0

        def gotHit(self):
            self.__hitpoints -= 1

        def update(self , * , time):
            return self.visual.getOccupiedCoords()
                
    class Ball:
        def __init__(self , * , texture):
            self.visual = h.Sprite(texture=texture , colorRegister={} , textureRectPosition=BALL_TEXTURE_RECT_POS , dimensions=(1 , 1) , zIndex=1)
            self.visual.setPosition((26 , 80))
            self.velocity = (1,1)    
            self.visual.setCollisionRect(collisionRect=(1 , 0))
            self.visual.setCollisionRectDimensions(dimensions=(3 , 1))
                        

        def update(self , * , time):


            currPos = self.visual.getPosition()
            if(currPos[0] >= 31 or currPos[0] <= 1):
                currVelocity = self.velocity
                self.velocity = (-currVelocity[0] , currVelocity[1])

            if(currPos[1] >= 161 or currPos[1] <= 1):
                currVelocity = self.velocity
                self.velocity = (currVelocity[0] , -currVelocity[1])
            
            self.visual.setPosition((currPos[0] + self.velocity[0] , currPos[1] + self.velocity[1]))
            return self.visual.getOccupiedCoords()         

    class Paddle:
        def __init__(self , * , texture):
            self.visual = h.Sprite(texture=texture , colorRegister={} , textureRectPosition=PADDLE_TEXTURE_RECT_POS , dimensions=(14 , 1) , zIndex=1)
            self.visual.setPosition((27 , 74))
            self.visual.setCollisionRect(collisionRect=(1,1))
            self.visual.setCollisionRectDimensions(dimensions=(14 , 1))

        def update(self , * , time):
            return self.visual.getOccupiedCoords()

        def handleInput(self , * , input , time):
            if(input == b"a"):
                currPos = self.visual.getPosition()
                self.visual.setPosition((currPos[0] , max(currPos[1] - 4 , 1)))
            elif(input == b"d"):
                currPos = self.visual.getPosition()
                self.visual.setPosition((currPos[0] , min(currPos[1] + 4 , 162 - 14)))


    def __init__(self , * , windowHandler , assetManager):
        self.__windowHandler = windowHandler
        self.__assetManager = assetManager
        self.__ball = self.Ball(texture=self.__assetManager.getTexture(textureName="BB"))
        # self.__brick = self.Brick(texture=self.__assetManager.getTexture(textureName="BB") , width=14 , height=1 , color="\x1b[38;2;255;255;0m" , position=(3 , 30) , hitpoints=3)
        self.__paddle = self.Paddle(texture=self.__assetManager.getTexture(textureName="BB"))
        self.__bricks = []
        probabilities = {
            4: 0.25,
            5: 0.20,
            6: 0.17,
            7: 0.14,
            8: 0.11,
            9: 0.08,
            10: 0.05
        }    


        colors = [
            "\x1b[38;2;255;80;80m",     # Red
            "\x1b[38;2;255;160;60m",    # Orange
            "\x1b[38;2;255;220;70m",    # Yellow
            "\x1b[38;2;100;220;100m",   # Green
            "\x1b[38;2;60;220;220m",    # Cyan
            "\x1b[38;2;80;160;255m",    # Blue
            "\x1b[38;2;150;100;255m",   # Purple
            "\x1b[38;2;240;100;200m",   # Pink
        ]

        rows = 20
        cols = 162
        rightSpace = 1
        downSpace = 1

        currRow = 1
        currColumn = 1
        while(currRow<=rows):
            currColumn = 1
            while(currColumn <= cols):
                acceptedSizes = list(range(4, min(162 - currColumn, 11)))
                if(len(acceptedSizes) == 0):
                    break
    
                choice = random.choices(
                    acceptedSizes,
                    weights=[probabilities[i] for i in acceptedSizes],
                    k=1
                )[0]
    
                colour = colors[random.randint(0 , len(colors) - 1)]
    
                self.__bricks.append(BrickBreaker.Brick(texture=self.__assetManager.getTexture(textureName="BB") , width=choice , height=1 , color=colour , position=(currRow , currColumn) , hitpoints=1))
                currColumn+=choice
                currColumn+=rightSpace
            currRow+=1
            currRow+=downSpace

    def handleInput(self , * , input , time):
        self.__paddle.handleInput(input=input , time=time)
    
    def update(self , * , time):
        
        # self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__brick.update(time=time))
        for brick in self.__bricks:
            val1 = self.__ball.visual.getWorldCollisionRect()
            val2 = brick.visual.getWorldCollisionRect()
            boolean = h.isColliding(rect1Pos=val1[0] , rect1Dimensions=val1[1] , rect2Pos=val2[0] , rect2Dimensions=val2[1])
            if(boolean):
                brick.gotHit()
                # if(self.__ball.visual.getPosition()[0] == brick.visual.getPosition()[0]):
                #     self.__ball.velocity = (-self.__ball.velocity[0] , self.__ball.velocity[1])
                # else:
                #     self.__ball.velocity = (self.__ball.velocity[0] , -self.__ball.velocity[1])
                ballRect = self.__ball.visual.getWorldCollisionRect()
                brickRect = brick.visual.getWorldCollisionRect()
                ballPos, ballDim = ballRect
                brickPos, brickDim = brickRect

                overlapRow = min(ballPos[0] + ballDim[1], brickPos[0] + brickDim[1]) - max(ballPos[0], brickPos[0])
                overlapCol = min(ballPos[1] + ballDim[0], brickPos[1] + brickDim[0]) - max(ballPos[1], brickPos[1])

                if overlapRow < overlapCol:
                    self.__ball.velocity = (-self.__ball.velocity[0], self.__ball.velocity[1])
                else:
                    self.__ball.velocity = (self.__ball.velocity[0], -self.__ball.velocity[1])
                # break  # prevent double-flip if multiple bricks overlap this frame


        val1 = self.__ball.visual.getWorldCollisionRect()
        val2 = self.__paddle.visual.getWorldCollisionRect()
        if(h.isColliding(rect1Pos=val1[0] , rect1Dimensions=val1[1] , rect2Pos=val2[0] , rect2Dimensions=val2[1])):
            currVelocity = self.__ball.velocity
            self.__ball.velocity = (-currVelocity[0] , currVelocity[1] )

        i=0
        while(i < len(self.__bricks)):
            if(not self.__bricks[i].isAlive()):
                self.__bricks[i] , self.__bricks[-1] =  self.__bricks[-1] , self.__bricks[i] 
                self.__bricks.pop()
            else:
                i+=1


        for brick in self.__bricks:
            self.__windowHandler.handleOccupiedCoords(occupiedCoords=brick.update(time=time))
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__ball.update(time=time))
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__paddle.update(time=time))

    def render(self):
        self.__windowHandler.render()


    
    

    



# def createLevel(* , probabillities , rows , cols , colors , listOfBricks):

    


 