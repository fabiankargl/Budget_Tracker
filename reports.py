from ledger import Ledger
from datetime import datetime, date


def print_summary(ledger: Ledger):
    print("=== Budget Summary ===")
    print(f"Balance: {ledger.get_balance()} €")
    print("Transaktionen:")
    for t in ledger:
        print(" -", t)

def get_monthly_report(ledger: Ledger, year: int, month: int):
    print(f"=== Monatlicher Report von {month:02d}-{year} ===")
    print("Transaktionen:")
    
    date_format = '%Y-%m-%d'

    monthly_transactions = [
        t for t in ledger
        if (t_date := datetime.strptime(t.date, date_format) if isinstance(t.date, str) else t.date)
        and t_date.year == year 
        and t_date.month == month
    ]
    
    for t in monthly_transactions:
        print(t)
        
    monthly_expenses = sum(t.amount for t in monthly_transactions if t.type == "expense")
    monthly_income = sum(t.amount for t in monthly_transactions if t.type == "income")
    
    print(f"\nEinahmen: {monthly_income:,.2f}")
    print(f"Ausgaben: {monthly_expenses:,.2f}")
    print(f"Balance: {monthly_income - monthly_expenses:,.2f}")
