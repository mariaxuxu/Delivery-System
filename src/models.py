from dataclasses import dataclass

@dataclass
class Client:
    id: int
    name: str
    is_vip: bool
    address: str

@dataclass
class Product:
    name: str
    price: float