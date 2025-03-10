from datetime import datetime

def menu () -> str:
    return input("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            MENU BANCARIO
        
        [d]\t Depositar
        [s]\t Sacar
        [e]\t Extrato
        [nu]\t Novo usuario
        [nc]\t Nova conta
        [q] - Sair      
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

=> """)


def depositar(valor: float, saldo: float, extrato: str) -> tuple[float, str]:
    if valor > 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saldo += valor
        extrato += f"{timestamp} | Depósito: R$ {valor:.2f}\n"
        return saldo, extrato
    else:
        print("Operação inválida. Valor de depósito deve ser maior que zero.")
        return saldo, extrato


def mostrar_extrato(extrato: str) -> None:
    print("EXTRATO".center(24, "="), end='\n\n')
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print(f"Limite de saque: R$ {limite:.2f}")
    print(f"Limite de saques: {LIMITE_SAQUES}")
    print(f"Total de saques: {saques}")
    print("=" * 24)


def sacar(valor: float, saldo: float, limite: float, extrato: str, num_saques: int, *,  limite_saques: int) -> tuple[float, str, int]:
    if valor <= 0:
        print("Operação inválida. O valor do saque deve ser maior que zero.")
    elif valor > saldo:
        print("Operação inválida. Saldo insuficiente.")
    elif valor > limite:
        print("Operação inválida. O valor excede o limite de saque.")
    elif num_saques >= limite_saques:
        print("Operação inválida. Limite de saques diários atingido.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} | Saque: R$ {valor:.2f}\n"
        num_saques += 1
        return saldo, extrato, num_saques
    
    return saldo, extrato, num_saques


def criar_usuario(usuarios: list[dict]) -> None:
    cpf = input("\nInforme apenas os números do CPF:")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("CPF já cadastrado. Tente novamente.")
        return
    nome = input("\nInforme o nome do usuário:")
    data_nasc = input("\nInforme a data de nascimento do usuário:")
    telefone = input("\nInforme o telefone do usuário:")
    endereco = input("\nInforme o endereco do usuário:")
    usuarios.append({
        "cpf": cpf,
        "nome": nome,
        "data_nasc": data_nasc,
        "telefone": telefone,
        "endereco": endereco
    })

    print(" Usuário cadastrado com sucesso ".center(80, "="))
    

def filtrar_usuario(cpf: str, usuarios: list[dict]) -> dict[str: str]:
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta(agencia: str, num_conta: int, contas: list[dict], usuarios: list[dict]) -> None:
    cpf = input("\nInforme apenas os números do CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        contas.append({
            "agencia": agencia,
            "num_conta": num_conta,
            "saldo": 0.0,
            "usuario": usuario
        })
        print("\nConta criada com sucesso.")
        return
    
    print("\nUsuário não encontrado")
    

saldo, saques, limite = 0.0, 0, 500
extrato = ""

LIMITE_SAQUES = 3
AGENCIA = "0001"

usuarios = []
contas = []

while True:
    op = menu().lower();
    print()

    if op == "d":
        print("DEPÓSITO".center(24, "="), end='\n\n')
        valor = float(input("Valor do depósito: R$ "))
        saldo, extrato = depositar(valor, saldo, extrato)
    elif op == "s":
        print("SAQUE".center(24, "="), end='\n\n')
        valor = float(input("Valor do saque: R$ "))
        saldo, extrato, saques = sacar(valor, saldo, limite, extrato, saques, limite_saques=LIMITE_SAQUES)
    elif op == "e":
        mostrar_extrato(extrato)
    elif op == "nu":
        criar_usuario(usuarios)
    elif op == "nc":
        num_conta = max(contas["num_conta"]) + 1
        criar_conta(AGENCIA, num_conta, contas, usuarios)
    elif op == "q":
        print("\nSaindo..")
        break
    else:
        print("Opção Inválida!")
    
