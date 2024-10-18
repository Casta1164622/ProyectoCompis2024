import CCOMPILER
from lexical_analyzer import LexicalAnalyzer, Lexema, GrammarSymbol

direccion = r"C:\compil.txt"

compilador = CCOMPILER.ccompiler(direccion)

compilador.loadCompiler()
compilador.checkCompiler()

lexer = LexicalAnalyzer(compilador)
tokens = lexer.get_lexical_tokens("") #aquí hagan sus pruebas
for token in tokens:
    print(token.get_symbol(), token.get_value())
