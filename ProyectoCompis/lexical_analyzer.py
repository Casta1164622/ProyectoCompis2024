import re
from typing import List, Dict, Any

class GrammarSymbol:
    TERMINAL = 0
    NONTERMINAL = 1
    STATE = 2

    def __init__(self, symbol_type: int, symbol: str = None):
        self.attributes: Dict[str, Any] = {}
        self.types: List[int] = []
        self.type: int = symbol_type
        self.symbol: str = symbol

    def get_symbol(self) -> str:
        return self.symbol

class Lexema(GrammarSymbol):
    def __init__(self, symbol: str, value: str):
        super().__init__(GrammarSymbol.TERMINAL, symbol)
        self.value: str = value

    def get_value(self) -> str:
        return self.value

class LexicalAnalyzer:
    def __init__(self, compiler):
        self.compiler = compiler
        self.token_patterns = self.compile_token_patterns()

    def convert_cset_to_regex(self, set_string: str) -> str:
        """Convierte un conjunto definido en el compilador a una expresión regular."""
        set_string = set_string.replace("'", "")
        if '..' in set_string:
            parts = set_string.split('..')
            return f'[{parts[0]}-{parts[1]}]'
        return set_string

    def compile_token_patterns(self) -> List[re.Pattern]:
        patterns = []

        # Convertir los conjuntos de caracteres desde el compilador
        digit_set = self.convert_cset_to_regex(self.compiler.Csets.get('digit', '[0-9]'))
        letter_set = self.convert_cset_to_regex(self.compiler.Csets.get('letter', '[A-Za-z_]'))
        charset = self.convert_cset_to_regex(self.compiler.Csets.get('charset', '[\x20-\xFE]'))

        # Procesar cada token en el compilador y generar su patrón regex
        for token in self.compiler.tokens:
            token = token.strip()

            if "number" in token:
                patterns.append((re.compile(digit_set + r'+'), 'number'))  # Uno o más dígitos
            elif "identifier" in token:
                # Definir identificadores: letra seguida de letras o dígitos
                patterns.append((re.compile(letter_set + r'(?:' + letter_set + r'|' + digit_set + r')*'), 'identifier'))
            elif "str" in token:
                # Cadenas: conjunto de caracteres seguidos de más conjuntos de caracteres
                patterns.append((re.compile(charset + r'+'), 'str'))
            else:
                # Para operadores, símbolos y tokens restantes
                operator_tokens = re.findall(r"'.+?'", token)  # Capturar operadores dentro de comillas simples
                for op in operator_tokens:
                    op_clean = op.replace("'", "")  # Limpiar comillas
                    patterns.append((re.compile(re.escape(op_clean)), op_clean))  # Escapar el operador

        return patterns

    def get_lexical_tokens(self, input_string: str) -> List[Lexema]:
        tokens = []

        # Primero verificar las keywords explícitamente
        keyword_set = set([kw.replace("'", "") for kw in self.compiler.keywords])

        # Obtener operadores desde los tokens del compilador
        operator_tokens = []
        for token in self.compiler.tokens:
            operator_tokens += re.findall(r"'.+?'", token)  # Extraer operadores

        # Dividir la entrada por espacios
        words = input_string.split()

        for word in words:
            index = 0
            while index < len(word):
                matched = False

                # Verificar si el token es un operador de los definidos
                for op in sorted(operator_tokens, key=len, reverse=True):  # Operadores más largos primero
                    op_clean = op.replace("'", "")  # Limpiar comillas del operador
                    if word[index:].startswith(op_clean) and \
                            (index + len(op_clean) == len(word) or not word[index + len(op_clean)].isalnum()):
                        tokens.append(Lexema(op_clean, op_clean))
                        index += len(op_clean)
                        matched = True
                        break

                if matched:
                    continue  # Ya se manejó como operador

                # Verificar si es una palabra clave
                for keyword in sorted(keyword_set, key=len, reverse=True):
                    if word[index:].startswith(keyword) and \
                            (index + len(keyword) == len(word) or not word[index + len(keyword)].isalnum()):
                        tokens.append(Lexema(keyword, keyword))
                        index += len(keyword)
                        matched = True
                        break

                if matched:
                    continue

                # Verificar si el token es un "identifier": empieza con una "letter"
                if re.match(r'[A-Za-z_]', word[index]):
                    identifier_match = re.match(r'[A-Za-z_][A-Za-z0-9_]*', word[index:])
                    if identifier_match:
                        tokens.append(Lexema("identifier", identifier_match.group()))
                        index += len(identifier_match.group())
                        matched = True
                        continue

                # Verificar si el token es un "number": comienza con un dígito
                if re.match(r'[0-9]', word[index]):
                    number_match = re.match(r'[0-9]+', word[index:])
                    # Si el número no está seguido de una letra, es un número válido
                    remaining_input = word[index + len(number_match.group()):]
                    if not remaining_input or not re.match(r'[A-Za-z_]', remaining_input[0]):
                        tokens.append(Lexema("number", number_match.group()))
                        index += len(number_match.group())
                        matched = True
                        continue
                    else:
                        # Si hay letras después del número, es una cadena (str)
                        tokens.append(Lexema("str", word))
                        matched = True
                        break

                # Verificar si el token es un "str": comienza con cualquier cosa que no sea una "letter"
                if re.match(r'[^\w]', word[index]) or re.match(r'[^A-Za-z_]', word[0]):
                    tokens.append(Lexema("str", word))
                    matched = True
                    break

                # Si no hubo coincidencia, avanzar
                index += 1

        # Agregar el token de final de archivo
        tokens.append(Lexema("$", "eof"))

        return tokens
