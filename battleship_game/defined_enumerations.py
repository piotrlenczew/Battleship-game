from enum import Enum


class Direction(Enum):
    """Define dircetions."""
    vertical = 0
    horizontal = 1


class Course(Enum):
    """Define courses."""
    north = 0
    west = 1
    south = 2
    east = 3


class Keys(Enum):
    """Define keys."""
    UP = 'KEY_UP'
    DOWN = 'KEY_DOWN'
    RIGHT = 'KEY_RIGHT'
    LEFT = 'KEY_LEFT'
    ROTATE = 'v'
    EXIT = 'x'
