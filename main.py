from functions.parsing import Parser
from functions.nfa import NFA

program_title = '''
#        AUTOMATAS FINITOS        #

Genera AFNs basados en una expresión regular. NOTA: para epsilon usar la letra 'e'
'''

main_menu = '''
Seleccione una opción:
1. Definir una expresión regular
0. Salir
'''

thompson_msg = '''
    # AFN CREADO #
'''

type_regex_msg = '''
Ingrese la expresión regular:
'''

if __name__ == "__main__":
    print(program_title)
    opt = None
    regex = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            print(type_regex_msg)
            regex = input('> ')

            try:
                parser = Parser(regex)
                tree = parser.Parse()
                print(thompson_msg)

                nfa = NFA(tree, regex, regex)
                nfa_regex = nfa.EvalRegex()

                nfa.WriteNFADiagram()

            except AttributeError as e:
                print(f'\n\tERR: Expresión no válida (faltan paréntesis)')
            except Exception as e:
                print(f'\n\tERR: {e}')

        elif opt == '0':
            print('Chau!')
            exit(1)
