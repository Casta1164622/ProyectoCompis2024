from re import L, split
import re
import produccion
class ccompiler:
    
    nombre = ""
    units = []
    Csets = {}
    tokens = []
    keywords = []
    productions = []
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
                        readingList = line.replace('\t','').replace(';\n','').split('=')
                        newProduction = produccion.produccion(readingList[0].replace(' ',''))
                        self.productionNames.append(readingList[0].replace(' ',''))
                        readingList = readingList[1].replace('\n','').split('|')
                        for item in readingList:
                            if('{' in item):
                                NewreadingList = item.split('{')
                                newProduction.producciones.append(NewreadingList[0])
                                
                                NewreadingList = NewreadingList[1].replace('}','').split(',')
                                for action in NewreadingList:
                                    newProduction.actions.append(action)

                            else:
                                if('Îµ' in item):
                                    newProduction.producciones.append('ε')
                                else:
                                    newProduction.producciones.append(item)
                        self.productions.append(newProduction)
    
    def checkCompiler(self):
        failed = False
        wordList = []
        for prodItem in self.productions:
            for producionItem in prodItem.producciones:
                wordList = producionItem.split()
                for word in wordList:
                    word = word
                    if('<' in word and '>' in word):
                        if(word in self.productionNames):
                            print(word+' Cuenta con una produccion \n')
                        else:
                            print("ERROR: El no terminal "+word+" no cuenta con una definicion \n")
                            failed = True
                    else:
                        if(word in 'ε'):
                            print('ε')
                        elif(word in self.keywords):
                            print(word + " encontrado en KEYWORDS")
                        elif(word in '\t'.join(self.tokens)):
                            print(word + " econtrado en TOKENS")
                        elif(word in self.Csets.keys()):
                            print(word + " econtrado en SETS")
                        elif(len(word.replace("'",''))):
                            foundMatch = False
                            charset = ''
                            charset = self.Csets.get('charset').replace('chr(', '').replace(')', '')
                            
                            start, end = [c for c in charset.split('..')]
                            pattern = f'[{chr(int(start))}-{chr(int(end))}]'

                            if(re.match(pattern, word)):
                                foundMatch = True
                                print(word+" encontrado en el rango del charset")

                            if(not foundMatch):
                                print("ERROR: el terminal "+word+" no esta definido o en un rango de charset")
                                failed = True
                        else:
                            print("ERROR: el terminal "+word+" no esta definido")
                            failed = True
        if(failed):
            print("El chequeo falló :o")
        else:
            print("Todo correcto :D")
                
    def getProductionsString(self):
        productions_str = ""
        for prod in self.productions:
        # Usamos un solo espacio después de "->"
            prod_str = f"{prod.nombre} ->{'|'.join(prod.producciones)}"
        # Reemplazamos "|ε" por "| ε" para que ε no esté pegado al "|"
            prod_str = prod_str.replace('|ε', '| ε')
            productions_str += prod_str + '\n'
        return productions_str


