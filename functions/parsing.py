from functions.tokens import TokenType # enumera los tipos de tokens posibles
from functions.nodes import * # importa todas las clases de nodos

class Parser: # convierte una secuencia de tokens (representación de una expresión regular) en un árbol sintáctico abstracto
    def __init__(self, tokens): #constructor; inicializa el parser con una lista de tokens y llama al método Next para obtener el primer token
        self.tokens = iter(tokens)
        self.Next()

    def Next(self): # avanza al siguiente token en la secuencia. Si no hay más tokens, establece self.curr_token a None
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def NewSymbol(self): # se encarga de analizar y construir los nodos para los símbolos básicos en la expresión regular
        token = self.curr_token

        if token.type == TokenType.LPAR: # si el token actual es un paréntesis izquierdo (, avanza al siguiente token y llama a Expression para evaluar la subexpresión dentro de los paréntesis.
            self.Next()
            res = self.Expression()

            if self.curr_token.type != TokenType.RPAR:
                raise Exception('No hay parentesis derecho para la expresion') # verifica que haya un paréntesis derecho ) y avanza al siguiente token

            self.Next()
            return res

        elif token.type == TokenType.LETTER: # si el token actual es una letra, crea un nodo Letter con el valor del token y avanza al siguiente token
            self.Next()
            return Letter(token.value)

    def NewOperator(self): # maneja operadores unarios
        res = self.NewSymbol() # llama a new symbol para obtener un simbolo

        while self.curr_token != None and \
                (
                    self.curr_token.type == TokenType.KLEENE # mientras el token actual sea un operador de Kleene (*), crea un nodo Kleene
                ):
            if self.curr_token.type == TokenType.KLEENE:
                self.Next() # avanza al siguiente token
                res = Kleene(res)

        return res

    def Expression(self): # construye el árbol sintactico que representa la ER completa, manejando todos los operadores
        res = self.NewOperator() # llama a NewOperator para obtener una expresion inicial

        while self.curr_token != None and \
                (
                    self.curr_token.type == TokenType.APPEND or 
                    self.curr_token.type == TokenType.OR 
                ):
            if self.curr_token.type == TokenType.OR: # si el token actual es de union, crea el nodo Or
                self.Next() # se avanza al siguiente
                res = Or(res, self.NewOperator()) # se crea la union entre el actual y el siguiente

            elif self.curr_token.type == TokenType.APPEND: # si el token actual es de concatenacion, crea el nodo Append
                self.Next()
                res = Append(res, self.NewOperator()) # se crea la concatenacion entre el actual y el siguiente

        return res

    def Parse(self): # verifica si sigue habiendo tokens que procesar
        if self.curr_token == None: 
            return None

        res = self.Expression() # si hay, llama a expression 

        return res
