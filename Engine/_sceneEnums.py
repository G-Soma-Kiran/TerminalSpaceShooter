
from enum import Enum
class Request(Enum):
    push=1,
    pop=2,
    popAndSave = 3,
    replaceWith=4,
    switchTo=5,
