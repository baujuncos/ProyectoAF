from functions.nodes import *

class Reader:# crea un árbol síntactico de forma PREFIJA
    def __init__(self, regex): #Inicializa el analizador con la expresión regular que se va a procesar.
        self.regex = regex
        self.curr_index = 0

    def Next(self): #siguiente caracter de la er
        if self.curr_index < len(self.regex):
            self.curr_index += 1
        return self.regex[self.curr_index - 1] if self.curr_index > 0 else None

    def CurrentChar(self): #devuelve el actual caracter de la er
        return self.regex[self.curr_index] if self.curr_index < len(self.regex) else None

    def NewSymbol(self):  #Analiza y construye un nodo para "cada" símbolo en la expresión regular.
        char = self.CurrentChar()
        
        if char == '(':
            self.Next()
            res = self.Expression()
            if self.CurrentChar() != ')':
                raise Exception('No hay paréntesis derecho para la expresión')
            self.Next()
            return res
        elif char.isalnum() or char == '.':
            self.Next()
            return Letter(char)

    def NewOperator(self): #Maneja los operadores en la expresión regular 
        res = self.NewSymbol()
        while self.CurrentChar() == '*':
            self.Next()
            res = Kleene(res)
        return res

    def Expression(self): #Construye el árbol sintáctico que representa la expresión regular completa, ordena de forma PREFIJA
        res = self.NewOperator()
        while self.CurrentChar() in ('+', '.'):
            if self.CurrentChar() == '+':
                self.Next()
                res = Or(res, self.NewOperator())
            elif self.CurrentChar() == '.':
                self.Next()
                res = Append(res, self.NewOperator())
        return res

    def Reader(self): #Inicia el análisis de la expresión regular
        if not self.regex:
            return None
        return self.Expression()
