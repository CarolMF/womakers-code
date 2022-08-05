import os

VAGAS_PARA_CARRO = 25
VAGAS_PARA_MOTO = 25

class Veiculo:
    def __init__(self, placa):
        self._placa = placa
        self.estacionado = False

    @property
    def placa(self):
        return self._placa

    def estacionar(self):
        self.estacionado = True

    def sair_da_vaga(self):
        self.estacionado = False

class Carro(Veiculo):
    def __init__(self, placa):
        super().__init__(placa)
        self.tipo = "carro"

    @property 
    def placa(self):
        return self._placa
    
    def estacionar(self):
        return super().estacionar()
    def sair_da_vaga(self):
        return super().sair_da_vaga()  

class Moto(Veiculo):
    def __init__(self, placa):
        super().__init__(placa)
        self.tipo = "moto"

    def estacionar(self):
        return super().estacionar()
    def sair_da_vaga(self):
        return super().sair_da_vaga()

class Vaga:
    def __init__(self, id, tipo) -> None:
        self.id = id
        self.tipo = tipo
        self.livre = True
        self.placa = 0

    def ocupar(self, placa):
        self.livre = False
        self.placa = placa

    def desocupar(self):
        self.livre = True
        self.placa = 0        

class Estacionamento():
    def __init__(self, total_vagas_de_carro, total_vagas_de_moto) -> None:
        self.total_vagas_de_carro = total_vagas_de_carro
        self.total_vagas_de_moto = total_vagas_de_moto
        self.carro_para_vaga = {}
        self.moto_para_vaga = {}
        self.carros_estacionados = []
        self.motos_estacionadas = []
        self.total_vagas_livres_carro = self.total_vagas_de_carro
        self.total_vagas_livres_moto = self.total_vagas_de_moto  

    def inicializar_vagas(self):
        inicio_vagas_de_moto = self.total_vagas_de_carro + 1
        self.vagas_de_carro = [Vaga(id=f"{n}", tipo="carro") for n in range(1, self.total_vagas_de_carro + 1)]
        self.vagas_de_moto = [Vaga(id=f"{n}", tipo="moto") for n in range(inicio_vagas_de_moto, self.total_vagas_de_moto + inicio_vagas_de_moto)]

    def encontrar_vaga_livre(self, tipo):
        vagas_livres_moto = [vaga for vaga in self.vagas_de_moto if vaga.livre == True]
        vagas_livres_carro = [vaga for vaga in self.vagas_de_carro if vaga.livre == True]
        if tipo == "moto":
            vagas_livres = vagas_livres_moto+vagas_livres_carro
            return vagas_livres[0] if vagas_livres else None
        return vagas_livres_carro[0] if vagas_livres_carro else None

    def estacionar(self, veiculo):
        vaga = self.encontrar_vaga_livre(veiculo.tipo)
        if vaga:
            if veiculo.tipo == "carro":
                return self.estacionar_carro(veiculo, vaga)
            else:
                return self.estacionar_moto(veiculo, vaga)
        else:
            return "Sem vagas disponíveis, tente novamente mais tarde."

    def estacionar_carro(self, carro, vaga):
        vaga.ocupar(carro.placa)
        self.carro_para_vaga[carro.placa] = vaga.id
        self.carros_estacionados.append(carro)
        carro.estacionar()
        self.total_vagas_livres_carro -= 1
        return f"Carro de placa {carro.placa} estacionado na vaga {vaga.id}"

    def estacionar_moto(self, moto, vaga):
        vaga.ocupar(moto.placa)
        self.moto_para_vaga[moto.placa] = vaga.id
        self.motos_estacionadas.append(moto)
        moto.estacionar()
        self.total_vagas_livres_moto -= 1
        return f"Moto de placa {moto.placa} estacionada na vaga {vaga.id}"        
   
    def encontrar_veiculo(self, placa):
        if placa not in self.moto_para_vaga and placa not in self.carro_para_vaga:
            return None
        if placa in self.moto_para_vaga:
            id_vaga_atual = self.moto_para_vaga[placa]
            if int(id_vaga_atual) > self.total_vagas_de_carro:
                vaga = filter(lambda vaga: vaga.id == id_vaga_atual, self.vagas_de_moto)
                return next(vaga)
        vaga = filter(lambda vaga: vaga.placa == placa, self.vagas_de_carro)
        return next(vaga)

    def remover_veiculo(self, placa):
        vaga_atual = self.encontrar_veiculo(placa)
        if vaga_atual:
            if placa in self.moto_para_vaga:
                return self.remover_moto(vaga_atual)
            return self.remover_carro(vaga_atual)
        return "Veículo não encontrado"
        
    def remover_carro(self, vaga):
        carro = next(filter(lambda veiculo: veiculo.placa == vaga.placa, self.carros_estacionados))
        carro.sair_da_vaga()
        self.carro_para_vaga.pop(carro.placa)
        self.carros_estacionados.remove(carro)     
        vaga.desocupar()
        self.total_vagas_livres_carro += 1
        return f"Carro removido, vaga {vaga.id} livre."
        
    def remover_moto(self, vaga):
        moto = next(filter(lambda veiculo: veiculo.placa == vaga.placa, self.motos_estacionadas))
        self.moto_para_vaga.pop(moto.placa)
        self.motos_estacionadas.remove(moto)    
        vaga.desocupar()
        moto.sair_da_vaga()
        if vaga.tipo == "moto":
            self.total_vagas_livres_moto += 1
        else:
            self.total_vagas_livres_carro += 1
        return f"Moto removida, vaga {vaga.id} livre."
        
    def estado_do_estacionamento(self):
        return f"Vagas livres - Carro ou moto: {self.total_vagas_livres_carro} / Exclusivo moto: {self.total_vagas_livres_moto}"
    
programa_continua = True
estacionamento = Estacionamento(VAGAS_PARA_CARRO, VAGAS_PARA_MOTO)
estacionamento.inicializar_vagas()

def menu():
    print('''888888 .dP"Y8 888888    db     dP""b8 88  dP"Yb  88b 88    db    8b    d8 888888 88b 88 888888  dP"Yb  
88__   `Ybo."   88     dPYb   dP   `" 88 dP   Yb 88Yb88   dPYb   88b  d88 88__   88Yb88   88   dP   Yb 
88""   o.`Y8b   88    dP__Yb  Yb      88 Yb   dP 88 Y88  dP__Yb  88YbdP88 88""   88 Y88   88   Yb   dP 
888888 8bodP'   88   dP""""Yb  YboodP 88  YbodP  88  Y8 dP""""Yb 88 YY 88 888888 88  Y8   88    YbodP  \n'''                                                                                                                              
    )
    print("Bem vindo ao controle de estacionamento. \n")
    print("1. Estacionar novo veículo")
    print("2. Encontrar veículo estacionado")
    print("3. Remover veículo")
    print("4. Status do estacionamento")
    print("5. Encerrar programa")
    return input("Selecione opção (1-5): ")

def filtrar_opcao(escolha):
    global programa_continua
    try:
        user_input = int(escolha)
    except ValueError:
        print("Opção inválida. Tente novamente. \n")
        return
    if user_input not in range(1, 6):
        print("Opção inválida. Tente novamente. \n")
        return
    if user_input == 5:
        programa_continua = False

    if user_input == 1:
        print(novo_veiculo())
    if user_input == 2:
        placa = input("Insira placa do veículo: ")
        vaga = estacionamento.encontrar_veiculo(placa)
        if vaga:
            print(f"O veículo está na vaga {vaga.id}")
        else:
            print(f"Veículo não encontrado.")

    if user_input == 3:
        placa = input("Placa do veículo: ")
        print(estacionamento.remover_veiculo(placa))
        
    if user_input == 4:
        print(estacionamento.estado_do_estacionamento())
        
def novo_veiculo():
    novo_veiculo_placa = input("Insira placa do veículo: ")
    novo_veiculo_tipo = input("Tipo do veículo (carro / moto): ")
    if novo_veiculo_tipo.lower() == "carro":
        novo_veiculo = Carro(novo_veiculo_placa)
        return estacionamento.estacionar(novo_veiculo)
    elif novo_veiculo_tipo.lower() == "moto":
        novo_veiculo = Moto(novo_veiculo_placa)
        return estacionamento.estacionar(novo_veiculo)   
    return "Veículo inválido, tente novamente"

while programa_continua:
    os.system("cls")
    escolha = menu()
    filtrar_opcao(escolha)
    print("\n----------------------------------------------------------------------\n")
    input("Pressione qualquer tecla para continuar.")
       
print("\n----------------------------------------------------------------------\n")
print("Encerrando controle de estacionamento. \n")
