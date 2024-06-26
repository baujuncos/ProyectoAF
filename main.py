from functions.reader import Reader  # Importa la clase Reader del módulo functions.reader
from functions.parsing import Parser  # Importa la clase Parser del módulo functions.parsing
from functions.nfa import NFA  # Importa la clase NFA del módulo functions.nfa

# Mensajes que se mostrarán al usuario
program_title = '''
#        AUTOMATAS FINITOS        #

Genera AFNs basados en una expresión regular. NOTA: para epsilon usar la letra 'e'
'''  # Título del programa y una nota sobre cómo representar epsilon

main_menu = '''
Seleccione una opción:
1. Definir una expresión regular
0. Salir
'''  # Menú principal para que el usuario seleccione una opción

thompson_msg = '''
    # AFN CREADO # '''  # Mensaje que se mostrará cuando se cree un AFN

type_regex_msg = '''
Ingrese la expresión regular: '''  # Mensaje para pedir al usuario que ingrese una expresión regular

if __name__ == "__main__":  # Asegura que este script solo se ejecute si no se ha importado desde otro módulo.
    print(program_title)  # Muestra el título del programa
    opt = None  # Inicializa la variable opt
    regex = None  # Inicializa la variable regex
    method = None  # Inicializa la variable method (no se utiliza en este código)

    while opt != 0:  # Bucle que continúa hasta que el usuario elija salir (opt == 0)
        print(main_menu)  # Muestra el menú principal
        opt = input('> ')  # Lee la opción seleccionada por el usuario

        if opt == '1':  # Si el usuario elige definir una expresión regular
            print(type_regex_msg)  # Muestra el mensaje para ingresar la expresión regular
            regex = input('> ')  # Lee la expresión regular ingresada por el usuario

            try:
                reader = Reader(regex)  # Crea un objeto Reader para tokenizar la expresión
                tokens = reader.CreateTokens()  # Crea los tokens a partir de la expresión regular
                parser = Parser(tokens)  # Crea un objeto Parser para analizar los tokens
                tree = parser.Parse()  # Genera el árbol de análisis sintáctico a partir de los tokens
                print(thompson_msg)  # Muestra el mensaje indicando que el AFN fue creado

                nfa = NFA(tree, reader.GetSymbols(), regex)  # Crea un objeto NFA con el árbol, los símbolos y la expresión regular
                nfa_regex = nfa.EvalRegex()  # Evalúa si la expresión regular es aceptada por el NFA

                nfa.WriteNFADiagram()  # Escribe y renderiza el diagrama del NFA

            except AttributeError as e:  # Maneja el error de atributo (por ejemplo, si faltan paréntesis)
                print(f'\n\tERR: Expresión no válida (faltan paréntesis)')

            except Exception as e:  # Maneja cualquier otro tipo de excepción
                print(f'\n\tERR: {e}')

        elif opt == '0':  # Si el usuario elige salir
            print('Chau!')  # Muestra un mensaje de despedida
            exit(1)  # Sale del programa
