import uuid
import time
import random
from typing import List
from .models import Client, Product
from .strategies import DeliveryStrategy, MotoDelivery, VipDelivery
from .states import CreatedState
from .database import Database
from .observers import OrderObserver
from .decorators import SimpleProduct, ExtraBacon, GiftPackage

class Order:
    def __init__(self, client: Client, strategy: DeliveryStrategy):
        self.id = str(uuid.uuid4())[:8]
        self.client = client
        self.items = []
        self.strategy = strategy
        self.state = CreatedState()
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.db = Database()
        self.observers: List[OrderObserver] = []

    def attach(self, observer: OrderObserver):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.id, self.state.get_name())

    def set_state(self, state):
        self.state = state
        self.db.log(f"Pedido {self.id}: Estado alterado para {self.state.get_name()}")
        self.notify_observers()

    def advance(self):
        self.state.next(self)

    def get_total(self, distance_km: float):
        subtotal = sum(p.price for p in self.items)
        return self.strategy.calculate_total(subtotal, distance_km)

    def save_to_db(self):
        order_dict = {
            "id": self.id,
            "client": self.client.name,
            "address": self.client.address,
            "items": [p.name for p in self.items],
            "status": self.state.get_name(),
            "total": sum(p.price for p in self.items),
            "timestamp": self.created_at
        }
        self.db.save_order(order_dict)

class OrderBuilder:
    def __init__(self, client_name, address, is_vip=False):
        # id random para cliente
        client_id = random.randint(1000, 9999)
        self.client = Client(client_id, client_name, is_vip, address)

        # factory para definir estratégia
        if is_vip:
            self.strategy = VipDelivery()
        else:
            self.strategy = MotoDelivery()

        self.order = Order(self.client, self.strategy)

    def add_product(self, product: Product):
        p = SimpleProduct(product)
        self.order.items.append(p)
        return self

    def with_extra_bacon(self):
        if self.order.items:
            last_item = self.order.items.pop()
            self.order.items.append(ExtraBacon(last_item))
        return self

    def with_gift_wrap(self):
        if self.order.items:
            last_item = self.order.items.pop()
            self.order.items.append(GiftPackage(last_item))
        return self
    
    def add_observer(self, observer: OrderObserver):
        self.order.attach(observer)
        return self

    def build(self):
        return self.order