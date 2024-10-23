import CCOMPILER
from lexical_analyzer import LexicalAnalyzer, Lexema, GrammarSymbol
from output import generate_lalr_table, display_parse_table  # Asegúrate de que esté en el archivo correcto
from map import asign, simplify_grammar

direccion = r"C:\compil.txt"

# Cargar el compilador
compilador = CCOMPILER.ccompiler(direccion)
compilador.loadCompiler()
compilador.checkCompiler()

# Inicializar el analizador léxico
lexer = LexicalAnalyzer(compilador)
tokens = lexer.get_lexical_tokens("PROGRAM prueba ; VAR variable1 : INTEGER ; VAR variable2 : INTEGER ; BEGIN variable1 := 5 * 4 + 3 * 5 ; READLN ( variable1 ) ; READLN ( variable2 ) IF TRUE AND FALSE OR TRUE AND TRUE THEN READLN ( variable1 ) ELSE READLN ( variable2 ) END .")
for token in tokens:
    print(token.get_symbol(), token.get_value())

#Cargar la tabla lalr (la gramatica está en el objeto compiler)
#grammar = compilador.getProductionsString()

#creamos el diccionario
diccionario = asign(grammar)

#simplificamos la gramatica
simpGrammar = simplify_grammar(grammar, diccionario)
print(grammar)

# Procesar las producciones del compilador
#grammar, terminals = process_productions(compilador.productions)

# Generar la tabla LALR usando la gramática procesada
#parse_table, term, non_term = generate_lalr_table(grammar)

# Reemplazar la lista term por los terminales identificados
#term = list(terminals)

# Mostrar la tabla LALR en la consola
#display_parse_table(parse_table, term, non_term)
