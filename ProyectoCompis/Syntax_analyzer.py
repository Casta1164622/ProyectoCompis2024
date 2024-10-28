from lexical_analyzer import GrammarSymbol

productionList = []
Lalr = []

class NonTerminalSymbol(GrammarSymbol):
    NONTERMINAL = 1

    def __init__(self, symbol):
        super().__init__(self.NONTERMINAL)
        self.set_symbol(symbol)

    def set_symbol(self, symbol):
        self.symbol = symbol

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

    def execute_operation(self, operation, lexemas, symbol):
        #aquí van las actions
        print("aquí haría una action por que hay reduce")

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

    def __init__(self, prods, lalrList):
        global productionList
        global Lalr
        productionList = prods
        Lalr = lalrList
        self.semanticAnalyzer = SemanticAnalyzer()
        self.productions = {}
        self.parsingTable = {}
        self.create_productions()
        self.create_parsing_table()
        self.parsingStack = []

    def create_productions(self):
        global productionList
        for i, production in enumerate(productionList):
            parts = production.split()  # Dividimos la producción por espacios
            left_side = parts[0]  # El primer elemento es el lado izquierdo
            right_side = parts[1:]  # El resto es el lado derecho
            self.productions[i + 1] = Production(left_side, *right_side);
        # aquí van las actions

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
                                    print("ERROR: Falló la acción semántica.")
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