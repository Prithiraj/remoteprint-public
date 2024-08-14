from pyparsing import Enum


from enum import Enum

class ItemType(Enum):
    COLUMNS = 1
    IMAGE = 2
    BARCODE = 3
    CONTENT = 4
    LINE = 5
    
class AlignType(Enum):
    left = 1
    right = 2
    centre = 3
    
class MarkupTags(Enum):
    w1h1 = 1
    w1h2 = 2
    w2h1 = 3

class LineModes(Enum):
    UP = 1
    DOWN = 2
    DASHED = 3
    

class DrawerOpenModes(Enum):
    START = 1
    END = 2
    NONE = 3
    