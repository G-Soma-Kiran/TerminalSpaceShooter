import time as T
import msvcrt as Input
import _main_menu as m
import sys


main_menu = m.MainMenu()
loopStart = T.perf_counter()
while(True):
    frameStart = T.perf_counter()
    
    while( Input.kbhit()):
        key = Input.getch()
        main_menu.handleInput(input=key , time=(T.perf_counter() - loopStart))

    main_menu.update(time=(T.perf_counter()- loopStart))
    main_menu.render()
    print(f"\x1b[162;1H", end="")
    sys.stdout.flush()
    frameEnd = T.perf_counter()
    if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.016 ):
        T.sleep(0.016 - (frameEnd - frameStart))


