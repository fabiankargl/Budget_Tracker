from ledger import Ledger
from datetime import datetime, date

class ReportGenerator:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger

    def print_summary(self):
        print("=== Budget Summary ===")
        print(f"Balance: {self.ledger.get_balance()} €")
        print("Transaktionen:")
        for t in self.ledger.transactions:
            print(" -", t)

    def get_monthly_report(self,
                           year: int,
                           month: int):
        print(f"=== Monatlicher Report von {month}-{year} ===")
        print("Transaktionen:")
        date_format = '%Y-%m-%d'
        monthly_expenses = 0
        monthly_income = 0
        for t in self.ledger.transactions:
            if not isinstance(t.date, date):
                t_date = datetime.strptime(t.date, date_format)
            else:
                t_date = t.date
            if t_date.year == year and t_date.month == month:
                print(t)
                if t.type == "expense":
                    monthly_expenses += t.amount
                else:
                    monthly_income += t.amount
        
        print(f"Einahmen: {monthly_income}")
        print(f"Ausgaben: {monthly_expenses}")
        print(f"Balance: {monthly_income-monthly_expenses}")