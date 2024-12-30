from enum import Enum

class CommandType(Enum):
    C_ARITHMETIC = "arithmetic"
    C_PUSH = "push"
    C_POP = "pop"
    C_LABEL = "label"
    C_GOTO = "goto"
    C_IF = "if-goto"
    C_FUNCTION = "function"
    C_CALL = "call"
    C_RETURN = "return"