class Token:
    def __init__(self, valor, classe):
        self.valor = valor
        self.classe = classe

class AnalisadorSintatico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.posicao = 0

    def proximo_token(self):
        if self.posicao < len(self.tokens):
            self.posicao += 1
            return self.tokens[self.posicao - 1]
        return None

    def programa(self):
        self.sequencia_de_comandos()
        # token = self.proximo_token()
        token = self.tokens[self.posicao].valor
        #print("fim de comando: ", token)
        if token == "END":
            if self.tokens[self.posicao - 1].valor == ';':
                print("Análise sintática finalizada!")
            else: 
                print("Erro! Esperado ; antes de END")
        else:
            print("Erro! Esperado 'END'.")

    def sequencia_de_comandos(self):
        while True:
            #print("iniciar cmando: ", self.tokens[self.posicao].valor)
            self.comando()
            #print("depois de cmando ", self.tokens[self.posicao].valor)  #ver por que isso esta dando = a ELSE n tokens3
            token = self.tokens[self.posicao]
            # print("ponto: ", token.valor)
            if not token or token.valor != ";":
                break
            if token.valor == ";":
                try:
                    if self.tokens[self.posicao + 1].valor == 'END':
                        self.proximo_token()
                        break
                    elif self.tokens[self.posicao + 1].classe == 'res':
                        self.proximo_token()
                    else:
                        pass
                except IndexError:
                    print('Esperava-se algo depois da virgula')
                    break

    def comando(self):
        if self.posicao + 1 < len(self.tokens):
            token = self.proximo_token()
        # print("comeco do comando: ",token.valor)
            if token.valor == "LET":
                self.atribuicao()
            elif token.valor == "GO":
                self.desvio()
            elif token.valor == "READ":
                self.leitura()
            elif token.valor == "PRINT":
                self.impressao()
            elif token.valor == "IF":
                self.decisao()
            elif token.classe == "rótulo":
                self.proximo_token()
                token = self.proximo_token()
                if token and token.valor == ":":
                    self.comando()
                else:
                    print("Erro! Esperado ':' após rótulo.")
            else:
                print("Erro! Comando inválido.")
        else: 
            print("Não foi identificado o comando seguinte")

    def atribuicao(self):
        token = self.proximo_token()
        if token and token.classe == "identificador":
            token = self.proximo_token()
            if token and token.valor == ":=":
                self.expressao()
                # print(self.tokens[self.posicao].valor)
            else:
                print("Erro! Esperado ':=' após identificador.")
        else:
            print("Erro! Esperado identificador.")

    def expressao(self):
        #print("token 2: ", self.tokens[self.posicao].valor)
        self.termo()
        #print("depois do term")
        token = self.tokens[self.posicao]
        #print("TOKEN 2: ", token.valor, token.classe)
        #print(self.tokens[self.posicao].valor)
        while token and token.valor in ["+", "-"]:
            self.proximo_token()  # Consumir operador
            self.termo()
            token = self.proximo_token()

    def termo(self):
        #print("token 3: ", self.tokens[self.posicao].valor)
        self.fator()
        token = self.tokens[self.posicao]
        #print("TOKEN 3: ", token.valor, token.classe)
        while token and token.valor in ["*", "/"]:
            self.proximo_token()  # Consumir operador
            self.fator()
            token = self.proximo_token()

    def fator(self):
        #print("token 4: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
        #print("TOKEN 4: ", token.valor, token.classe)
        if token and token.classe == "identificador":
            self.proximo_token() # Consumir identificador
        elif token and token.classe == "número":
            self.proximo_token()  # Consumir número
        elif token and token.valor == "<":
            self.proximo_token()  # Consumir "<"
            self.expressao()
            token = self.proximo_token()
            if token and token.valor == ">":
                self.proximo_token()  # Consumir ">"
            else:
                print("Erro! Esperado '>' após expressão.")
        else:
            print("Erro! Fator inválido.")

    def desvio(self):
        token = self.tokens[self.posicao]
        if token and token.valor == "TO":
            #print("entrou no to: ", self.tokens[self.posicao].valor)
            self.proximo_token()  # Consumir "TO"
            token = self.tokens[self.posicao]
            if token:
                if token.classe == "rótulo":
                    self.proximo_token()  # Consumir rótulo
                    token = self.tokens[self.posicao]
                    if token and token.valor == ";":
                        self.proximo_token()
                        self.lista_de_rótulos()
                        self.comando()
                    elif token and token.valor != ";":
                        print("Erro! Esperado ;")
                elif token.classe == "identificador":
                    idSalvo = token
                    self.proximo_token()  # Consumir identificador
                    token = self.tokens[self.posicao]
                    if token and token.valor == "OF":
                        #print("entrou no OF: ", self.tokens[self.posicao].valor)
                        self.proximo_token()  # Consumir OF
                        self.lista_de_rótulosComID(idSalvo)
                    else:
                        print("Erro! Esperado 'OF' após identificador em GO TO.")
            

                # if token and token.valor == "OF":
                #     print("entrou em OF: ", self.tokens[self.posicao].valor)
                #     self.proximo_token()  # Consumir "OF"
                #     self.lista_de_rótulos()
                # else:
                #     print("Erro! Esperado 'OF' após rótulo.")
            else:
                print("Erro! Esperado rótulo.")
        elif token and token.classe == "rótulo":
            self.proximo_token()  # Consumir rótulo
        else:
            print("Erro! Desvio inválido.")
        #print("fim do desvio",self.tokens[self.posicao].valor)

    def lista_de_rótulos(self):
        token = self.tokens[self.posicao]
        #print("lista de rotulos: ", token.valor)
        while token and token.classe != "rótulo":
           # print("entrouAqui")
            self.proximo_token()
            if(self.tokens[self.posicao].classe == "rótulo"):
                self.proximo_token()
                break
            
            
            # print("entrou no rtulo: ", self.tokens[self.posicao].valor)
            # self.proximo_token()  # Consumir rótulo
            # print("entrou no rtulo: ", self.tokens[self.posicao].valor)
            # token = self.proximo_token()
            # if token and token.valor == ",":
            #     self.proximo_token()  # Consumir ","
            #     token = self.proximo_token()
            # else:
            #     break

    def lista_de_rótulosComID(self, id):
        token = self.tokens[self.posicao]   #salva o rotulo a pesquisa 
        rotuloDesejado = []  
        rotuloDesejado.append(token.valor)
        i = 0   #indice do while
        idDesejado = id
        #print(idDesejado.valor)
        #print("lista de rotulosID: ", token.valor)
        self.proximo_token()    #consome o rotulo
        while True:
            #print("entrouRotuloDesejado")
            # print("antes da virgula: ",self.tokens[self.posicao].valor)
            while self.tokens[self.posicao].valor == ',':
                self.proximo_token()    #pula a virgula
                rotuloDesejado.append(self.tokens[self.posicao].valor)
                self.proximo_token()    #pula outro rotulo
            
            # print("antes do ponto e virgula: ",self.tokens[self.posicao].valor)

            if self.tokens[self.posicao].valor == ';':
                self.proximo_token()

            # print("antes da funcao: ",self.tokens[self.posicao].valor)
            # print(rotuloDesejado[0], rotuloDesejado[1])
            if(self.tokens[self.posicao].valor in rotuloDesejado):
                # print("encontrou oum rotulo: ", self.tokens[self.posicao].valor)
                self.proximo_token()
                if(self.tokens[self.posicao].valor == idDesejado.valor):
                    #print("aqui: ",self.tokens[self.posicao].valor)
                    self.proximo_token()
                    break
            self.proximo_token()
                
                

    def leitura(self):
        # self.proximo_token()  # Consumir "READ"
        self.lista_de_identificadores()

    def lista_de_identificadores(self):
        token = self.proximo_token()
        while token and token.classe == "identificador":
            # self.proximo_token()  # Consumir identificador
            # token = self.proximo_token()
            token = self.proximo_token()
            if token and token.valor == ",":
                # self.proximo_token()  # Consumir ","
                token = self.proximo_token()
            else:
                break

    def impressao(self):
        #print("primeira: ", self.tokens[self.posicao].valor)
        self.lista_de_expressões()


    def lista_de_expressões(self):
        self.expressao()
        #print("depois de expressao: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
       # print("depois da expressao: ", token.valor)
        if token.classe == "identificador":
            print("Erro! Esperado ',' entre identificadores")
        else:
            while token and token.valor == ",":
                #print("entes de tira virgula; ", self.tokens[self.posicao].valor)
                self.proximo_token()  # Consumir ","
                # print("pulou , agra e: ", self.tokens[self.posicao].valor)
                self.expressao()
                # print("saiu expressao ,: ",self.tokens[self.posicao].valor)
                token = self.tokens[self.posicao]

    def decisao(self):
       # print("token 1: ", self.tokens[self.posicao].valor)
        self.comparação()
        token = self.tokens[self.posicao]
       # print("TOKEN 1: ", token.valor, token.classe)
        if token and token.valor == "THEN":
            self.proximo_token()  # Consumir "THEN"
            self.comando()
          #  print("teste 2: ", self.tokens[self.posicao].valor)
            if self.tokens[self.posicao].valor == ';':
                self.proximo_token()

            token = self.tokens[self.posicao]
            if token and token.valor == "ELSE":
            #    print("entrou no else: ", self.tokens[self.posicao].valor)
                self.proximo_token()  # Consumir "ELSE"
                self.comando()
        else:
            print("Erro! Esperado 'THEN' após comparação.")

    def comparação(self):
     #   print("token 1.5: ", self.tokens[self.posicao].valor)
        self.expressao()
     #   print("token 1.55: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
     #   print("TOKEN 1.5: ", token.valor, token.classe)
        if token and token.classe == "operador de comparação":
            self.proximo_token()  # Consumir operador de comparação
            self.expressao()
        else:
            print("Erro! Esperado operador de comparação.")


tokens = [ #EXEMPLO
    Token("READ", "res"),  
    Token("x", "identificador"),  
    Token(",", "sim"), 
    Token("y", "identificador"),  
    Token(";", "sim"), 
    Token("END", "res")
]

tokens1 = [ #LET
    Token("LET", "res"),  
    Token("x", "identificador"),  
    Token(":=", "sim"),
    Token("5", "número"),  
    Token(";", "sim"),  
    Token("END", "res")
]

tokens2 = [ #PRINT
    Token("PRINT", "res"), 
    Token("x", "identificador"),  
    Token(",", "sim"),  
    Token("y", "identificador"), 
    Token(";", "sim"),  
    Token("END", "res")
]

tokens3 = [ #IF ELSE
    Token("IF", "res"),  
    Token("x", "identificador"),  
    Token(">", "operador de comparação"),  
    Token("y", "identificador"),  
    Token("THEN", "res"), 
    Token("PRINT", "res"),  
    Token("x", "identificador"),  
    Token(";", "sim"),  
    Token("ELSE", "res"),  
    Token("PRINT", "res"),  
    Token("y", "identificador"),  
    Token(";", "sim"),  
    Token("END", "res")
]

tokens4 = [ # GO TO
    Token("GO", "res"), 
    Token("TO", "res"),  
    Token("rótulo1", "rótulo"),  
    Token(";", "sim"), 
    Token("END", "res"),
    Token("rótulo1", "rótulo"),  
    Token("PRINT", "res"),  
    Token("x", "identificador"), 
    Token(";", "sim"),
    Token("END", "res")  
]

tokens5 = [ # GO TO x OF
    Token("GO", "res"),       
    Token("TO", "res"),   
    Token("x", "identificador"),    
    Token("OF", "res"),      
    Token("rótulo1", "rótulo"),   
    Token(";", "sim"),        
    Token("END", "res"),
    Token("rótulo1", "rótulo"),  
    Token("x", "identificador"),
    Token(";", "sim"),
    Token("END", "res")       
]

tokens_completo = [ # JUNÇÃO DE TODAS
    Token("LET", "res"),  
    Token("x", "identificador"),  
    Token(":=", "sim"),
    Token("5", "número"),  
    Token(";", "sim"),
    Token("PRINT", "res"), 
    Token("x", "identificador"),  
    Token(",", "sim"),  
    Token("y", "identificador"), 
    Token(";", "sim"),  
    Token("IF", "res"),  
    Token("x", "identificador"),  
    Token(">", "operador de comparação"),  
    Token("y", "identificador"),  
    Token("THEN", "res"), 
    Token("PRINT", "res"),  
    Token("x", "identificador"),  
    Token(";", "sim"),  
    Token("ELSE", "res"),  
    Token("PRINT", "res"),  
    Token("y", "identificador"),  
    Token(";", "sim"),
    Token("GO", "res"), 
    Token("TO", "res"),  
    Token("rótulo1", "rótulo"),  
    Token(";", "sim"), 
    Token("END", "res"),
    Token("rótulo1", "rótulo"),  
    Token("PRINT", "res"),  
    Token("x", "identificador"), 
    Token(";", "sim"),
    Token("GO", "res"),       
    Token("TO", "res"),   
    Token("x", "identificador"),    
    Token("OF", "res"),      
    Token("rótulo1", "rótulo"),   
    Token(";", "sim"),        
    Token("END", "res"),
    Token("rótulo1", "rótulo"),  
    Token("x", "identificador"),
    Token(";", "sim"),
    Token("END", "res")
] 

tokensComVirgula = [
    Token("GO", "res"), 
    Token("TO", "res"),  
    Token("x", "identificador"),    
    Token("OF", "res"),      
    Token("rótulo1", "rótulo"),   
    Token(",", "sim"),
    Token("rótulo2", "rótulo"),   
    Token(";", "sim"),        
    Token("END", "res"),
    Token("rótulo2", "rótulo"),  
    Token("x", "identificador"),
    Token(";", "sim"),
    Token("END", "res")       
] 

analisador = AnalisadorSintatico(tokensComVirgula)
analisador.programa()