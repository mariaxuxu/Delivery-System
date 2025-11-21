import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.builders import OrderBuilder
from src.database import Database
from src.strategies import VipDelivery, MotoDelivery
from src.states import CreatedState, CookingState
from src.decorators import SimpleProduct, ExtraBacon
from src.models import Product
from src.observers import OrderObserver

class TestIfoodSystem(unittest.TestCase):

    def setUp(self):
        self.db = Database()

    def test_singleton_pattern(self):
        """Teste 1: Instância única do DB"""
        db1 = Database()
        db2 = Database()
        self.assertEqual(id(db1), id(db2))

    def test_strategy_vip(self):
        """Teste 2: Estratégia VIP (90% do valor, frete 0)"""
        builder = OrderBuilder("VIP Paulo Henrique", "Rua Pereira Antonia de Souza, 122", is_vip=True)
        order = builder.add_product(Product("Item", 100.00)).build()
        total = order.get_total(50)
        self.assertEqual(total, 90.00)
        self.assertIsInstance(order.strategy, VipDelivery)

    def test_strategy_moto(self):
        """Teste 3: Estratégia Moto (Taxa + Km)"""
        builder = OrderBuilder("Normal Maria Benitez", "Rua Santa Genebra, 765", is_vip=False)
        order = builder.add_product(Product("Item", 10.00)).build()
        total = order.get_total(5.0)
        self.assertEqual(total, 20.00)

    def test_state_flow(self):
        """Teste 4: Transição de Estados"""
        order = OrderBuilder("State Maria", "Rua Santa Genebra, 765").build()
        self.assertIsInstance(order.state, CreatedState)
        order.advance()
        self.assertIsInstance(order.state, CookingState)

    def test_decorator(self):
        """Teste 5: Decorator adiciona preço e muda nome"""
        p_base = SimpleProduct(Product("Burger", 20.00))
        p_bacon = ExtraBacon(p_base)
        self.assertEqual(p_bacon.price, 25.00)
        self.assertTrue("Bacon Extra" in p_bacon.name)

    def test_observer(self):
        """Teste 6: Observer é notificado"""
        mock_obs = MagicMock(spec=OrderObserver)
        builder = OrderBuilder("Obs maria@gmail.com", "Rua Santa Genebra, 765")
        pedido = builder.add_observer(mock_obs).build()
        pedido.advance()
        mock_obs.update.assert_called()

if __name__ == '__main__':
    unittest.main()