import json
import os
from typing import List

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_file = "data/database.json"
            cls._instance._ensure_db_exists()
        return cls._instance

    def _ensure_db_exists(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def save_order(self, order_data: dict):
        data = self.get_all_orders()
        data.append(order_data)
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[DATABASE] Pedido salvo com sucesso em {self.db_file}")

    def get_all_orders(self) -> List[dict]:
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def log(self, message: str):
        print(f"[SYSTEM LOG]: {message}")