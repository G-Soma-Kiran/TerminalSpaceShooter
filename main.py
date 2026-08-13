import time as T
import msvcrt as Input


def run():
    with open("MainMenuStart.txt" , "r" , encoding="utf-8") as file:
        mainmenu_start = file.read()
    with open("MainMenuHelp.txt" , "r" , encoding="utf-8") as file:
        mainmenu_help = file.read()
    with open("MainMenuNill.txt" , "r" , encoding="utf-8") as file:
        mainmenu_nill = file.read()
    fileOption = mainmenu_start

    renderStart = T.perf_counter()
    lastVisibleTime = renderStart
    visible = True
    changed = False
    while(True):
        frameStart = T.perf_counter()
        while( Input.kbhit()):
            key = Input.getch()
            if(key == b"w" and fileOption!=mainmenu_start):
                fileOption = mainmenu_start
                changed = True
                visible = True
                lastVisibleTime = T.perf_counter()
            elif( key == b"s" and fileOption!=mainmenu_help):
                fileOption = mainmenu_help
                changed = True
                visible = True
                lastVisibleTime = T.perf_counter()
            elif( key == b'\x1b'):
                print("\033[H\033[J", end="")
                return

        now = T.perf_counter()
        if(now - lastVisibleTime >= 0.5):
            visible = not visible
            lastVisibleTime = now
            changed = True


        if(visible and changed):
            print("\033[H\033[J", end="")
            print(fileOption , end="")
            changed = False
        elif((not visible) and changed):
            print("\033[H\033[J", end="")
            print(mainmenu_nill , end="")
            changed = False



        frameEnd = T.perf_counter()
        if((frameEnd - frameStart) > 0 and (frameEnd - frameStart) < 0.016 ):
            T.sleep(0.016 - (frameEnd - frameStart))



run()