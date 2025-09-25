from ledger import Ledger
from datetime import datetime, date

def print_summary(ledger: Ledger):
    print("=== Budget Summary ===")
    print(f"Balance: {ledger.get_balance()} €")
    print("Transaktionen:")
    for t in ledger.transactions:
        print(" -", t)

def get_monthly_report(ledger: Ledger, year: int, month: int):
    print(f"=== Monatlicher Report von {month}-{year} ===")
    print("Transaktionen:")
    monthly_transactions = [
        t for t in ledger.transactions
        if (t_date := (t.date if isinstance(t.date, date) else datetime.strptime(t.date, '%Y-%m-%d'))).year == year
        and t_date.month == month
    ]

    monthly_expenses = sum(t.amount for t in monthly_transactions if t.type == "expense")
    monthly_income = sum(t.amount for t in monthly_transactions if t.type == "income")
    
    print(f"Einahmen: {monthly_income}")
    print(f"Ausgaben: {monthly_expenses}")
    print(f"Balance: {monthly_income-monthly_expenses}")
