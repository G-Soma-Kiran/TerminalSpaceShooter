import Engine.engine as eng
import Games._main_menu as m
import Games.collisionTest as collision
import Games.BrickBreaker as brick
import Games.TicTacToe as tik
import Games.pauseScene as p
import Games.Tetris as tetris


game = eng.Game(defaultScene="Tetris")

game.assetManager.importTextures(arrow="./Assets/Textures/Arrow.txt" , main_menu_nill="./Assets/Textures/MainMenuNill.txt" , BB="./Assets/Textures/brickBreaker.txt" , tic="./Assets/Textures/tictactoe.txt" , pause="./Assets/Textures/pause.txt" )
game.sceneManager.registerScene(tik.TikTakToe , m.MainMenu , collision.collisionTest , brick.BrickBreaker , p.PauseScene , tetris.Tetris)

game.run()