from enum import IntEnum


class Priority(IntEnum):
    STATEMENT = 0
    UNARY = 1
    BINARY = 2
    KEYWORD = 3
