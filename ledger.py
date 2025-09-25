from models import Transaction, Category
import json
from datetime import date

class Ledger:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    
    def _sum_transactions_by_type(self, t_type: str) -> float:
        return sum(t.amount for t in self.transactions if t.type == t_type)

    def get_balance(self):
        income = self._sum_transactions_by_type("income")
        expenses = self._sum_transactions_by_type("expense")
        return income - expenses
    
    def get_transactions_by_category(self, category: str):
        transactions = []
        for t in self.transactions:
            if t.category == category:
                transactions.append(t)
        
        return transactions

    def serialize_transaction(self, obj):
        if isinstance(obj, Transaction):
            data = obj.__dict__.copy()
            if isinstance(data.get('date'), date):
                data['date'] = data['date'].isoformat()
            if isinstance(data.get('category'), Category):
                data['category'] = f"{data['category'].category} ({data['category'].limit}€)"
            return data
    
    def save_to_json(self):
        json_file_path = "transaction.json"

        with open(json_file_path, 'w') as json_file:
            json.dump(self.transactions, json_file, default=self.serialize_transaction)
        
        print(f"Daten wurden gespeichert in {json_file_path}")
    
    def load_from_json(self):
        json_file_path = "transaction.json"

        with open(json_file_path) as f:
            transactions = json.load(f)
            
        for t in transactions:
            new_t = Transaction(amount=float(t["amount"]),
                                category=t["category"],
                                t_type=t["type"],
                                description=t["description"],
                                t_date=t["date"])
            self.add_transaction(new_t)