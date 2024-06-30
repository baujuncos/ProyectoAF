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
        #self.trans_func = self.GenerateTransitionTable()
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
