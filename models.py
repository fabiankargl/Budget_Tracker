from datetime import date
import json

class Transaction:
    def __init__(self,
                 amount: float,
                 category: str,
                 t_type: str,
                 description: str = "",
                 t_date: date = None):
        self.amount = amount
        self.category = category
        self.type = t_type # income or expense
        self.description = description
        self.date = t_date if t_date else date.today()
    
    def __repr__(self):
        return f"{self.date} | {self.type.upper()} | {self.category}: {self.amount}€ ({self.description})"
    
class Category:
    def __init__(self,
                 category_name: str,
                 limit: int):
        self.category = category_name
        self.limit = limit

    def __repr__(self):
        shown_limit = 0
        if self.limit == 0 or not self.limit:
            shown_limit = "-"
        else:
            shown_limit = self.limit
        return f"{self.category} (Limit: {shown_limit}€)"

