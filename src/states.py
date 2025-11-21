from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def next(self, order): pass
    @abstractmethod
    def cancel(self, order): pass
    @abstractmethod
    def get_name(self) -> str: pass

class CreatedState(OrderState):
    def next(self, order):
        print("--- Pagamento aprovado. Enviando para cozinha... ---")
        from .states import CookingState
        order.set_state(CookingState())

    def cancel(self, order):
        print("Pedido cancelado.")
        order.set_state(CancelledState())

    def get_name(self): return "CRIADO / AGUARDANDO PAGAMENTO"

class CookingState(OrderState):
    def next(self, order):
        print("--- Comida pronta! Chamando entregador... ---")
        from .states import OnRouteState
        order.set_state(OnRouteState())

    def cancel(self, order):
        print("ERRO: Não pode cancelar. A comida já está sendo feita!")

    def get_name(self): return "PREPARANDO NA COZINHA"

class OnRouteState(OrderState):
    def next(self, order):
        print("--- Pedido entregue no destino! ---")
        from .states import DeliveredState
        order.set_state(DeliveredState())
        order.save_to_db()
    
    def cancel(self, order):
        print("ERRO: O motoboy já saiu!")

    def get_name(self): return "EM ROTA DE ENTREGA"

class DeliveredState(OrderState):
    def next(self, order): print("Pedido já finalizado.")
    def cancel(self, order): print("Pedido já finalizado.")
    def get_name(self): return "ENTREGUE"

class CancelledState(OrderState):
    def next(self, order): pass
    def cancel(self, order): pass
    def get_name(self): return "CANCELADO"