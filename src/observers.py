from abc import ABC, abstractmethod

class OrderObserver(ABC):
    @abstractmethod
    def update(self, order_id: str, status_name: str):
        pass

class CustomerEmailNotifier(OrderObserver):
    def __init__(self, client_email: str):
        self.email = client_email

    def update(self, order_id: str, status_name: str):
        print(f"[EMAIL para {self.email}]: O pedido #{order_id} mudou para: {status_name}")

class RestaurantAppNotifier(OrderObserver):
    def update(self, order_id: str, status_name: str):
        print(f"[RESTAURANTE APP]: Atenção! Atualização no pedido #{order_id}: {status_name}")