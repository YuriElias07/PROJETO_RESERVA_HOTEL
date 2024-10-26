from datetime import datetime

class Cliente:
    def __init__(self, nome, email, id_cliente):
        self.nome = nome
        self.email = email
        self.id_cliente = id_cliente

    def __str__(self):
        return f"ID: {self.id_cliente} - Cliente: {self.nome}, Email: {self.email}"


class Quarto:
    def __init__(self, numero, tipo, preco):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Reservado"
        return f"Quarto {self.numero} ({self.tipo}) - R${self.preco} - {status}"


class Reserva:
    def __init__(self, cliente, quarto, data_inicio, data_fim, id_reserva):
        self.cliente = cliente
        self.quarto = quarto
        self.data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
        self.data_fim = datetime.strptime(data_fim, '%d/%m/%Y')
        self.id_reserva = id_reserva
        self.valor_total = self.calcular_valor_total()

    def calcular_valor_total(self):
        dias = (self.data_fim - self.data_inicio).days
        return dias * self.quarto.preco

    def __str__(self):
        return (f"ID: {self.id_reserva} - Reserva de {self.cliente.nome} no quarto {self.quarto.numero} "
                f"de {self.data_inicio.strftime('%d/%m/%Y')} até {self.data_fim.strftime('%d/%m/%Y')} "
                f"- Total: R${self.valor_total:.2f}")


class GerenciadorDeReservas:
    def __init__(self):
        self.quartos = []
        self.reservas = []
        self.clientes = []
        self.contador_clientes = 1  # Contador para IDs de clientes
        self.contador_reservas = 1   # Contador para IDs de reservas

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def listar_quartos(self):
        return self.quartos

    def atualizar_quarto(self, numero, tipo=None, preco=None):
        for quarto in self.quartos:
            if quarto.numero == numero:
                if tipo:
                    quarto.tipo = tipo
                if preco:
                    quarto.preco = preco
                return quarto
        return None

    def remover_quarto(self, numero):
        self.quartos = [quarto for quarto in self.quartos if quarto.numero != numero]

    def listar_quartos_disponiveis(self):
        return [quarto for quarto in self.quartos if quarto.disponivel]

    def reservar_quarto(self, cliente, quarto_numero, data_inicio, data_fim):
        for quarto in self.quartos:
            if quarto.numero == quarto_numero and quarto.disponivel:
                reserva = Reserva(cliente, quarto, data_inicio, data_fim, self.contador_reservas)
                quarto.disponivel = False
                self.reservas.append(reserva)
                self.contador_reservas += 1  # Incrementa o contador de reservas
                return reserva
        return None

    def listar_reservas(self):
        return self.reservas

    def adicionar_cliente(self, cliente):
        cliente.id_cliente = self.contador_clientes  # Define o ID do cliente
        self.clientes.append(cliente)
        self.contador_clientes += 1  # Incrementa o contador de clientes

    def listar_clientes(self):
        return self.clientes

    def atualizar_cliente(self, nome_antigo, novo_nome=None, novo_email=None):
        for cliente in self.clientes:
            if cliente.nome == nome_antigo:
                if novo_nome:
                    cliente.nome = novo_nome
                if novo_email:
                    cliente.email = novo_email
                return cliente
        return None

    def remover_cliente(self, nome):
        self.clientes = [cliente for cliente in self.clientes if cliente.nome != nome]


# Funções auxiliares para a interface do console
def menu_principal():
    print("\n--- Sistema de Reservas de Hotel ---")
    print("1. Gerenciar Quartos")
    print("2. Gerenciar Reservas")
    print("3. Gerenciar Clientes")
    print("4. Sair")
    return input("Escolha uma opção: ")


def menu_quartos():
    print("\n--- Gerenciamento de Quartos ---")
    print("1. Listar quartos")
    print("2. Adicionar quarto")
    print("3. Atualizar quarto")
    print("4. Remover quarto")
    print("5. Voltar ao menu principal")
    return input("Escolha uma opção: ")


def menu_reservas():
    print("\n--- Gerenciamento de Reservas ---")
    print("1. Fazer uma reserva")
    print("2. Ver reservas")
    print("3. Voltar ao menu principal")
    return input("Escolha uma opção: ")


def menu_clientes():
    print("\n--- Gerenciamento de Clientes ---")
    print("1. Adicionar cliente")
    print("2. Listar clientes")
    print("3. Atualizar cliente")
    print("4. Remover cliente")
    print("5. Voltar ao menu principal")
    return input("Escolha uma opção: ")


def listar_quartos(gerenciador):
    quartos = gerenciador.listar_quartos()
    if quartos:
        print("\nQuartos:")
        for quarto in quartos:
            print(quarto)
    else:
        print("\nNenhum quarto cadastrado.")


def adicionar_quarto(gerenciador):
    numero = int(input("Número do quarto: "))
    tipo = input("Tipo do quarto: ")
    preco = float(input("Preço do quarto: "))
    quarto = Quarto(numero, tipo, preco)
    gerenciador.adicionar_quarto(quarto)
    print("\nQuarto adicionado com sucesso!")


def atualizar_quarto(gerenciador):
    numero = int(input("Número do quarto a ser atualizado: "))
    tipo = input("Novo tipo do quarto (pressione Enter para manter): ")
    preco = input("Novo preço do quarto (pressione Enter para manter): ")

    if preco:
        preco = float(preco)
    else:
        preco = None

    quarto = gerenciador.atualizar_quarto(numero, tipo if tipo else None, preco)
    if quarto:
        print("\nQuarto atualizado com sucesso!")
        print(quarto)
    else:
        print("\nQuarto não encontrado.")


def remover_quarto(gerenciador):
    numero = int(input("Número do quarto a ser removido: "))
    gerenciador.remover_quarto(numero)
    print("\nQuarto removido com sucesso!")


def fazer_reserva(gerenciador):
    nome = input("Nome do cliente: ")
    email = input("Email do cliente: ")
    cliente = Cliente(nome, email, None)  # ID será gerado ao adicionar o cliente

    try:
        quarto_numero = int(input("Número do quarto desejado: "))
        data_inicio = input("Data de início (dd/mm/yyyy): ")
        data_fim = input("Data de fim (dd/mm/yyyy): ")

        reserva = gerenciador.reservar_quarto(cliente, quarto_numero, data_inicio, data_fim)
        if reserva:
            print("\nReserva confirmada!")
            print(reserva)
        else:
            print("\nQuarto indisponível ou número de quarto inválido.")
    except ValueError:
        print("\nEntrada inválida. Tente novamente.")


def ver_reservas(gerenciador):
    reservas = gerenciador.listar_reservas()
    if reservas:
        print("\nReservas:")
        for reserva in reservas:
            print(reserva)
    else:
        print("\nNenhuma reserva encontrada.")


def adicionar_cliente(gerenciador):
    nome = input("Nome do cliente: ")
    email = input("Email do cliente: ")
    cliente = Cliente(nome, email, None)  # ID será gerado ao adicionar o cliente
    gerenciador.adicionar_cliente(cliente)
    print("\nCliente adicionado com sucesso!")


def listar_clientes(gerenciador):
    clientes = gerenciador.listar_clientes()
    if clientes:
        print("\nClientes:")
        for cliente in clientes:
            print(cliente)
    else:
        print("\nNenhum cliente cadastrado.")


def atualizar_cliente(gerenciador):
    nome_antigo = input("Nome do cliente a ser atualizado: ")
    novo_nome = input("Novo nome do cliente (pressione Enter para manter): ")
    novo_email = input("Novo email do cliente (pressione Enter para manter): ")

    cliente = gerenciador.atualizar_cliente(nome_antigo, novo_nome if novo_nome else None, novo_email if novo_email else None)
    if cliente:
        print("\nCliente atualizado com sucesso!")
        print(cliente)
    else:
        print("\nCliente não encontrado.")


def remover_cliente(gerenciador):
    nome = input("Nome do cliente a ser removido: ")
    gerenciador.remover_cliente(nome)
    print("\nCliente removido com sucesso!")


# Inicialização do sistema e loop principal
def main():
    gerenciador = GerenciadorDeReservas()
    gerenciador.adicionar_quarto(Quarto(101, "Single", 100))
    gerenciador.adicionar_quarto(Quarto(102, "Double", 150))
    gerenciador.adicionar_quarto(Quarto(103, "Suite", 540))
    gerenciador.adicionar_quarto(Quarto(104, "Suite", 240))
    gerenciador.adicionar_quarto(Quarto(105, "Double", 300))

    while True:
        opcao = menu_principal()
        if opcao == "1":
            while True:
                opcao_quarto = menu_quartos()
                if opcao_quarto == "1":
                    listar_quartos(gerenciador)
                elif opcao_quarto == "2":
                    adicionar_quarto(gerenciador)
                elif opcao_quarto == "3":
                    atualizar_quarto(gerenciador)
                elif opcao_quarto == "4":
                    remover_quarto(gerenciador)
                elif opcao_quarto == "5":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        elif opcao == "2":
            while True:
                opcao_reserva = menu_reservas()
                if opcao_reserva == "1":
                    fazer_reserva(gerenciador)
                elif opcao_reserva == "2":
                    ver_reservas(gerenciador)
                elif opcao_reserva == "3":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        elif opcao == "3":
            while True:
                opcao_cliente = menu_clientes()
                if opcao_cliente == "1":
                    adicionar_cliente(gerenciador)
                elif opcao_cliente == "2":
                    listar_clientes(gerenciador)
                elif opcao_cliente == "3":
                    atualizar_cliente(gerenciador)
                elif opcao_cliente == "4":
                    remover_cliente(gerenciador)
                elif opcao_cliente == "5":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()