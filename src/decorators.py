from abc import ABC, abstractmethod
from .models import Product

class ProductComponent(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def price(self) -> float: pass

class SimpleProduct(ProductComponent):
    def __init__(self, product: Product):
        self._product = product
    
    @property
    def name(self) -> str: return self._product.name
    
    @property
    def price(self) -> float: return self._product.price

class ProductDecorator(ProductComponent):
    def __init__(self, component: ProductComponent):
        self.component = component

    @property
    def name(self) -> str: return self.component.name

    @property
    def price(self) -> float: return self.component.price

class ExtraBacon(ProductDecorator):
    @property
    def name(self) -> str: return f"{self.component.name} + Bacon Extra"
    
    @property
    def price(self) -> float: return self.component.price + 5.00

class GiftPackage(ProductDecorator):
    @property
    def name(self) -> str: return f"{self.component.name} (Embalagem Presente)"
    
    @property
    def price(self) -> float: return self.component.price + 12.00