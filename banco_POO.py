from abc import ABC, abstractmethod
from datetime import date, datetime


class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    @property
    def transacoes(self):
        return self._transacoes


class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, cliente, numero, agencia):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            return False
        self._saldo += valor
        return True

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento


# Criando um cliente
cliente1 = PessoaFisica("João", "123.456.789-00", date(1990, 5, 15), "Rua das Flores, 123")

# Criando uma conta
conta1 = Conta.nova_conta(cliente1, 1001, "001")
cliente1.adicionar_conta(conta1)

# Realizando transações
cliente1.realizar_transacao(conta1, Deposito(500))
cliente1.realizar_transacao(conta1, Saque(200))

# Exibindo saldo e histórico
print(f"Saldo atual: R$ {conta1.saldo:.2f}")
print("Histórico de transações:", conta1.historico.transacoes)
