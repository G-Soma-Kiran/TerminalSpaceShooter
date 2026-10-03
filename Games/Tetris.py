import Engine.helpers as h
from enum import Enum
import random as rnd

_GRID_SIZE = (40, 26)      # (width in CHARACTERS, height in ROWS). One cell = 2 chars wide, 1 row tall.
_GRID_POS = ()             # terminal (row, col) of the board's top-left, set in Tetris.__init__

_SPAWN_ROW = 1             # spawn row, relative to the top of the board (piece is visible immediately).Value is set to 1 beacuse all pieces have pivot as the second block. Although Z and S have a problem with this.
_GRAVITY_BASE = 0.5        # seconds per automatic step down at level 1
_GRAVITY_MIN = 0.05        # fastest allowed fall interval
_CLEAR_FLASH_TIME = 0.2    # how long cleared rows flash white
_LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}   # multiplied by level , score shi

_WHITE = h.color(255, 255, 255)
_GHOST_COLOR = h.color(90, 90, 90)
_DOT_COLOR = h.color(60, 60, 60)
_HUD_COLOR = h.color(200, 200, 200)
_HINT_COLOR = h.color(120, 120, 120)
_OVER_COLOR = h.color(255, 80, 80)


def shade(rgb, k):
    """rgb tuple -> ANSI color string, brightness scaled by k."""
    return h.color(*(min(255, int(v * k)) for v in rgb))


def _text(row, col, s, color, z=1, solid=False):
    """Text as an occupiedCoords dict. solid=True also draws the spaces (to blank what is behind)."""
    return {(row, col + i): (ch, color, z) for i, ch in enumerate(s) if solid or ch != " "}

class BlockType(Enum):
    L = 1
    J = 2
    Z = 3
    S = 4
    I = 5
    T = 6
    O = 7


_SHAPES = {
    BlockType.L: [(-1, 0), (0, 0), (1, 0), (1, 2)],
    BlockType.J: [(-1, 0), (0, 0), (1, 0), (1, -2)],
    BlockType.Z: [(0, -2), (0, 0), (1, 0), (1, 2)],
    BlockType.S: [(0, 0), (0, 2), (1, -2), (1, 0)],
    BlockType.I: [(-1, 0), (0, 0), (1, 0), (2, 0)],
    BlockType.T: [(0, -2), (0, 0), (0, 2), (1, 0)],
    BlockType.O: [(0, 0), (0, -2), (1, -2), (1, 0)],
}

# The I piece should not be set as a single center , if that is done then its movement is trash.
# It just flips between these two fixed states instead.
_I_STATES = (
    [(-1, 0), (0, 0), (1, 0), (2, 0)],
    [(0, -2), (0, 0), (0, 2), (0, 4)],
)

_COLORS = {
    BlockType.L: (245, 130, 20),
    BlockType.J: (40, 90, 220),
    BlockType.Z: (220, 40, 50),
    BlockType.S: (0, 200, 80),
    BlockType.I: (0, 220, 220),
    BlockType.T: (160, 60, 220),
    BlockType.O: (245, 220, 0),
}


class Tetris:

    class Block:

        class CollisionType(Enum):
            NoCollision = 0
            LeftOutOfBounds = 1
            RightOutOfBounds = 2
            BottomOutOfBounds = 3
            BlockCollision = 4

        # Wall kicks tried in order when rotating, in (rows, characters) , each one of them is tried in order until the result fits else rotation is cancelled.
        KICKS = ((0, 0), (0, 2), (0, -2), (0, 4), (0, -4), (-1, 0) ,(-2,0))

        def __init__(self, grid, color, blockType):
            self.__gameGrid = grid
            self.__blockType = blockType
            self.color = color                      
            self.__individualPositions = list(_SHAPES[blockType])
            self.__iState = 0  #The state of the I piece , either first orientation or second orientation.
            self.__position = (_GRID_POS[0] + _SPAWN_ROW, _GRID_POS[1] + _GRID_SIZE[0] // 2)
            self.__settled = False

            self.__individualSprites = []
            for _ in range(4):
                sprite = h.Sprite(texture="██", colorRegister={}, textureRectPosition=(1, 1), dimensions=(2, 1), zIndex=2)
                # left char bright, right char darker , a little polishing , as i cant put dark outlines to blocks due to terminal rendering.
                sprite.setColorRegister(colorRegister={(1, 1): shade(color, 1.0), (1, 2): shade(color, 0.7)})
                self.__individualSprites.append(sprite)

        #collision stuff
        def __globalPositions(self, position, offsets):
            return [(o[0] + position[0], o[1] + position[1]) for o in offsets]

        def getGlobalPositions(self):
            return self.__globalPositions(self.__position, self.__individualPositions)

        def __isValid(self, positions):
            cols, rows = _GRID_SIZE[0] // 2, _GRID_SIZE[1]
            for row, col in positions:
                r = row - _GRID_POS[0]
                c = (col - _GRID_POS[1]) // 2

                if c < 0:
                    return self.CollisionType.LeftOutOfBounds
                if c >= cols:
                    return self.CollisionType.RightOutOfBounds
                if r >= rows:
                    return self.CollisionType.BottomOutOfBounds
                if r >= 0 and self.__gameGrid[r][c] is not None:     # if r < 0 = above the board, so we dont care. Well we do care but it is done by isBlocked().
                    return self.CollisionType.BlockCollision

            return self.CollisionType.NoCollision

        def __fits(self, position, offsets):
            return self.__isValid(self.__globalPositions(position, offsets)) == self.CollisionType.NoCollision

        def isBlocked(self):
            """True if the piece overlaps something right now (used for game over on spawn)."""
            return not self.__fits(self.__position, self.__individualPositions)

        def __shift(self, dc):
            """try to shift the whole block horizontally , if the resulting block __fits , accept the shift else neglect the shift."""
            pos = (self.__position[0], self.__position[1] + dc)
            if self.__fits(pos, self.__individualPositions):
                self.__position = pos

        def __rotate(self):
            """rotate the block , if is out of bounds , try to every kick to push it into correct place , if kick did not work then ignore the rotation"""
            if self.__blockType == BlockType.O:
                return

            if self.__blockType == BlockType.I:
                newState = 1 - self.__iState
                rotated = list(_I_STATES[newState])
            else:
                newState = self.__iState
                rotated = [(-c // 2, r * 2) for r, c in self.__individualPositions]

            for dr, dc in self.KICKS:
                pos = (self.__position[0] + dr, self.__position[1] + dc)
                if self.__fits(pos, rotated):
                    self.__individualPositions = rotated
                    self.__position = pos
                    self.__iState = newState
                    return
            # no kick worked => rotation is simply cancelled

        def tryToMove(self, input):
            """moves the block using shift or rotate basing on the given input"""
            if input == b"d":
                self.__shift(2)
            elif input == b"a":
                self.__shift(-2)
            elif input == b"r":
                self.__rotate()

        def tryToMoveDown(self, settleOnFail=True):
            """Returns True if the piece moved. A failed move down is the ONLY thing that settles a piece."""
            pos = (self.__position[0] + 1, self.__position[1])
            if self.__fits(pos, self.__individualPositions):
                self.__position = pos
                return True
            if settleOnFail:
                self.__settled = True
            return False

        # The ghost peice and hard drop stuff
        def __dropPosition(self):
            pos = self.__position
            while self.__fits((pos[0] + 1, pos[1]), self.__individualPositions):
                pos = (pos[0] + 1, pos[1])
            return pos

        def hardDrop(self):
            """Teleports to the landing spot and settles. Returns how many rows it fell."""
            pos = self.__dropPosition()
            dropped = pos[0] - self.__position[0]
            self.__position = pos
            self.__settled = True
            return dropped

        def getGhostCoords(self):
            coords = {}
            for row, col in self.__globalPositions(self.__dropPosition(), self.__individualPositions):
                if row >= _GRID_POS[0]:
                    coords[(row, col)] = ("░", _GHOST_COLOR, 0)        # z=0: the real piece wins overlaps , not really , any z works because there is no collision between ghost piece and real piece , thats the whole point.
                    coords[(row, col + 1)] = ("░", _GHOST_COLOR, 0)
            return coords

        def update(self):
            pos = self.getGlobalPositions()
            for sprite, p in zip(self.__individualSprites, pos):
                sprite.setPosition(p)
                sprite.setVisibility(p[0] >= _GRID_POS[0])             # hide cells above the border
            return self.__settled

        def getOccupiedCoords(self):
            return [sprite.getOccupiedCoords() for sprite in self.__individualSprites]

    def renderBelow(self):
        return self.__renderBelow

    def updateBelow(self):
        return self.__updateBelow

    def __init__(self, *, windowHandler, assetManager, animationRegistry):
        self.__windowHandler = windowHandler
        self.__assetManager = assetManager
        self.__animationRegistry = animationRegistry

        self.__reqs = []
        self.__renderBelow = False
        self.__updateBelow = False

        self.__previousTime = 0

        global _GRID_POS
        _GRID_POS = (
            (self.__windowHandler.getWindowSize()[1] // 2) - (_GRID_SIZE[1] // 2),
            (self.__windowHandler.getWindowSize()[0] // 2) - (_GRID_SIZE[0] // 2)
        )

        self.__score = 0
        self.__lines = 0
        self.__over = False
        self.__clearing = None          # tuple of => (rows being cleared, time the flash ends) or None
        self.__activeBlock = None
        self.__bag = []

        # grid[row][col] -> None (empty) or an rgb tuple (locked cell)
        self.__grid = [[None] * (_GRID_SIZE[0] // 2) for _ in range(_GRID_SIZE[1])]

        self.__setupExtras()

        self.__nextType = self.__drawFromBag()
        self.__spawn(0)

    def __setupExtras(self):
        cols = _GRID_SIZE[0] // 2

        # border => the rectangle boundary.
        border = h.Sprite(h.rectangle(dimensions=(_GRID_SIZE[0] + 2, _GRID_SIZE[1] + 2)), colorRegister={}, textureRectPosition=(1, 1),
                          dimensions=(_GRID_SIZE[0] + 2, _GRID_SIZE[1] + 2), zIndex=1)
        border.setTransparency(True)
        border.setPosition((_GRID_POS[0] - 1, _GRID_POS[1] - 1))
        self.__borderCoords = border.getOccupiedCoords()

        # dotted background => looks cool , cheap replacement of grid => jugaad.
        dots = ("· " * cols + "\n") * _GRID_SIZE[1]
        background = h.Sprite(texture=dots, colorRegister={}, textureRectPosition=(1, 1), dimensions=_GRID_SIZE, zIndex=-1)
        background.setColorRegister(colorRegister={}, defaultColor=_DOT_COLOR)
        background.setTransparency(True)
        background.setPosition(_GRID_POS)
        self.__backgroundCoords = background.getOccupiedCoords()

        # locked cells: ONE sprite, rebuilt only when the grid changes
        blank = ("  " * cols + "\n") * _GRID_SIZE[1]
        self.__renderSprite = h.Sprite(texture=blank, colorRegister={}, textureRectPosition=(1, 1), dimensions=_GRID_SIZE, zIndex=1)
        self.__renderSprite.setTransparency(True)
        self.__renderSprite.setPosition(_GRID_POS)
        self.updateGrid()

        nextRect = h.Sprite(texture=h.rectangle(dimensions=(12,6)) , colorRegister={} , textureRectPosition=(1,1) , dimensions=(12,6) , zIndex=1)
        nextRect.setPosition((_GRID_POS[0]+6 ,  _GRID_POS[1] + _GRID_SIZE[0] + 3))
        nextRect.setTransparency(True)
        self.__nextRectCoords = nextRect.getOccupiedCoords()

    def updateGrid(self, flashRows=()):
        lines = []
        colors = {}
        for i, row in enumerate(self.__grid):
            text = ""
            for j, cell in enumerate(row):
                if cell is None:
                    text += "  "
                    continue
                text += "██"
                if i in flashRows:
                    colors[(i + 1, 2 * j + 1)] = _WHITE
                    colors[(i + 1, 2 * j + 2)] = _WHITE
                else:
                    colors[(i + 1, 2 * j + 1)] = shade(cell, 1.0)
                    colors[(i + 1, 2 * j + 2)] = shade(cell, 0.7)
            lines.append(text + "\n")

        self.__renderSprite.setTexture("".join(lines))
        self.__renderSprite.setColorRegister(colorRegister=colors)
        self.__boardCoords = self.__renderSprite.getOccupiedCoords()

    #some game logic related stuff
    def __drawFromBag(self):
        """7-bag: every piece type appears once per 7 pieces."""
        if not self.__bag:
            self.__bag = list(BlockType)
            rnd.shuffle(self.__bag)
        return self.__bag.pop()

    def __level(self):
        return self.__lines // 10 + 1

    def __gravityInterval(self):
        return max(_GRAVITY_MIN, _GRAVITY_BASE * (0.85 ** (self.__level() - 1)))

    def __spawn(self, time):
        blockType = self.__nextType
        self.__nextType = self.__drawFromBag()
        block = Tetris.Block(self.__grid, _COLORS[blockType], blockType)
        self.__previousTime = time
        if block.isBlocked():                 # no room for the new piece as soon as it is spawned => game over
            self.__activeBlock = None
            self.__over = True
            return
        block.update()                        # place its sprites before the first render i.e sets position for each individual block.
        self.__activeBlock = block

    def __lock(self, time):
        block = self.__activeBlock
        self.__activeBlock = None

        lockedAboveBoard = False
        for row, col in block.getGlobalPositions():
            r = row - _GRID_POS[0]
            if r < 0:
                lockedAboveBoard = True       # above the grid => dont belong to the grid => we ignore.
                continue
            self.__grid[r][(col - _GRID_POS[1]) // 2] = block.color

        if lockedAboveBoard:
            self.__over = True
            return

        full = [i for i, row in enumerate(self.__grid) if None not in row]
        if full:
            self.__clearing = (full, time + _CLEAR_FLASH_TIME)
            self.updateGrid(flashRows=full)   # rows flash white until the timer ends
        else:
            self.updateGrid()
            self.__spawn(time)

    def __removeRows(self, rows):
        remaining = [row for i, row in enumerate(self.__grid) if i not in rows]
        cols = _GRID_SIZE[0] // 2
        # slice-assign so every reference to this list (the activeBlock holds one) stays valid . smiple do a shallow reset.
        self.__grid[:] = [[None] * cols for _ in rows] + remaining
        self.__score += _LINE_SCORES.get(len(rows), 800) * self.__level()
        self.__lines += len(rows)

    def __restart(self, time):
        for row in self.__grid:
            row[:] = [None] * len(row)
        self.__score = 0
        self.__lines = 0
        self.__over = False
        self.__clearing = None
        self.__bag = []
        self.__nextType = self.__drawFromBag()
        self.updateGrid()
        self.__spawn(time)

    def handleInput(self, *, input, time):
        if input == b"p":
            self.__reqs.append((h.Request.popAndSave, None))
            self.__reqs.append((h.Request.push, "TikTakToe"))
            return

        if input == b"\x1b":
            self.__reqs.append((h.Request.pop, None))
            return

        if self.__over:
            if input == b"\r":
                self.__restart(time)
            return

        if self.__activeBlock is None:        # rows are flashing, ignore gameplay input. activeBlock is only set to None and no newBlock is spawned only when flashing and row clearing is happening.
            return

        if input == b" ":
            self.__score += 2 * self.__activeBlock.hardDrop()
        elif input == b"s":
            if self.__activeBlock.tryToMoveDown(settleOnFail=False):
                self.__score += 1
        else:
            self.__activeBlock.tryToMove(input)

    def update(self, *, time):
        if self.__over:
            pass

        elif self.__clearing is not None:
            rows, until = self.__clearing
            if time >= until:
                self.__clearing = None
                self.__removeRows(rows)
                self.updateGrid()
                self.__spawn(time)

        else:
            if time - self.__previousTime >= self.__gravityInterval():
                self.__activeBlock.tryToMoveDown()
                self.__previousTime = time

            if self.__activeBlock.update():   # True once the piece has settled
                self.__lock(time)

        copy = self.__reqs[:]
        self.__reqs.clear()
        return copy

    def __hudCoords(self):
        top = _GRID_POS[0]
        left = _GRID_POS[1] + _GRID_SIZE[0] + 4
        coords = {}
        coords.update(_text(top, left, f"SCORE  {self.__score}", _HUD_COLOR))
        coords.update(_text(top + 1, left, f"LINES  {self.__lines}", _HUD_COLOR))
        coords.update(_text(top + 2, left, f"LEVEL  {self.__level()}", _HUD_COLOR))
        coords.update(_text(top + 4, left, "NEXT", _HUD_COLOR))

        rgb = _COLORS[self.__nextType]
        for dr, dc in _SHAPES[self.__nextType]:
            r, c = top + 8 + dr, left + 4 + dc
            if(self.__nextType == BlockType.O):
                c+=1
            coords[(r, c)] = ("█", shade(rgb, 1.0), 1)
            coords[(r, c + 1)] = ("█", shade(rgb, 0.7), 1)

        hints = ["A / D    move", "R        rotate", "S        soft drop", "SPACE    hard drop", "P        pause", "ESC      quit"]
        for i, hint in enumerate(hints):
            coords.update(_text(top + 14 + i, left, hint, _HINT_COLOR))

        if self.__over:
            midRow = top + _GRID_SIZE[1] // 2
            for dr, msg in enumerate(["             ", "  GAME OVER  ", " ENTER: retry", "             "]):
                col = _GRID_POS[1] + (_GRID_SIZE[0] - len(msg)) // 2
                coords.update(_text(midRow - 1 + dr, col, msg, _OVER_COLOR, z=3, solid=True))
        return coords

    def render(self):
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__backgroundCoords)
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__borderCoords)
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__boardCoords)

        if self.__activeBlock is not None:
            self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__activeBlock.getGhostCoords())
            for coord in self.__activeBlock.getOccupiedCoords():
                self.__windowHandler.handleOccupiedCoords(occupiedCoords=coord)

        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__hudCoords())
        self.__windowHandler.handleOccupiedCoords(occupiedCoords=self.__nextRectCoords)
        self.__windowHandler.render()