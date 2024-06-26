from enum import Enum


class TokenType(Enum):   #numeracion para ayudarnos a representar cada tipo distinto de
    LETTER = 0
    APPEND = 1
    OR = 2
    KLEENE = 3
    LPAR = 4
    RPAR = 5


class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type   #tipo de token
        self.value = value  #valor
        self.precedence = type.value    #precedencia

    def __repr__(self):
        return f'{self.type.name}: {self.value}'
