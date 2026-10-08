import Engine.engine as eng
import Games._main_menu as m
import Games.collisionTest as collision
import Games.BrickBreaker as brick
import Games.TicTacToe as tik
import Games.pauseScene as p
import Games.Tetris as tetris
import Games.FlappyBird as fb


game = eng.Game(defaultScene="FlappyBird" , viewSize=(162,32))

game.subsystems.getAssetManager().importTextures(arrow="./Assets/Textures/Arrow.txt" , main_menu_nill="./Assets/Textures/MainMenuNill.txt" , BB="./Assets/Textures/brickBreaker.txt" , tic="./Assets/Textures/tictactoe.txt" , pause="./Assets/Textures/pause.txt" ,FlappyBird="./Assets/Textures/FlappyBird.txt")
game.registerScene(tik.TikTakToe , m.MainMenu , collision.collisionTest , brick.BrickBreaker , p.PauseScene , tetris.Tetris , fb.FlappyBird)

game.run()