class Cliente:
    def __init__(self, nome, telefone, genero, renda):
        self._id = 10
        self._nome = nome
        self._telefone = telefone
        self._genero = genero
        self.__renda_mensal = renda
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value       
        return self._id

    @property
    def nome(self):
        return self._nome
    
    @property
    def telefone(self):
        return self._telefone
    
    @property
    def genero(self):
        return self._genero

    @property
    def renda_mensal(self):
        return self.__renda_mensal

class Conta(Cliente):
    def __init__(self, titular: Cliente, numero):
        self.numero = numero
        self._titulares = [titular]
        self.__saldo = 0
        self.conta_mulher = False
        self.__cheque_especial = 0

    def __str__(self) -> str:
        return f"Conta: {self.numero} - Titular(es): {[titular.nome for titular in self.titulares]} - Saldo: R${self.saldo} - Cheque especial: R${self.cheque_especial}"

    @property
    def titulares(self):
        return self._titulares
  
    @property
    def saldo(self):
        return self.__saldo
    
    @saldo.setter
    def saldo(self, valor):
        self.__saldo = valor

    @property
    def cheque_especial(self):
        # Ativa apenas na presença de um titular mulher
        # Média da renda de todos os titulares.
        return self.__cheque_especial
    
    @cheque_especial.setter
    def cheque_especial(self, valor):
        if self.conta_mulher == True:
            self.__cheque_especial = valor

    def adicionar_titular(self, novo_titular: Cliente):
        if novo_titular.genero == "f":
            self.conta_mulher = True
            self.cheque_especial += novo_titular.renda_mensal
        self._titulares.append(novo_titular)

    def saque(self, valor):
        if self.saldo + self.cheque_especial >= valor:
            novo_saldo = self.saldo - valor
            self.saldo = novo_saldo
            return f"Saque no valor de R${valor} concluído, novo saldo: R${novo_saldo}"
        return "Saldo insuficiente."

    def deposito(self, valor):
        novo_saldo = self.saldo + valor
        self.saldo = novo_saldo
        return f"Depósito no valor de R${valor} concluído. Novo saldo: R${novo_saldo}"

    def consultar_saldo(self):
        cheque_especial = ""
        if self.conta_mulher:
            cheque_especial = f"Total cheque especial: R${self.cheque_especial}"
        return f"Saldo atual: R${self.saldo} {cheque_especial}"
            
class Banco():
    def __init__(self):
        self._contas_ativas = []
        self._clientes = []

    @property
    def contas_ativas(self):
        return self._contas_ativas

    @property
    def clientes(self):
        return self._clientes

    def cadastrar_cliente(self, cliente: Cliente):
        # Cadastro de novos clientes.
        cliente.id += len(self.clientes)
        self._clientes.append(cliente)
        return cliente.id

    def criar_conta(self, cliente: Cliente):
        # Cria conta com um titular inicial, podendo adicionar mais posteriormente.
        numero_conta = 1001+len(self._contas_ativas)
        nova_conta = Conta(cliente, numero_conta)
        if cliente.genero == "f":
            nova_conta.conta_mulher = True
            nova_conta.cheque_especial = cliente.renda_mensal
        self._contas_ativas.append(nova_conta)

    def editar_nome(self, cliente: Cliente, novo_nome):
        cliente._nome = novo_nome
    
    def editar_telefone(self, cliente: Cliente, novo_telefone):
        cliente._telefone = novo_telefone
    
    def editar_renda(self, cliente: Cliente, nova_renda):
        cliente.__renda_mensal = nova_renda

# Casos de teste

banco = Banco()

cliente1 = Cliente("Jessica Jones", "111222", "f", 1000)
banco.cadastrar_cliente(cliente1)
cliente2 = Cliente("Billy Butcher", "222333", "m", 1000)
banco.cadastrar_cliente(cliente2)
cliente3 = Cliente("Miriam Maisel", "333444", "f", 3000)
banco.cadastrar_cliente(cliente3)

banco.criar_conta(cliente1)
conta1 = banco.contas_ativas[0]
banco.criar_conta(cliente2)
conta2 = banco.contas_ativas[1]
banco.criar_conta(cliente3)
conta3 = banco.contas_ativas[2]

print(f"Conta {conta1.numero} - Titular(es): {[titular.nome for titular in conta1.titulares]}")
print(f"Conta {conta1.numero} - é conta mulher? {conta1.conta_mulher}")
print(f"Conta {conta1.numero} - Cheque especial: R${conta1.cheque_especial}")
print(f"Adicionando cliente {cliente2.nome} à conta {conta1.numero}")
conta1.adicionar_titular(cliente2)
print(conta1)
print("------------------------------------------")
print(conta2)
print(f"Conta {conta2.numero} - é conta mulher? {conta2.conta_mulher}")
print("------------------------------------------")
print(conta3)
print(f"Adicionando cliente {cliente1.nome} à conta {conta3.numero}")
conta3.adicionar_titular(cliente1)
print(conta3)
print(conta3.deposito(500))
print(conta3.saque(1000))
print(conta3.saque(4000))

