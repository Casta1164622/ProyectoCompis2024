from state import State, lalrState
from table import term_and_nonterm, calculate_first, get_augmented, find_states, combine_states, get_parse_table
from map import reverse_simplify_grammar

def read_grammar_from_string(grammar_string):
    """Lee la gramática desde una cadena y la devuelve en formato adecuado"""
    grammar = []
    
    # Separar la cadena por líneas
    lines = grammar_string.splitlines()
    
    # Procesar cada línea
    for line in lines:
        # Eliminar espacios y saltos de línea
        line = line.strip().replace(' ', '')
        
        # Si la línea no está vacía
        if line != '':
            # Separar la línea en lado izquierdo (lhs) y derecho (rhs) por '->'
            lhs, rhs = line.split('->')
            
            # Si hay varias producciones separadas por '|'
            if '|' in rhs:
                # Dividir las producciones y agregarlas
                for prod in rhs.split('|'):
                    grammar.append([lhs, prod])
            else:
                # Si solo hay una producción, agregarla
                grammar.append([lhs, rhs])
    
    return grammar


def generate_lalr_table(grammar):
    """Genera la tabla LALR dada una gramática"""
    # Inicialización de variables
    term = []
    non_term = []
    first = {}
    augment_grammar = []
    states = []
    lalr_states = []
    parse_table = []

    # Proceso
    term_and_nonterm(grammar, term, non_term)
    calculate_first(grammar, first, term, non_term)
    get_augmented(grammar, augment_grammar)
    find_states(states, augment_grammar, first, term, non_term)
    combine_states(lalr_states, states)
    get_parse_table(parse_table, lalr_states, augment_grammar)

    return parse_table, term, non_term

def display_parse_table(parse_table, term, non_term, asignaciones):
    """Muestra la tabla LALR en un archivo de texto, aplicando reverse_simplify_grammar a cada línea."""
    all_symbols = term + ['$'] + non_term
    
    with open("tabla.txt", "w") as file:
        # Encabezado de la tabla
        header = '{:12}'.format('') + ''.join(f'{symb:12}' for symb in all_symbols)
        file.write(header + '\n')
        file.write('-' * len(header) + '\n')

        # Imprimir cada fila de la tabla
        for index, state in enumerate(parse_table):
            row = '{:<12}'.format(index)
            for symbol in all_symbols:
                if symbol in state:
                    action = state[symbol]
                    if action > 0:
                        row += '{:<12}'.format(f's{action}')
                    elif action < 0:
                        row += '{:<12}'.format(f'r{-action}')
                    elif action == 0:
                        row += '{:<12}'.format('accept')
                else:
                    row += '{:<12}'.format('')

            # Aplicar reverse_simplify_grammar a la fila generada
            row_simplified = reverse_simplify_grammar(row, asignaciones)
            
            # Escribir la fila en el archivo
            file.write(row_simplified + '\n')

def leer_input_txt_como_string():
    ruta_archivo = 'input.txt'
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read().replace('\n', ' ')
    return contenido

def generate_lalr_list(parse_table, term, non_term):
    """
    Genera una lista de strings en el formato:
    "estado símbolo operación estado_destino" para cada entrada en la tabla LALR.
    """
    lalr_list = []
    all_symbols = term + ['$'] + non_term  # Todos los símbolos en el orden terminales + '$' + no terminales

    for state_index, state in enumerate(parse_table):
        for symbol in all_symbols:
            # Primero verificamos si es un no terminal para manejar GoTo
            if symbol in non_term and symbol in state:
                goto_state = state[symbol]
                line = f"{state_index} {symbol} goto {goto_state}"
                lalr_list.append(line)

            # Si es un terminal o '$', manejamos shift, reduce, o accept
            elif symbol in term + ['$']:
                if symbol in state:
                    action = state[symbol]
                    if action > 0:
                        operation = "shift"
                        destination = action
                    elif action < 0:
                        operation = "reduce"
                        destination = -action
                    elif action == 0:
                        operation = "accept"
                        destination = ''
                    else:
                        continue  # Si no hay acción, se salta

                    # Formateamos la salida según el tipo de operación
                    if operation != "accept":
                        line = f"{state_index} {symbol} {operation} {destination}"
                    else:
                        line = f"{state_index} {symbol} {operation}"

                    lalr_list.append(line)
                
    return lalr_list

