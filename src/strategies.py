from abc import ABC, abstractmethod

class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate_total(self, subtotal: float, distance_km: float) -> float:
        pass

class MotoDelivery(DeliveryStrategy):
    def calculate_total(self, subtotal: float, distance_km: float) -> float:
        # taxa fixa 5.00 + 1.00/km
        return subtotal + 5.00 + (distance_km * 1.00)

class DroneDelivery(DeliveryStrategy):
    def calculate_total(self, subtotal: float, distance_km: float) -> float:
        # taxa fixa 15.00 + 2.00/km
        return subtotal + 15.00 + (distance_km * 2.00)

class VipDelivery(DeliveryStrategy):
    def calculate_total(self, subtotal: float, distance_km: float) -> float:
        # frete grátis + 10% desconto na comida
        return subtotal * 0.90