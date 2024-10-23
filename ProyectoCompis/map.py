def asign(cadena):
    # Diccionario para guardar las asignaciones
    asignaciones = {}
    
    asignaciones['ε'] = 'e'
    asignaciones['Îµ'] = 'e'

    # Letras para no terminales (mayúsculas) y terminales (minúsculas)
    letras_mayus = iter([chr(i) for i in range(ord('A'), ord('Z') + 1)])
    letras_minus = iter([chr(i) for i in range(ord('a'), ord('z') + 1) if chr(i) != 'e'])
    
    # Caracteres especiales para no terminales cuando se acaben las mayúsculas
    caracteres_especiales_mayus = iter(['!', '@', '_', '(', '%', '^', '&', '*', '-', '+'])

    # Caracteres especiales para terminales cuando se acaben las minúsculas
    caracteres_especiales_minus = iter(['~', '`', '\\', '/', '[', ']', '{', '}', ':', ';', '"', '<', '=', '#', ',', '?'])

    # Separar la cadena en líneas
    lineas = cadena.splitlines()
    
    # Procesar cada línea
    for linea in lineas:
        # Separar la línea por espacios
        partes = linea.split(" ")
        
        # Procesar cada parte
        for parte in partes:
            # Si es un no terminal (entre < >)
            if parte.startswith('<') and parte.endswith('>'):
                if parte not in asignaciones:
                    # Usar la siguiente letra mayúscula o un carácter especial si se acaban
                    try:
                        asignaciones[parte] = next(letras_mayus)
                    except StopIteration:
                        asignaciones[parte] = next(caracteres_especiales_mayus)
            # Si es un terminal (entre ' ')
            elif parte.startswith("'") and parte.endswith("'"):
                if parte not in asignaciones:
                    # Asignar la siguiente letra minúscula o un carácter especial si se acaban
                    try:
                        asignaciones[parte] = next(letras_minus)
                    except StopIteration:
                        asignaciones[parte] = next(caracteres_especiales_minus)
    
    return asignaciones

def simplify_grammar(cadena, asignaciones):
    """Reemplaza los no terminales y terminales en la cadena según el diccionario de asignaciones."""
    # Separar la cadena en líneas
    lineas = cadena.splitlines()
    
    nueva_cadena = []
    
    # Procesar cada línea
    for linea in lineas:
        partes = linea.split(" ")  # Separar la línea por espacios
        nueva_linea = []
        
        # Procesar cada parte
        for parte in partes:
            # Si la parte está en el diccionario de asignaciones, se reemplaza
            if parte in asignaciones:
                nueva_linea.append(asignaciones[parte])
            else:
                nueva_linea.append(parte)  # Si no está, se deja igual
        
        # Unir las partes nuevamente en una línea
        nueva_cadena.append(" ".join(nueva_linea))
    
    # Unir todas las líneas en una sola cadena con saltos de línea
    return "\n".join(nueva_cadena)