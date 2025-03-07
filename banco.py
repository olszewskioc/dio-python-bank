from datetime import datetime

def menu () -> str:
    return input("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            MENU BANCARIO
        
        [d] - Depositar
        [s] - Sacar
        [e] - Extrato
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


def sacar(valor: float, saldo: float, limite: float, extrato: str, num_saques: int, limite_saques: int) -> tuple[float, str, int]:
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





saldo, saques, limite = 0.0, 0, 500
extrato = ""

LIMITE_SAQUES = 3

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
        saldo, extrato, saques = sacar(valor, saldo, limite, extrato, saques, LIMITE_SAQUES)
    elif op == "e":
        print("EXTRATO".center(24, "="), end='\n\n')
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(f"Limite de saque: R$ {limite:.2f}")
        print(f"Limite de saques: {LIMITE_SAQUES}")
        print(f"Total de saques: {saques}")
        print("=" * 24)
    elif op == "q":
        print("\nSaindo..")
        break
    else:
        print("Opção Inválida!")
    
