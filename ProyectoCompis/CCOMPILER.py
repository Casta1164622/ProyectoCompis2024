﻿from re import L, split
import re
class ccompiler:
    
    nombre = ""
    units = []
    Csets = {}
    tokens = []
    keywords = []
    productions = {}
    actions = {}
    productionNames = []
    

    def __init__(self,file_dir):
        self.file_dir = file_dir
    
    def loadCompiler(self):
        readingUnits = False
        readingSets = False
        readingTokens = False
        readingKeyWords = False
        readingProductions = False
        readingList = []

        with open(self.file_dir) as file:
            for line in file:
                if "COMPILER" in line:
                    self.nombre = line.replace('COMPILER','').replace('\n','')
                if "UNITS" in line:
                    readingUnits = True
                elif "SETS" in line:
                    readingSets = True 
                    readingUnits = False
                elif "TOKENS" in line:
                    readingTokens = True
                    readingSets = False
                elif "KEYWORDS" in line:
                    readingKeyWords = True
                    readingTokens = False
                elif "PRODUCTIONS" in line:
                    readingProductions = True
                    readingKeyWords = False
                
                if(readingUnits):
                    self.units = line.replace(';\n','').replace('\t','').split(",")
                elif(readingSets):
                    readingList = line.split('=')
                    if(len(readingList)>1):
                        self.Csets[readingList[0].replace('\t','').replace(' ','')] = readingList[1].replace(';\n','').replace(' ','')
                elif(readingTokens):
                    if "TOKENS" not in line:
                        self.tokens.append(line.replace('\t','').replace(';\n',''))
                elif(readingKeyWords):
                    if "KEYWORDS" not in line:
                        readingList = line.replace('\t','').replace(';\n','').replace(',\n','').split(',')
                        for item in readingList:
                            self.keywords.append(item)
                elif(readingProductions):
                    if "PRODUCTIONS" not in line:

                        left_side = re.match(r"^(.*?)(?==)", line).group().strip()   # Left side before '='
                        middle_side = re.search(r"=(.*?)(?={)", line).group(1).strip()  # Middle part between '=' and '{'
                        right_side = re.search(r"{.*}", line).group().strip('{').strip('}')       # Right side with '{'

                            # Split the right-hand side by '|' and strip spaces
                        middle_options = [option.strip() for option in middle_side.split('|')]
                        right_options = [option.strip() for option in right_side.split(',')]
                        
                        self.productionNames.append(left_side.strip())
                            # Add to actios
                        self.actions[left_side.strip()] = right_options
                            # Add to productions
                        self.productions[left_side.strip()] = middle_options
                        
    
    def checkCompiler(self):
        failed = False
        wordList = []
        for prodItem in self.productions:
            for values in self.productions[prodItem]:
                for producionItem in values.split(' '):
                    if('<' in producionItem and '>' in producionItem and not producionItem == "'<>'"):
                        if(producionItem in self.productionNames):
                            print(producionItem+' Cuenta con una produccion \n')
                        else:
                            print("ERROR: El no terminal "+producionItem+" no cuenta con una definicion \n")
                            failed = True
                    else:
                        if(producionItem in 'ε'):
                            print('ε')
                        elif(producionItem in self.keywords):
                            print(producionItem + " encontrado en KEYWORDS")
                        elif(producionItem in '\t'.join(self.tokens)):
                            print(producionItem + " econtrado en TOKENS")
                        elif(producionItem in self.Csets.keys()):
                            print(producionItem + " econtrado en SETS")
                        elif(len(producionItem.replace("'",''))):
                            foundMatch = False
                            charset = ''
                            charset = self.Csets.get('charset').replace('chr(', '').replace(')', '')
                            
                            start, end = [c for c in charset.split('..')]
                            pattern = f'[{chr(int(start))}-{chr(int(end))}]'

                            if(re.match(pattern, producionItem)):
                                foundMatch = True
                                print(producionItem+" encontrado en el rango del charset")

                            if(not foundMatch):
                                print("ERROR: el terminal "+producionItem+" no esta definido o en un rango de charset")
                                failed = True
                        else:
                            print("ERROR: el terminal "+producionItem+" no esta definido")
                            failed = True
        if(failed):
            print("El chequeo falló :o")
            return False
        else:
            print("Todo correcto :D")
            return True

    def productionsTostring(self):
        productions_str = ""
        for lhs, rhs in self.productions.items():
            rhs_str = ' | '.join(rhs)
            productions_str += f"{lhs} -> {rhs_str}\n"
        return productions_str
    
    def Production_list(self):
        production_list = []
        for lhs, rhs in self.productions.items():
            for opcion in rhs:
                produccion = f"{lhs} {opcion}"
                production_list.append(produccion)
        return production_list
    
    def getFlattenedActionsList(self):
        flattened_actions = []
        for production in self.productionNames:
            if production in self.actions:
                flattened_actions.extend(self.actions[production])
        return flattened_actions
