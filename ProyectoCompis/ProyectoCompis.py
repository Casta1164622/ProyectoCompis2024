import CCOMPILER
from lexical_analyzer import LexicalAnalyzer
from output import generate_lalr_table, display_parse_table
from map import asign, simplify_grammar, reverse_simplify_grammar_list
from output import read_grammar_from_string, leer_input_txt_como_string, generate_lalr_list
from Syntax_analyzer import SyntaxAnalyzer

#Se solicita la ruta donde esté el txt con la información de la gramatica, los tokens, etc.
direccion = input("Ingrese ruta del archivo:\n") # En mi caso la ruta de mi txt es: C:\compil.txt
#Se crea la instancia del objeto compilador (Fase 1)
compilador = CCOMPILER.ccompiler(direccion)
# Cargar el compilador
compilador.loadCompiler()

if compilador.checkCompiler():
    # Inicializar el analizador léxico
    lexer = LexicalAnalyzer(compilador)
    tokens = lexer.get_lexical_tokens(leer_input_txt_como_string())

    #Cargar la tabla lalr (la gramatica está en el objeto compiler)
    grammarString = compilador.productionsTostring()

    #creamos el diccionario
    diccionario = asign(grammarString)

    #simplificamos la gramatica
    simpGrammar = simplify_grammar(grammarString, diccionario)

    grammar = read_grammar_from_string(simpGrammar)

    if grammar:
        # Generar la tabla LALR
        parse_table, term, non_term = generate_lalr_table(grammar)
        # Mostrar la tabla LALR en el txt
        display_parse_table(parse_table, term, non_term, diccionario)
        #Generar las producciones para que sean cargadas en la tabla del analizador sintáctico
        productions = compilador.Production_list()
        #Se generan los estados de la lalr (la que está en el txt) para que sean cargados por el analizador sintáctico
        lalr = generate_lalr_list(parse_table, term, non_term)
        #Se "desimplifica" la gramatica, ya que eso se usó nada mas para crear los estados y la lalr por lo que para que pueda ser cargado por el analizador sintáctico se le mandan como son o sea sin simplificar
        lalr = reverse_simplify_grammar_list(lalr, diccionario)
        #Se crea la instancia del analizador sintactico, mandandole las producciones y los estados de la lalr
        syntaxAn = SyntaxAnalyzer(productions, lalr)
        #Se parsea el input (el método de parsing imprime si se acepta o si no)
        syntaxAn.parsing(tokens)
    else:
        #Si algo sale mal con la gramatica se imprime que hubo un error en la gramatica
        print("Gramática inválida o sin producciones")
