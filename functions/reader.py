from functions.tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz01234567890.'  #cadena que contiene todos los caracteres válidos para las letras en las expresiones regulares, incluyendo letras minúsculas, dígitos y el punto


class Reader:    #objeto en el que se lee la cadena 
    def __init__(self, string: str):    #constructor de la clase Reader. Recibe un string y elimina los espacios
        self.string = iter(string.replace(' ', ''))  #crea un iterador sobre la cadena
        self.input = set()     #Inicializa un conjunto vacío para almacenar los símbolos de la expresión y llama al método Next
        self.Next()

    def Next(self):  
        try:
            self.curr_char = next(self.string)  # Intenta obtener el siguiente carácter del iterador
        except StopIteration:
            self.curr_char = None  #Si el iterador se agota, establece self.curr_char en None.

    def CreateTokens(self):      
        while self.curr_char != None:  #siempre que haya un caracter que recorrer voy creando tokens

            if self.curr_char in LETTERS:     #si el caracter es uno de LETTERS prosigo
                self.input.add(self.curr_char)
                yield Token(TokenType.LPAR, '(')  #creo token parentesis apertura
                yield Token(TokenType.LETTER, self.curr_char)

                self.Next()
                added_parenthesis = False

                while self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char in '*'):

                    if self.curr_char == '*':
                        yield Token(TokenType.KLEENE, '*')
                        yield Token(TokenType.RPAR, ')')
                        added_parenthesis = True

                    if self.curr_char in LETTERS:
                        self.input.add(self.curr_char)
                        yield Token(TokenType.APPEND)
                        yield Token(TokenType.LETTER, self.curr_char)

                    self.Next()

                    if self.curr_char != None and self.curr_char == '(' and added_parenthesis:
                        yield Token(TokenType.APPEND)

                if self.curr_char != None and self.curr_char == '(' and not added_parenthesis:
                    yield Token(TokenType.RPAR, ')')
                    yield Token(TokenType.APPEND)

                elif not added_parenthesis:
                    yield Token(TokenType.RPAR, ')')

            elif self.curr_char == '+':   #si encuentro un caracter de tipo OR genero el token de tipo OR
                self.Next()
                yield Token(TokenType.OR, '+')

            elif self.curr_char == '(':
                self.Next()
                yield Token(TokenType.LPAR)

            elif self.curr_char in (')*'):

                if self.curr_char == ')':
                    self.Next()
                    yield Token(TokenType.RPAR)

                elif self.curr_char == '*':
                    self.Next()
                    yield Token(TokenType.KLEENE)

                # finalmente, chequear si se necesita agregar un token de concatenacion cuando no hay nada entre letras
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            else:
                raise Exception(f'Entrada no valida: {self.curr_char}')

    def GetSymbols(self):
        return self.input
