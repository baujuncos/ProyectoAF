# clases que representan los nodos en el arbol sintactico para la ER


class Letter: # representa una letra individual en la expresion regular
    def __init__(self, value): # inicializa una instancia de letter con un valor específico
        self.value = value

    def __repr__(self): # devuelve una representacion en cadena de la letra (el valor)
        return f'{self.value}'


class Append(): # representa la concatenacion de dos subexpresiones
    def __init__(self, a, b): # inicializa una instancia de Append con dos subexpresiones, 'a' y 'b'.
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}.{self.b})' # devuelve una representación en cadena de la concatenación de las dos subexpresiones con un punto (.) como separador


class Or(): # representa la union/operacion OR de dos subexpresiones
    def __init__(self, a, b): # inicializa una instancia de OR con dos subexpresiones, 'a' y 'b'.
        self.a = a
        self.b = b

    def __repr__(self): # devuelve una representación en cadena de la operación OR entre las dos subexpresiones con una barra (|) como separador
        return f'({self.a}|{self.b})'


class Kleene(): # representa la operación de clausura de Kleene de una subexpresión
    def __init__(self, a): # inicializa una instancia de Kleene con una subexpresión 'a'.
        self.a = a

    def __repr__(self): # devuelve una representación en cadena de la subexpresión seguida de un asterisco (*)
        return f'{self.a}*'


class Expression(): # representa una expresión regular genérica que puede consistir en una o dos subexpresiones; permite tratar todas las expresiones regulares de manera uniforme sin preocuparse por su tipo específico
    def __init__(self, a, b=None): # inicializa una instancia de Expression con una subexpresión 'a' y, opcionalmente, una segunda subexpresión 'b'
        self.a = a
        self.b = b

    def __repr__(self): # devuelve una representación en cadena de las subexpresiones concatenadas si 'b' no es None, de lo contrario solo devuelve 'a'.
        if self.b != None:
            return f'{self.a}{self.b}'
        return f'{self.a}'
