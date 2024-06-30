from functions.nodes import *

class Parser:
    def __init__(self, regex):
        self.regex = regex
        self.curr_index = 0

    def Next(self):
        if self.curr_index < len(self.regex):
            self.curr_index += 1
        return self.regex[self.curr_index - 1] if self.curr_index > 0 else None

    def CurrentChar(self):
        return self.regex[self.curr_index] if self.curr_index < len(self.regex) else None

    def NewSymbol(self):
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

    def NewOperator(self):
        res = self.NewSymbol()
        while self.CurrentChar() == '*':
            self.Next()
            res = Kleene(res)
        return res

    def Expression(self):
        res = self.NewOperator()
        while self.CurrentChar() in ('+', '.'):
            if self.CurrentChar() == '+':
                self.Next()
                res = Or(res, self.NewOperator())
            elif self.CurrentChar() == '.':
                self.Next()
                res = Append(res, self.NewOperator())
        return res

    def Parse(self):
        if not self.regex:
            return None
        return self.Expression()
