from datetime import datetime, timedelta

from newConexao import Conexao
from Classes.Cliente import Cliente
from Classes.Carro import Carro
from Classes.Locacao import Locacao
from ControllerClasses.ControllerCliente import ControllerCliente
from ControllerClasses.ControllerCarro import ControllerCarro
from ControllerClasses.ControllerLocacao import ControllerLocacao
from Relatorios import Relatorios


def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"[!] Informe um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("[!] Digite um número inteiro válido.")


def ler_valor(mensagem, minimo=0.01):
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if valor < minimo:
                print(f"[!] Informe um valor maior ou igual a {minimo:.2f}.")
                continue
            return valor
        except ValueError:
            print("[!] Digite um valor numérico válido (ex.: 120,00).")


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("[!] Este campo é obrigatório.")


def ler_data(mensagem):
    while True:
        entrada = input(mensagem).strip()
        try:
            return datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("[!] Data inválida. Use o formato DD/MM/AAAA.")


def exibir_splash_screen(ctrl_cli, ctrl_car, ctrl_loc, conexao):
    total_cli = ctrl_cli.total_registros(conexao)
    total_car = ctrl_car.total_registros(conexao)
    total_loc = ctrl_loc.total_registros(conexao)
    print("=" * 65)
    print("         SISTEMA DE LOCAÇÃO DE VEÍCULOS")
    print(" Disciplina: Banco de Dados | Semestre: 2026/2")
    print(" Professor: Howard Roatti")
    print("-" * 65)
    print(f" Clientes cadastrados: {total_cli}")
    print(f" Carros cadastrados:   {total_car}")
    print(f" Locações registradas: {total_loc}")
    print("=" * 65)


def obter_valor_diaria(conexao, placa):
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT VALOR_DIARIA FROM CARROS WHERE PLACA = :1",
            (placa,),
        )
        resultado = cursor.fetchone()
        return float(resultado[0]) if resultado else None
    finally:
        cursor.close()


def menu_relatorios(relatorios):
    while True:
        print("\n--- RELATÓRIOS ---\n1. Locações detalhadas\n2. Faturamento por modelo\n3. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            relatorios.relatorio_locacoes_detalhadas()
        elif opcao == "2":
            relatorios.relatorio_faturamento_por_modelo()
        elif opcao == "3":
            return
        else:
            print("[!] Opção inválida.")


def menu_inserir(conexao, ctrl_cli, ctrl_car, ctrl_loc):
    while True:
        print("\n--- INSERIR ---\n1. Cliente\n2. Carro\n3. Locação\n4. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cliente = Cliente(
                cpf=ler_texto("CPF (11 números): "),
                nome=ler_texto("Nome: "),
                telefone=input("Telefone (opcional): ").strip(),
            )
            ctrl_cli.inserir(conexao, cliente)
        elif opcao == "2":
            carro = Carro(
                placa=ler_texto("Placa: ").upper(),
                modelo=ler_texto("Modelo: "),
                marca=ler_texto("Marca: "),
                valor_diaria=ler_valor("Valor da diária (R$): "),
            )
            ctrl_car.inserir(conexao, carro)
        elif opcao == "3":
            ctrl_cli.listar(conexao)
            cpf = ler_texto("CPF do cliente: ")
            if not ctrl_cli.cliente_existe(conexao, cpf):
                print("[!] Cliente não encontrado.")
                continue
            ctrl_car.listar(conexao)
            placa = ler_texto("Placa do carro: ").upper()
            diaria = obter_valor_diaria(conexao, placa)
            if diaria is None:
                print("[!] Carro não encontrado.")
                continue
            data_inicio = ler_data("Data de início (DD/MM/AAAA): ")
            dias = ler_inteiro("Quantidade de dias: ", 1)
            data_previsao = data_inicio + timedelta(days=dias)
            print(f"Data prevista para devolução: {data_previsao.strftime('%d/%m/%Y')}")
            locacao = Locacao(
                cliente=Cliente(cpf=cpf),
                carro=Carro(placa=placa),
                data_inicio=data_inicio,
                data_previsao=data_previsao,
                dias=dias,
                valor_total=diaria * dias,
            )
            ctrl_loc.inserir(conexao, locacao)
        elif opcao == "4":
            return
        else:
            print("[!] Opção inválida.")


def menu_remover(conexao, ctrl_cli, ctrl_car, ctrl_loc):
    while True:
        print("\n--- REMOVER ---\n1. Cliente\n2. Carro\n3. Locação\n4. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            ctrl_cli.listar(conexao)
            ctrl_cli.remover(conexao, ler_texto("CPF do cliente: "))
        elif opcao == "2":
            ctrl_car.listar(conexao)
            ctrl_car.remover(conexao, ler_texto("Placa do carro: ").upper())
        elif opcao == "3":
            ctrl_loc.listar(conexao)
            ctrl_loc.remover(conexao, ler_inteiro("Código da locação: ", 1))
        elif opcao == "4":
            return
        else:
            print("[!] Opção inválida.")


def menu_atualizar(conexao, ctrl_cli, ctrl_car, ctrl_loc):
    while True:
        print(
            "\n--- ATUALIZAR ---\n"
            "1. Cliente\n2. Carro\n3. Locação\n4. Registrar devolução\n5. Voltar"
        )
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            ctrl_cli.listar(conexao)
            cpf_atual = ler_texto("CPF atual do cliente: ")
            if not ctrl_cli.cliente_existe(conexao, cpf_atual):
                print("[!] Cliente não encontrado.")
                continue
            ctrl_cli.atualizar(
                conexao,
                cpf_atual,
                Cliente(
                    cpf=ler_texto("Novo CPF (11 números): "),
                    nome=ler_texto("Novo nome: "),
                    telefone=input("Novo telefone (opcional): ").strip(),
                ),
            )
        elif opcao == "2":
            ctrl_car.listar(conexao)
            placa_atual = ler_texto("Placa atual do carro: ").upper()
            if not ctrl_car.carro_existe(conexao, placa_atual):
                print("[!] Carro não encontrado.")
                continue
            ctrl_car.atualizar(
                conexao,
                placa_atual,
                Carro(
                    placa=ler_texto("Nova placa: ").upper(),
                    modelo=ler_texto("Novo modelo: "),
                    marca=ler_texto("Nova marca: "),
                    valor_diaria=ler_valor("Novo valor da diária (R$): "),
                ),
            )
        elif opcao == "3":
            ctrl_loc.listar(conexao)
            codigo = ler_inteiro("Código da locação: ", 1)
            if not ctrl_loc.locacao_existe(conexao, codigo):
                print("[!] Locação não encontrada.")
                continue
            ctrl_cli.listar(conexao)
            cpf = ler_texto("CPF do cliente: ")
            if not ctrl_cli.cliente_existe(conexao, cpf):
                print("[!] Cliente não encontrado.")
                continue
            ctrl_car.listar(conexao)
            placa = ler_texto("Placa do carro: ").upper()
            diaria = obter_valor_diaria(conexao, placa)
            if diaria is None:
                print("[!] Carro não encontrado.")
                continue
            data_inicio = ler_data("Nova data de início (DD/MM/AAAA): ")
            dias = ler_inteiro("Nova quantidade de dias: ", 1)
            data_previsao = data_inicio + timedelta(days=dias)
            ctrl_loc.atualizar(
                conexao,
                Locacao(
                    codigo_locacao=codigo,
                    cliente=Cliente(cpf=cpf),
                    carro=Carro(placa=placa),
                    data_inicio=data_inicio,
                    data_previsao=data_previsao,
                    dias=dias,
                    valor_total=diaria * dias,
                ),
            )
        elif opcao == "4":
            ctrl_loc.listar(conexao)
            codigo = ler_inteiro("Código da locação devolvida: ", 1)
            data_fim = ler_data("Data efetiva da devolução (DD/MM/AAAA): ")
            ctrl_loc.registrar_devolucao(conexao, codigo, data_fim)
        elif opcao == "5":
            return
        else:
            print("[!] Opção inválida.")


def main():
    db = Conexao(
        host="localhost",
        porta=1521,
        servico="XEPDB1",
    )
    conexao = db.conectar()
    if not conexao:
        print("\n[!] Não foi possível conectar ao banco de dados.")
        return

    try:
        ctrl_cli = ControllerCliente()
        ctrl_car = ControllerCarro()
        ctrl_loc = ControllerLocacao()
        relatorios = Relatorios(conexao)
        exibir_splash_screen(ctrl_cli, ctrl_car, ctrl_loc, conexao)

        while True:
            print(
                "\n================ MENU PRINCIPAL ================\n"
                "1. Relatórios\n2. Inserir registros\n3. Remover registros\n"
                "4. Atualizar registros\n5. Sair\n"
                "================================================"
            )
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                menu_relatorios(relatorios)
            elif opcao == "2":
                menu_inserir(conexao, ctrl_cli, ctrl_car, ctrl_loc)
            elif opcao == "3":
                menu_remover(conexao, ctrl_cli, ctrl_car, ctrl_loc)
            elif opcao == "4":
                menu_atualizar(conexao, ctrl_cli, ctrl_car, ctrl_loc)
            elif opcao == "5":
                print("\nAté logo!")
                break
            else:
                print("[!] Opção inválida.")
    except Exception as erro:
        print(f"\n[!] Ocorreu um erro inesperado: {erro}")
    finally:
        db.desconectar()


if __name__ == "__main__":
    main()
