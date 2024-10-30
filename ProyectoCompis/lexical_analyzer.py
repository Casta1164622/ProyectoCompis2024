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
        super().__init__(GrammarSymbol.TERMINAL, symbol if symbol == "$" else f"'{symbol}'")
        self.value: str = value

    def get_value(self) -> str:
        return self.value

class LexicalAnalyzer:
    def __init__(self, compiler):
        self.compiler = compiler
        self.sets_patterns = self.compile_token_patterns()
        self.token_patterns = self.convert_token_to_pattern()
    
    def convert_token_to_pattern(self):
        patterns = []
        number = self.compiler.tokens[0].split("=")[1].replace("digit", self.sets_patterns[0])
        number = number.replace(" ", "")
        patterns.append(number)
        identifier = self.compiler.tokens[1].split("=")[1].replace("digit", self.sets_patterns[0])
        identifier = identifier.replace("letter", self.sets_patterns[1])
        identifier = identifier.replace("check", "")
        identifier = identifier.replace(" ", "")
        patterns.append(identifier)
        return patterns

    def convert_cset_to_regex(self, set_string: str) -> str:  # Convertimos los Csets en Regex
        set_string = set_string.replace("'", "")
        set_string = set_string.replace("+", "")
        
        if '..' in set_string:
            parts = set_string.split('..')
            if len(parts) < 3:
                if "chr" in parts[0] and "chr" in parts[1]:
                    begin = int(parts[0].replace("chr(", "").replace(")", ""))
                    end = int(parts[1].replace("chr(", "").replace(")", ""))
                    begin_hex = f"{begin:02x}"
                    end_hex = f"{end:02x}"
                    
                    return f"[\\x{begin_hex}-\\x{end_hex}]"
                else:
                    return f"[{parts[0]}-{parts[1]}]"
            else:
                return f"[{parts[0]}-{parts[1]}-{parts[2]}]"
        
        return set_string


    def compile_token_patterns(self) -> List[re.Pattern]:
        patterns = []
        digit_set = self.convert_cset_to_regex(self.compiler.Csets.get('digit'))
        patterns.append(digit_set)
        letter_set = self.convert_cset_to_regex(self.compiler.Csets.get('letter'))
        patterns.append(letter_set)
        charset = self.convert_cset_to_regex(self.compiler.Csets.get('charset'))
        patterns.append(charset)

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
                if re.match(self.sets_patterns[1], word[index]):
                    identifier_match = re.match(self.token_patterns[1], word[index:])
                    if identifier_match:
                        tokens.append(Lexema("identifier", identifier_match.group()))
                        index += len(identifier_match.group())
                        matched = True
                        continue

                # Verificar si el token es un "number": comienza con un dígito
                if re.match(self.sets_patterns[0], word[index]):
                    number_match = re.match(self.token_patterns[0], word[index:])
                    # Si el número no está seguido de una letra, es un número válido
                    remaining_input = word[index + len(number_match.group()):]
                    if not remaining_input or not re.match(self.sets_patterns[1], remaining_input[0]):
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
                if re.match(r'[^\w]', word[index]) or not re.match(r'[^A-Za-z_]', word[0]):
                    tokens.append(Lexema("str", word))
                    matched = True
                    break

                # Si no hubo coincidencia, avanzar
                index += 1

        # Agregar el token de final de archivo
        tokens.append(Lexema("$", "eof"))

        return tokens
