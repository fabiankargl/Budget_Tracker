from ledger import Ledger
from models import Transaction, Category
from reports import ReportGenerator
from categorymanager import CategoryManager
from utils import select_category
import readchar

class BudgetApp:
    def __init__(self):
        self.ledger = Ledger()
        self.reporter = ReportGenerator(self.ledger)
        self.cat_manager = CategoryManager()

    def run(self):
        print("Lädt Transaktionen....")
        self.ledger.load_from_json()
        while True:
            print("\n=== Budget Tracker ===")
            print("1) Neue Transaktion hinzufügen")
            print("2) Alle Transaktionen anzeigen")
            print("3) Zusammenfassung anzeigen")
            print("4) Kategorie hinzufügen")
            print("5) Kategorie löschen")
            print("6) Monatlicher Report")
            print("7) Beenden")

            choice = input("Wähle eine Option: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.show_transactions()
            elif choice == "3":
                self.reporter.print_summary()
            elif choice == "4": 
                category_name = input("Neue Kategorie: ")
                category_limit = input("Kategorie Limit (Optional): ")
                new_cat = Category(category_name=category_name,
                                   limit=category_limit)
                self.cat_manager.add_category(category=new_cat)
            elif choice == "5":
                self.remove_category()
            elif choice == "6":
                year = int(input("Jahr: "))
                month = int(input("Monat: "))
                self.reporter.get_monthly_report(year, month)
            elif choice == "7":
                print("Auf Wiedersehen!")
                self.ledger.save_to_json()
                break
            else:
                print("Ungültige Auswahl!")

    def add_transaction(self):
        amount = float(input("Betrag: "))

        categories = self.cat_manager.categories
        index = select_category(categories=categories)
        category = categories[index]

        try:
            limit = float(category.limit)
            if limit > 0 and amount > limit:
                print(f"Warnung: Betrag ({amount}€) überschreitet das Limit der Kategorie ({limit}€)!")
        except (ValueError, AttributeError):
            pass

        t_type = input("Typ (income/expense): ")
        description = input("Beschreibung: ")

        t = Transaction(amount=amount,
                        category=category,
                        t_type=t_type,
                        description=description)
        self.ledger.add_transaction(transaction=t)
        print("Transaktion gespeichert")

    
    def show_transactions(self):
        if not self.ledger.transactions:
            print("Keine Transaktionen vorhanden")
        for t in self.ledger.transactions:
            print(t)

    def remove_category(self):
        categories = self.cat_manager.categories
        index = select_category(categories=categories)
        category = categories[index]

        self.cat_manager.delete_category(category=category)
        print("Kategorie erfolgreich gelöscht")