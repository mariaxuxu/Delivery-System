from .models import Product

class Menu:
    _items = [
        # pizzas
        Product("Pizza Calabresa", 45.00),
        Product("Pizza Calabresa Especial", 52.00),
        Product("Pizza 4 Queijos", 48.00),
        Product("Pizza Margherita", 44.00),
        Product("Pizza Portuguesa", 50.00),
        Product("Pizza Frango com Catupiry", 49.00),

        # lanches
        Product("X-Burger da Casa", 22.50),
        Product("X-Salada", 18.00),
        Product("X-Bacon", 24.00),
        Product("X-Tudo", 28.00),

        # bebidas
        Product("Coca-Cola 2L", 12.00),
        Product("Coca-Cola Lata", 6.00),
        Product("Suco de Laranja", 8.00),
        Product("Guaraná Antarctica 1L", 9.00),

        # sobremesas
        Product("Pudim de Leite", 10.00),
        Product("Mousse de Maracujá", 9.00),
        Product("Brownie com Sorvete", 16.00)
    ]

    @classmethod
    def get_items(cls):
        return cls._items

    @classmethod
    def get_product(cls, index):
        if 0 <= index < len(cls._items):
            return cls._items[index]
        return None