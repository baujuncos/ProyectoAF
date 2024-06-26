from functions.reader import Reader
from functions.parsing import Parser
from functions.nfa import NFA


#Mensajes que se mostraran al usuario
program_title = '''   

#        AUTOMATAS FINITOS        #

Genera AFNs basados en un expresion regular. NOTA: para epsilon usar la letra 'e'
'''
main_menu = '''
Seleccione una opcion:
1. Definir una expresion regular
0. Salir
'''
thompson_msg = '''
    # AFN CREADO # '''

type_regex_msg = '''
Ingrese la expresion regular: '''

if __name__ == "__main__":  # asegurarse de que este script solo se ejecute si no se ha importado desde otro módulo.
    print(program_title)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            print(type_regex_msg)
            regex = input('> ')

            try:
                reader = Reader(regex)   #Se crea un objeto Reader para tokenizar la expresión
                tokens = reader.CreateTokens()
                parser = Parser(tokens)
                tree = parser.Parse()
                print(thompson_msg)

                nfa = NFA(tree, reader.GetSymbols(), regex)
                nfa_regex = nfa.EvalRegex()


                nfa.WriteNFADiagram()

            except AttributeError as e:
                print(f'\n\tERR: Expresion no valida (faltan parentesis)')

            except Exception as e:
                print(f'\n\tERR: {e}')

        elif opt == '0':
            print('Chau!')
            exit(1)
