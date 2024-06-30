from graphviz import Digraph
from functions.nodes import Or, Letter, Append, Kleene

class NFA:
    def __init__(self, tree, regex):
        # Propiedades del autómata finito no determinista (NFA)
        self.accepting_states = []
        self.trans_func = None
        self.curr_state = 1

        # Árbol de nodos y expresión regular
        self.regex = regex
        self.tree = tree
        self.regexAccepted = None

        # Propiedades para crear el diagrama con Graphviz
        self.dot = Digraph(comment='Diagrama AFN', strict=True)
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')

        # Ejecuta el algoritmo de construcción del NFA
        self.Render(tree)
        self.trans_func = self.GenerateTransitionTable()
        self.accepting_states = self.GetAcceptingState()

    def Render(self, node):
        # Renderiza el nodo actual llamando al método correspondiente
        self.prev_state = self.curr_state
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        # Renderiza un nodo de letra
        return node.value

    def AppendNode(self, node):
        # Renderiza un nodo de concatenación (.)
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )
        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.b)
        )

    def OrNode(self, node):
        # Renderiza un nodo OR (+)
        initial_node = self.curr_state - 1
        mid_node = None

        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'ε'
        )
        self.curr_state += 1

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        mid_node = self.curr_state
        self.curr_state += 1

        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'ε'
        )

        self.curr_state += 1

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.b)
        )

        self.curr_state += 1

        self.dot.edge(
            str(mid_node),
            str(self.curr_state),
            'ε'
        )

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'ε'
        )

    def KleeneNode(self, node):
        # Renderiza un nodo de estrella de Kleene (*)
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'ε'
        )

        first_node = self.curr_state - 1
        self.curr_state += 1

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        self.dot.edge(
            str(self.curr_state),
            str(first_node + 1),
            'ε'
        )

        self.curr_state += 1

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'ε'
        )

        self.dot.edge(
            str(first_node),
            str(self.curr_state),
            'ε'
        )

    def GenerateTransitionTable(self):
        # Genera la tabla de transiciones
        states = [i.replace('\t', '') for i in self.dot.source.split('\n') if '->' in i and '=' in i]  # obtiene las transiciones del diagrama
        self.trans_func = dict.fromkeys([str(s) for s in range(self.curr_state + 1)])  # crea un diccionario con los números de los estados
        self.trans_func[str(self.curr_state)] = dict()  # inicia la tabla de transiciones para un estado actual

        for state in states:  # procesa todas las transiciones y actualiza la tabla
            splitted = state.split(' ')
            init = splitted[0]
            final = splitted[2]

            symbol_index = splitted[3].index('=')
            symbol = splitted[3][symbol_index + 1]

            try:
                self.trans_func[init][symbol].append(final)
            except:
                self.trans_func[init] = {symbol: [final]}

        return self.trans_func

    def EvalRegex(self):
        # Evalúa si la expresión regular es aceptada por el NFA
        try:
            self.EvalNext(self.regex[0], '0', self.regex)
            return 'Yes' if self.regexAccepted else 'No'
        except RecursionError:
            if self.regex[0] in self.symbols and self.regex[0] != 'ε':
                return 'Yes'
            else:
                return 'No'

    def EvalNext(self, eval_symbol, curr_state, eval_regex):
        # Evalúa el siguiente símbolo de la expresión regular
        if self.regexAccepted is not None:
            return

        transitions = self.trans_func[curr_state]
        for trans_symbol in transitions:
            if trans_symbol == 'ε':
                if not eval_regex and str(self.accepting_states) in transitions['ε']:
                    self.regexAccepted = True
                    return

                for state in transitions['ε']:
                    if self.regexAccepted is not None:
                        break
                    self.EvalNext(eval_symbol, state, eval_regex)

            elif trans_symbol == eval_symbol:
                next_regex = eval_regex[1:]
                try:
                    next_symbol = next_regex[0]
                except:
                    next_symbol = None

                if not next_symbol:
                    if str(self.accepting_states) in transitions[trans_symbol]:
                        self.regexAccepted = True
                        return

                    elif str(self.accepting_states) != curr_state:
                        for state in transitions[trans_symbol]:
                            self.EvalNext('ε', state, None)
                        if self.regexAccepted is not None:
                            return

                if self.regexAccepted is not None:
                    return

                for state in transitions[trans_symbol]:
                    if not next_symbol and str(state) == self.accepting_states:
                        self.regexAccepted = True
                        return

                    self.EvalNext(next_symbol, state, next_regex)

    def GetAcceptingState(self):
        # Obtiene el estado de aceptación
        self.dot.node(str(self.curr_state), shape='doublecircle')
        self.accepting_states.append(self.curr_state)
        return self.curr_state

    def WriteNFADiagram(self):
        # Escribe el diagrama del NFA en un archivo y lo renderiza
        source = self.dot.source  # obtiene la fuente del diagrama
        # escribe en el archivo
        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)


# Función que escribe contenido en un archivo.
def WriteToFile(filename: str, content: str):
    with open(filename, 'w', encoding='utf-8') as _file:
        _file.write(content)
    return f'Archivo "{filename}" creado'
