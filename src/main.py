from Conexao import Conexao
from Classes.Cliente import Cliente
from Classes.Carro import Carro
from Classes.Locacao import Locacao
from ControllerClasses.ControllerCliente import ControllerCliente
from ControllerClasses.ControllerCarro import ControllerCarro
from ControllerClasses.ControllerLocacao import ControllerLocacao
from Relatorios import Relatorios

def exibir_splash_screen(ctrl_cli, ctrl_car, ctrl_loc, conexao):
    # Obtém a contagem de registos de cada tabela
    total_cli = ctrl_cli.total_registros(conexao)
    total_car = ctrl_car.total_registros(conexao)
    total_loc = ctrl_loc.total_registros(conexao)
    
    print("=" * 65)
    print("         SISTEMA DE LOCAÇÃO DE VEÍCULOS")
    print(" Disciplina: Banco de Dados | Semestre: 2026/2")
    print(" Professor: Howard Roatti")
    print(" Componentes do Grupo: Lucas de Souza Barboza e Grupo")
    print("-" * 65)
    print(f" -> Total de Clientes cadastrados: {total_cli}")
    print(f" -> Total de Carros cadastrados:   {total_car}")
    print(f" -> Total de Locações registradas: {total_loc}")
    print("=" * 65)

def main():
    # Inicializa a conexão com a base de dados
    db = Conexao(database="locadora_veiculos", user="root", password="")
    conexao = db.conectar()
    
    if not conexao:
        print("\n[!] Erro crítico: Não foi possível conectar ao banco de dados.")
        return

    # Instancia TODAS as controladoras necessárias
    ctrl_cli = ControllerCliente()
    ctrl_car = ControllerCarro()
    ctrl_loc = ControllerLocacao()
    relatorios = Relatorios(conexao)

    # Exibe a Splash Screen ao iniciar
    exibir_splash_screen(ctrl_cli, ctrl_car, ctrl_loc, conexao)

    # Loop principal do menu
    while True:
        print("\n=================== MENU PRINCIPAL ===================")
        print("1. Relatórios")
        print("2. Inserir Registros")
        print("3. Remover Registros")
        print("4. Atualizar Registros")
        print("5. Sair")
        print("======================================================")
        
        opcao = input("Escolha uma opção: ")

        # 1. RELATÓRIOS
        if opcao == "1":
            while True:
                print("\n--- SUBMENU RELATÓRIOS ---")
                print("1. Relatório Detalhado de Locações (JOIN)")
                print("2. Faturamento por Modelo de Carro (GROUP BY)")
                print("3. Voltar ao Menu Principal")
                op_rel = input("Escolha uma opção: ")
                
                if op_rel == "1":
                    relatorios.relatorio_locacoes_detalhadas()
                elif op_rel == "2":
                    relatorios.relatorio_faturamento_por_modelo()
                elif op_rel == "3":
                    break
                else:
                    print("\n[!] Opção inválida!")

        # 2. INSERIR REGISTROS
        elif opcao == "2":
            while True:
                print("\n--- SUBMENU INSERIR ---")
                print("1. Inserir Cliente")
                print("2. Inserir Carro")
                print("3. Inserir Locação")
                print("4. Voltar ao Menu Principal")
                op_ins = input("Escolha a entidade: ")

                if op_ins == "1":
                    nome = input("Nome do Cliente: ")
                    cpf = input("CPF do Cliente: ")
                    telefone = input("Telefone do Cliente: ")
                    cli = Cliente(nome=nome, cpf=cpf, telefone=telefone)
                    ctrl_cli.inserir(conexao, cli)
                elif op_ins == "2":
                    modelo = input("Modelo do Carro: ")
                    marca = input("Marca do Carro: ")
                    placa = input("Placa do Carro: ")
                    diaria = float(input("Valor da Diária (ex: 120.00): "))
                    car = Carro(modelo=modelo, marca=marca, placa=placa, valor_diaria=diaria)
                    ctrl_car.inserir(conexao, car)
                elif op_ins == "3":
                    print("\nSelecione o Cliente e o Carro para a locação:")
                    ctrl_cli.listar(conexao)
                    id_cliente = int(input("\nInforme o ID do Cliente: "))
                    
                    ctrl_car.listar(conexao)
                    id_carro = int(input("\nInforme o ID do Carro: "))
                    
                    data = input("Data da Locação (DD/MM/AAAA): ")
                    dias = int(input("Quantidade de dias: "))
                    
                    cursor = conexao.cursor()
                    cursor.execute("SELECT valor_diaria FROM carro WHERE id_carro = " + str(id_carro))
                    res_diaria = cursor.fetchone()
                    cursor.close()
                    
                    if res_diaria:
                        valor_diaria = float(res_diaria[0])
                        valor_total = valor_diaria * dias
                        
                        cli_obj = Cliente(id_cliente=id_cliente)
                        car_obj = Carro(id_carro=id_carro)
                        loc = Locacao(cliente=cli_obj, carro=car_obj, data_locacao=data, dias=dias, valor_total=valor_total)
                        ctrl_loc.inserir(conexao, loc)
                    else:
                        print("\n[!] Carro não encontrado.")
                elif op_ins == "4":
                    break
                else:
                    print("\n[!] Opção inválida!")

        # 3. REMOVER REGISTROS
        elif opcao == "3":
            while True:
                print("\n--- SUBMENU REMOVER ---")
                print("1. Remover Cliente")
                print("2. Remover Carro")
                print("3. Remover Locação")
                print("4. Voltar ao Menu Principal")
                op_rem = input("Escolha a entidade: ")

                if op_rem == "1":
                    ctrl_cli.listar(conexao)
                    id_cli = int(input("\nInforme o ID do cliente que deseja remover: "))
                    ctrl_cli.remover(conexao, id_cli)
                elif op_rem == "2":
                    ctrl_car.listar(conexao)
                    id_car = int(input("\nInforme o ID do carro que deseja remover: "))
                    ctrl_car.remover(conexao, id_car)
                elif op_rem == "3":
                    ctrl_loc.listar(conexao)
                    id_loc = int(input("\nInforme o ID da locação que deseja remover: "))
                    ctrl_loc.remover(conexao, id_loc)
                elif op_rem == "4":
                    break
                else:
                    print("\n[!] Opção inválida!")

        # 4. ATUALIZAR REGISTROS
        elif opcao == "4":
            while True:
                print("\n--- SUBMENU ATUALIZAR ---")
                print("1. Atualizar Cliente")
                print("2. Atualizar Carro")
                print("3. Atualizar Locação")
                print("4. Voltar ao Menu Principal")
                op_atv = input("Escolha a entidade: ")

                if op_atv == "1":
                    ctrl_cli.listar(conexao)
                    id_cli = int(input("\nInforme o ID do cliente que deseja atualizar: "))
                    if ctrl_cli.cliente_existe(conexao, id_cli):
                        nome = input("Novo Nome: ")
                        cpf = input("Novo CPF: ")
                        telefone = input("Novo Telefone: ")
                        cli = Cliente(id_cliente=id_cli, nome=nome, cpf=cpf, telefone=telefone)
                        ctrl_cli.atualizar(conexao, cli)
                    else:
                        print("\n[!] Cliente não encontrado.")
                elif op_atv == "2":
                    ctrl_car.listar(conexao)
                    id_car = int(input("\nInforme o ID do carro que deseja atualizar: "))
                    if ctrl_car.carro_existe(conexao, id_car):
                        modelo = input("Novo Modelo: ")
                        marca = input("Nova Marca: ")
                        placa = input("Nova Placa: ")
                        diaria = float(input("Novo Valor da Diária: "))
                        car = Carro(id_carro=id_car, modelo=modelo, marca=marca, placa=placa, valor_diaria=diaria)
                        ctrl_car.atualizar(conexao, car)
                    else:
                        print("\n[!] Carro não encontrado.")
                elif op_atv == "3":
                    ctrl_loc.listar(conexao)
                    id_loc = int(input("\nInforme o ID da locação que deseja atualizar: "))
                    if ctrl_loc.locacao_existe(conexao, id_loc):
                        ctrl_cli.listar(conexao)
                        id_cliente = int(input("\nNovo ID do Cliente: "))
                        ctrl_car.listar(conexao)
                        id_carro = int(input("\nNovo ID do Carro: "))
                        data = input("Nova Data (DD/MM/AAAA): ")
                        dias = int(input("Nova Quantidade de Dias: "))
                        
                        cursor = conexao.cursor()
                        cursor.execute("SELECT valor_diaria FROM carro WHERE id_carro = " + str(id_carro))
                        res_diaria = cursor.fetchone()
                        cursor.close()
                        
                        if res_diaria:
                            valor_total = float(res_diaria[0]) * dias
                            cli_obj = Cliente(id_cliente=id_cliente)
                            car_obj = Carro(id_carro=id_carro)
                            loc = Locacao(id_locacao=id_loc, cliente=cli_obj, carro=car_obj, data_locacao=data, dias=dias, valor_total=valor_total)
                            ctrl_loc.atualizar(conexao, loc)
                        else:
                            print("\n[!] Carro selecionado não existe.")
                    else:
                        print("\n[!] Locação não encontrada.")
                elif op_atv == "4":
                    break
                else:
                    print("\n[!] Opção inválida!")