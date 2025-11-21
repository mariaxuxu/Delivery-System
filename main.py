import time
import os
from src.builders import OrderBuilder
from src.database import Database
from src.observers import CustomerEmailNotifier, RestaurantAppNotifier
from src.menu import Menu

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Digite um número válido.")

def ler_bool(mensagem):
    while True:
        resp = input(mensagem).lower().strip()
        if resp in ['s', 'sim', 'y', 'yes']: return True
        if resp in ['n', 'nao', 'não', 'no']: return False

def exibir_menu():
    print("\n--- 📜 CARDÁPIO DO DIA ---")
    items = Menu.get_items()
    for i, item in enumerate(items):
        print(f"[{i+1}] {item.name:<20} R$ {item.price:.2f}")
    print("-" * 30)

def main():
    limpar_tela()
    print("="*50)
    print("PIZZARIA DOS HENRIQUE'S BENITEZ")
    print("="*50)

    nome = input("Seu nome: ")
    endereco = input("Seu endereço: ")
    is_vip = ler_bool("Você é VIP?: ")

    builder = OrderBuilder(nome, endereco, is_vip=is_vip)

    email = input("E-mail para status: ")
    builder.add_observer(CustomerEmailNotifier(email))
    builder.add_observer(RestaurantAppNotifier())

    print(f"\n✅ Bem-vindo(a), {nome}!")

    while True:
        print("\n" + "="*30)
        print("SEU CARRINHO:")
        if not builder.order.items:
            print("   (Vazio)")
        else:
            for i, item in enumerate(builder.order.items, 1):
                print(f"   {i}. {item.name} - R$ {item.price:.2f}")
        print("="*30)

        print("\nO que deseja fazer?")
        print("[1] Ver Cardápio e Adicionar Item")
        print("[2] Adicionar Bacon Extra no último item (+ R$ 5,00)")
        print("[3] Embrulhar p/ Presente o último item (+ R$ 12,00)")
        print("[4] Finalizar Pedido")
        print("[0] Cancelar")

        opcao = input("👉 Opção: ")

        if opcao == '1':
            exibir_menu()
            try:
                escolha = int(input("Digite o número do produto: "))
                produto = Menu.get_product(escolha - 1)
                if produto:
                    builder.add_product(produto)
                    print(f"✅ {produto.name} adicionado!")
                else:
                    print("Produto inválido.")
            except ValueError:
                print("Digite um número.")

        elif opcao == '2':
            if not builder.order.items:
                print("Carrinho vazio!")
            else:
                builder.with_extra_bacon()
                print("✅ Bacon adicionado!")

        elif opcao == '3':
            if not builder.order.items:
                print("Carrinho vazio!")
            else:
                builder.with_gift_wrap()
                print("✅ Embalagem adicionada!")

        elif opcao == '4':
            if not builder.order.items:
                print("❌ Carrinho vazio!")
            else:
                break

        elif opcao == '0':
            print("👋 Tchau!")
            return

    # Checkout
    limpar_tela()
    distancia = ler_float("Distância da entrega (km): ")

    pedido = builder.build()
    total = pedido.get_total(distancia)

    print("\n" + "*"*40)
    print("🧾 RESUMO DO PEDIDO")
    print("*"*40)
    print(f"Cliente: {pedido.client.name}")
    print(f"Endereço: {pedido.client.address}")
    print(f"Itens: {[i.name for i in pedido.items]}")
    print(f"TOTAL A PAGAR: R$ {total:.2f}")

    if ler_bool("\nConfirmar pedido?: "):
        print("\nProcessando...")
        estados = 3
        for _ in range(estados):
            time.sleep(1.5)
            pedido.advance()

        print("\n✅ Obrigado! Seu pedido foi salvo.")
    else:
        print("Pedido descartado.")

if __name__ == "__main__":
    main()