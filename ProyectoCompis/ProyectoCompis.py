import CCOMPILER
from lexical_analyzer import LexicalAnalyzer
from output import generate_lalr_table, display_parse_table
from map import asign, simplify_grammar
from output import read_grammar_from_string, leer_input_txt_como_string

direccion = r"C:\compil.txt"

# Cargar el compilador
compilador = CCOMPILER.ccompiler(direccion)
compilador.loadCompiler()
compilador.checkCompiler()

# Inicializar el analizador léxico
lexer = LexicalAnalyzer(compilador)
tokens = lexer.get_lexical_tokens(leer_input_txt_como_string())

#Cargar la tabla lalr (la gramatica está en el objeto compiler)
grammarString = compilador.generarProduccionesString()

#creamos el diccionario
diccionario = asign(grammarString)

#simplificamos la gramatica
simpGrammar = simplify_grammar(grammarString, diccionario)

grammar = read_grammar_from_string(simpGrammar)

if grammar:
    # Generar la tabla LALR
    parse_table, term, non_term = generate_lalr_table(grammar)
    # Mostrar la tabla LALR en la consola
    display_parse_table(parse_table, term, non_term)
else:
    print("Gramática inválida o archivo vacío.")
