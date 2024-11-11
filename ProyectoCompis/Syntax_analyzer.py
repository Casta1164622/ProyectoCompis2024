from lexical_analyzer import GrammarSymbol
from lexical_analyzer import Lexema

productionList = []
Lalr = []
ActionList = []
rutaOutput = ""
currentTemp = 0

class NonTerminalSymbol(GrammarSymbol):
    NONTERMINAL = 1

    def __init__(self, symbol, value=None):
        super().__init__(self.NONTERMINAL)
        self.set_symbol(symbol)
        self.value = value

    def set_symbol(self, symbol):
        self.symbol = symbol
    
    def get_value(self) -> str:
        return self.value

class Operation:
    SHIFT = 0
    REDUCE = 1
    GOTO = 2
    ACCEPT = 4
    ERROR = 5

    def __init__(self, type, state_or_production):
        self.set_type(type)
        if type == self.SHIFT or type == self.GOTO:
            self.set_state(state_or_production)
        else:
            self.set_production(state_or_production)

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def get_production(self):
        return self._production

    def set_production(self, production):
        self._production = production

class Production:
    def __init__(self, non_terminal_key, *symbols):
        self.set_non_terminal_key(non_terminal_key)
        self.set_symbols(symbols)
        self.actions = []

    def get_non_terminal_key(self):
        return self._non_terminal_key

    def set_non_terminal_key(self, non_terminal_key):
        self._non_terminal_key = non_terminal_key

    def get_symbols(self):
        return self._symbols

    def set_symbols(self, symbols):
        self._symbols = symbols

    def get_actions(self):
        return self.actions

    def set_actions(self, *actions):
        for action in actions:
            self.actions.append(action)

import os

class SemanticAnalyzer:
    def __init__(self):
        self.symbols_table = {}
        self.temps = []

    def execute_operation(self, operation, lexemas, symbol):
        if operation == "start_program":
            symbol.value = f'class {lexemas[3].get_value()} ' + "{" + f'{lexemas[1].get_value()}' + " }"
            print(f"program loaded with value: {symbol.value}")
            self.escribir_en_archivo(symbol.value)
        elif operation == "execute_block":
            if lexemas[1].get_value() is None:
                symbol.value = f'{lexemas[0].get_value()}'
            else:
                symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
            print(f"Block loaded with value: {symbol.value}")
        elif operation == "handle_declarations":
            if lexemas[0].get_value() is None:
                symbol.value = f'{lexemas[1].get_value()}'
            else:
                symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
            print(f"declarations loaded with value: {symbol.value}")
        elif operation == "declare_variable":
            if lexemas[0].get_value() is None:
                symbol.value = f'static {lexemas[2].get_value()} {lexemas[4].get_value()};'
            else:
                symbol.value = f'static {lexemas[2].get_value()} {lexemas[4].get_value()}; {lexemas[0].get_value()}'
            print(f"variable declaration loaded with value: {symbol.value}")
        elif operation == "set_type_int":
            symbol.value = "int"
            print("Tipo establecido a int")
        elif operation == "set_type_double":
            symbol.value = "double"
            print("Tipo establecido a double")
        elif operation == "set_type_bool":
            symbol.value = "bool"
            print("Tipo establecido a bool")
        elif operation == "set_type_string":
            symbol.value = "string"
            print("Tipo establecido a string")
        elif operation == "begin_compound_statement":
            symbol.value = 'static void Main(string[] args){ ' + f'{lexemas[1].get_value()}' + " }"
            print(f"Compound statement loaded with value: {symbol.value}")
        elif operation == "add_statement":
            symbol.value = lexemas[0].get_value()
            print(f"statement loaded with value: {symbol.value}")
        elif operation == "add_statements":
            if lexemas[0].get_value() is None:
                symbol.value = lexemas[1].get_value()
            else:
                symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
                print(f"statement loaded with value: {symbol.value}")
        elif operation == "add_statement_ext":
            if lexemas[0].get_value() is None:
                symbol.value = lexemas[1].get_value()
            else:
                symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
                print(f"statement loaded with value: {symbol.value}")
        elif operation == "handle_assignment":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"Statement loaded with value: {symbol.value}")
        elif operation == "handle_if_statement":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"Statement loaded with value: {symbol.value}")
        elif operation == "handle_while_statement":
            print("Acción: handle_while_statement")
        elif operation == "handle_procedure_call":
            print("Acción: handle_procedure_call")
        elif operation == "handle_io_statement":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"Statement loaded with value: {symbol.value}")
        elif operation == "assign_value":
            symbol.value = f'{lexemas[2].get_value()} = {lexemas[0].get_value()};'
            print(f"Assignment loaded with value: {symbol.value}")
        elif operation == "execute_if":
            if lexemas[0].get_value() is None:
                symbol.value = "if (" + f'{lexemas[3].get_value()}' + " ) {" + f'{lexemas[1].get_value()}' + " }"
            else:
                symbol.value = "if (" + f'{lexemas[3].get_value()}' + " ) {" + f'{lexemas[1].get_value()}' + "}" + f'{lexemas[0].get_value()}'
            print(f"else loaded with value: {symbol.value}")
        elif operation == "execute_else":
            symbol.value = "else { " + f'{lexemas[0].get_value()}' + " }"
            print(f"else loaded with value: {symbol.value}")
        elif operation == "execute_println":
            symbol.value = f'Console.WriteLine({lexemas[1].get_value()});'
            print(f"PRINTLN loaded with value: {symbol.value}")
        elif operation == "execute_readln":
            symbol.value = f'{lexemas[1].get_value()} = Console.ReadLine();'
            print(f"READLN loaded with value: {symbol.value}")
        elif operation == "evaluate_expression":
            if lexemas[0].get_value() is None:
                symbol.value = f'{lexemas[1].get_value()}'
                print(f"expression loaded with value: {symbol.value}")
            else:
                symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
                print(f"expression loaded with value: {symbol.value}")
        elif operation == "evaluate_relational_expression":
            symbol.value = f'{lexemas[1].get_value()} {lexemas[0].get_value()}'
            print(f"relational with value: {symbol.value}")
        elif operation == "evaluate_simple_expression":
            symbol.value = f'{lexemas[2].get_value()} {lexemas[1].get_value()} {lexemas[0].get_value()}'
            print(f"simple expression loaded with value: {symbol.value}")
        elif operation == "evaluate_agruped_expression":
            symbol.value = f'({lexemas[1].get_value()})'
            print(f"agruped expression loaded with value: {symbol.value}")
        elif operation == "evaluate_term":
            symbol.value = f'{lexemas[2].get_value()} {lexemas[1].get_value()} {lexemas[0].get_value()}'
            print(f"term loaded with value: {symbol.value}")
        elif operation == "load_boolean_constant":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"boolean constant loaded with value: {symbol.value}")
        elif operation == "load_identifier":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"identifier loaded with value: {symbol.value}")
        elif operation == "load_number":
            symbol.value = f'{lexemas[0].get_value()}'
            print(f"number loaded with value: {symbol.value}")
        elif operation == "load_constant":
                print("Acción: load_constant")
        elif operation == "set_relational_equals":
            symbol.value = "=="
            print("Relational operator set to '=='")
        elif operation == "set_relational_not_equals":
            symbol.value = "!="
            print("Relational operator set to '!='")
        elif operation == "set_relational_less":
            symbol.value = "<"
            print("Relational operator set to '<'")
        elif operation == "set_relational_less_equals":
            symbol.value = "<="
            print("Relational operator set to '<='")
        elif operation == "set_relational_greater":
            symbol.value = ">"
            print("Relational operator set to '>'")
        elif operation == "set_relational_greater_equals":
            symbol.value = ">="
            print("Relational operator set to '>='")
        elif operation == "set_addition":
            symbol.value = "+"
            print("Additive operator set to '+'")
        elif operation == "set_subtraction":
            symbol.value = "-"
            print("Additive operator set to '-'")
        elif operation == "set_logical_or":
            symbol.value = "||"
            print("Logical OR set to '||'")
        elif operation == "set_multiplication":
            symbol.value = "*"
            print("Multiplicative operator set to '*'")
        elif operation == "set_division":
            symbol.value = "/"
            print("Multiplicative operator set to '/'")
        elif operation == "set_logical_and":
            symbol.value = "&&"
            print("Logical AND set to '&&'")
        elif operation == "load_true":
            symbol.value = "true"
            print("Boolean constant set to 'true'")
        elif operation == "load_false":
            symbol.value = "false"
            print("Boolean constant set to 'false'")
        elif operation == "load_string":
            symbol.value = f'"{lexemas[1].get_value()}"'
            print(f"String constant loaded with value: {symbol.value}")
        else:
            print("Operación no reconocida.")

    def escribir_en_archivo(self, contenido):
        global rutaOutput
        ruta = rutaOutput
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            print("El contenido se ha escrito correctamente en el archivo.")
        except Exception as e:
            print(f"Ocurrió un error al escribir en el archivo: {e}")


class SymbolItem:
    VARIABLE = 0
    METHOD = 1
    INT = 2
    BOOLEAN = 3
    GLOBAL = 4
    LOCAL = 5

    def __init__(self, id_, function, type_, scope, memory_address, value):
        self._id = id_
        self._function = function
        self._type = type_
        self._scope = scope
        self._memory_address = memory_address
        self._value = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        self._id = id_

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        self._function = function

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_):
        self._type = type_

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        self._scope = scope

    @property
    def memory_address(self):
        return self._memory_address

    @memory_address.setter
    def memory_address(self, memory_address):
        self._memory_address = memory_address

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class SyntaxAnalyzer:
    RESULT_ACCEPT = 0
    RESULT_FAILED = 1

    def __init__(self, prods, lalrList, actions, ruta):
        global productionList
        global Lalr
        global ActionList
        global rutaOutput
        ActionList = actions
        productionList = prods
        Lalr = lalrList
        rutaOutput = ruta
        self.semanticAnalyzer = SemanticAnalyzer()
        self.productions = {}
        self.parsingTable = {}
        self.create_productions()
        self.create_parsing_table()
        self.parsingStack = []

    def create_productions(self):
        global productionList
        global ActionList
        for i, production in enumerate(productionList):
            parts = production.split()  # Dividimos la producción por espacios
            left_side = parts[0]  # El primer elemento es el lado izquierdo
            right_side = parts[1:]  # El resto es el lado derecho
            self.productions[i + 1] = Production(left_side, *right_side);
        # aquí van las actions
        for i, element in enumerate(ActionList):
            indice = i + 1
            if element != "do_nothing":
                self.productions[indice].set_actions(element)

    def create_parsing_table(self):
        global Lalr
        # aquí va la tabla LALR
        for rule in Lalr:
            parts = rule.split(" ")

            # Extraer los componentes de cada regla
            state = int(parts[0])               # Estado actual (número entero)
            symbol = parts[1]                    # Símbolo (cadena de texto)
            operation_type = parts[2].upper()    # Tipo de operación (convertido a mayúsculas)
            next_state = int(parts[3]) if len(parts) > 3 else state  # Estado destino o mismo estado si es 'ACCEPT'
            action = 0
            if operation_type == "SHIFT":
                action = Operation.SHIFT
            elif operation_type == "REDUCE":
                action = Operation.REDUCE
            elif operation_type == "ACCEPT":
                action = Operation.ACCEPT
            elif operation_type == "GOTO":
                action = Operation.GOTO

            # Agregar el estado al diccionario si no existe
            if state not in self.parsingTable:
                self.parsingTable[state] = {}

            # Crear la operación y agregarla al estado en parsing_table
            self.parsingTable[state][symbol] = Operation(action, next_state)

    def parsing(self, tokens):
        state0 = GrammarSymbol(GrammarSymbol.STATE, "0")
        self.parsingStack.append(state0)
        print("Inicializando: Estado inicial 0 en la pila.")

        i = 0
        while i < len(tokens):
            token = tokens[i]
            print(f"Token actual: {token.get_symbol()} con valor {token.get_value()}")

            if self.parsingStack[-1].type == GrammarSymbol.STATE:
                state = int(self.parsingStack[-1].get_symbol())
                to_do = self.parsingTable.get(state, {}).get(token.get_symbol(), None)

                if to_do:
                    if to_do.get_type() == Operation.SHIFT:
                        self.parsingStack.append(token)
                        self.parsingStack.append(GrammarSymbol(GrammarSymbol.STATE, str(to_do.get_state())))
                        print(f"SHIFT: Token {token.get_symbol()} al estado {to_do.get_state()}")
                        i += 1

                    elif to_do.get_type() == Operation.REDUCE:
                        prod = self.productions[to_do.get_production()]
                        index = len(prod.get_symbols()) - 1
                        input_for_semantic_actions = []

                        print(f"REDUCE: Producción {prod.get_non_terminal_key()} -> {' '.join(prod.get_symbols())}")

                        while index >= 0:
                            symbol = prod.get_symbols()[index]
                            if symbol == "ε" or symbol == "Îµ":
                                index -= 1
                            else:
                                self.parsingStack.pop()
                                stack_symbol = self.parsingStack.pop()

                                if stack_symbol.type == GrammarSymbol.TERMINAL and stack_symbol.get_symbol() == symbol:
                                    input_for_semantic_actions.append(stack_symbol)
                                    print(f"REDUCE: Eliminando símbolo terminal {stack_symbol.get_symbol()}")
                                    index -= 1
                                elif stack_symbol.type == GrammarSymbol.NONTERMINAL and stack_symbol.get_symbol() == symbol:
                                    input_for_semantic_actions.append(stack_symbol)
                                    print(f"REDUCE: Eliminando símbolo no terminal {stack_symbol.get_symbol()}")
                                    index -= 1
                                else:
                                    print("ERROR: Símbolo en la pila no coincide con el esperado.")
                                    return self.RESULT_FAILED

                        non_terminal = NonTerminalSymbol(prod.get_non_terminal_key())

                        if prod.get_actions():
                            for action in prod.get_actions():
                                try:
                                    self.semanticAnalyzer.execute_operation(action, input_for_semantic_actions, non_terminal)
                                    print(f"Acción semántica ejecutada: {action}")
                                except Exception:
                                    print("ERROR: Falló la acción semántica. Acción de fallo: " + action)
                                    return self.RESULT_FAILED

                        self.parsingStack.append(non_terminal)
                        print(f"REDUCE: Pushing no terminal {non_terminal.get_symbol()}")

                    elif to_do.get_type() == Operation.ACCEPT:
                        print("ACCEPT: El análisis fue exitoso.")
                        return self.RESULT_ACCEPT

                    else:
                        print("ERROR: Acción desconocida.")
                        return self.RESULT_FAILED
                else:
                    print("ERROR: No hay acción definida en la tabla de parsing.")
                    return self.RESULT_FAILED

            elif self.parsingStack[-1].type == GrammarSymbol.NONTERMINAL:
                non_terminal = self.parsingStack.pop()
                last_state = self.parsingStack.pop()
                state = int(last_state.get_symbol())
                to_do = self.parsingTable[state].get(non_terminal.get_symbol())

                if to_do.get_type() == Operation.GOTO:
                    self.parsingStack.append(last_state)
                    self.parsingStack.append(non_terminal)
                    self.parsingStack.append(GrammarSymbol(GrammarSymbol.STATE, str(to_do.get_state())))
                    print(f"GOTO: Estado {to_do.get_state()} para no terminal {non_terminal.get_symbol()}")

                else:
                    print("ERROR: No hay acción GOTO definida en la tabla de parsing.")
                    return self.RESULT_FAILED

            else:
                print("ERROR: Tipo de símbolo desconocido en la pila.")
                return self.RESULT_FAILED

        print("ACCEPT: El análisis fue exitoso.")
        return self.RESULT_ACCEPT