from enum import Enum  # Importa la clase Enum del módulo enum para crear enumeraciones

class TokenType(Enum):  # Define una enumeración para representar los distintos tipos de tokens
    LETTER = 0  # Token para letras y dígitos
    APPEND = 1  # Token para el operador de concatenación
    OR = 2  # Token para el operador OR
    KLEENE = 3  # Token para el operador Kleene star (*)
    LPAR = 4  # Token para el paréntesis de apertura
    RPAR = 5  # Token para el paréntesis de cierre

class Token:
    def __init__(self, type: TokenType, value=None):  # Constructor que inicializa un token con un tipo y un valor opcional
        self.type = type  # Tipo de token basado en la enumeración TokenType
        self.value = value  # Valor del token, por defecto None
        self.precedence = type.value  # Precedencia del token, usando el valor del tipo de token

    def __repr__(self):  # Método especial para representar el token como una cadena
        return f'{self.type.name}: {self.value}'  # Devuelve una cadena que muestra el tipo y el valor del token