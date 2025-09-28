from ledger import Ledger
from models import Transaction, Category
from reports import ReportGenerator
from categorymanager import CategoryManager
import readchar

MENU_OPTIONS = {
    "1": "Neue Transaktion hinzufügen",
    "2": "Alle Transaktionen anzeigen",
    "3": "Zusammenfassung anzeigen",
    "4": "Kategorie hinzufügen",
    "5": "Kategorie löschen",
    "6": "Monatlicher Report",
    "7": "Beenden"
}

MSG_LOADING = "Lädt Transaktionen..."
MSG_GOODBYE = "Auf Wiedersehen"
MSG_INVALID = "Ungültige Auswahl"
MSG_NO_TRANSACTION = "Keine Transaktion vorhanden"
MSG_SAVED = "Transaktion gespeichert"
MSG_CAT_DELETED = "Kategorie erfolgreich gelöscht"


KEY_UP = readchar.key.UP
KEY_DOWN = readchar.key.DOWN
KEY_ENTER = readchar.key.ENTER

class BudgetApp:
    def __init__(self):
        self.ledger = Ledger()
        self.reporter = ReportGenerator(self.ledger)
        self.cat_manager = CategoryManager()

    def run(self):
        print(MSG_LOADING)
        self.ledger.load_from_json()

        while True:
            print("\n=== Budget Tracker ===")
            for k, label in MENU_OPTIONS.items():
                print(f"{k}) {label}")

            choice = input("Wähle eine Option: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.show_transactions()
            elif choice == "3":
                self.reporter.print_summary()
            elif choice == "4": 
                self.add_category()
            elif choice == "5":
                self.remove_category()
            elif choice == "6":
                self.monthly_report()
            elif choice == "7":
                print(MSG_GOODBYE)
                self.ledger.save_to_json()
                break
            else:
                print(MSG_INVALID)

    def add_transaction(self):
        amount = float(input("Betrag: "))

        categories = self.cat_manager
        index = 0

        print("Kategorie mit Pfeiltasten auswählen und Enter drücken:")
        while True:
            for i, cat in enumerate(categories):
                prefix = "-> " if i == index else "  "
                print(f"{prefix}{cat}")
            key = readchar.readkey()
            if key == KEY_UP:
                index = (index - 1) % len(categories)
            elif key == KEY_DOWN:
                index = (index + 1) % len(categories)
            elif key == KEY_ENTER:
                break
            print("\033c", end="")
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
        print(MSG_SAVED)

    
    def show_transactions(self):
        if not self.ledger:
            print(MSG_NO_TRANSACTION)
        for t in self.ledger:
            print(t)

    def add_category(self):
        cat_name = input("Neue Kategorie: ")
        cat_limit = input("Kategorie Limit: ")
        new_cat = Category(cat_name=cat_name, limit=cat_limit)
        self.cat_manager.add_category(category=new_cat)

    def remove_category(self):
        categories = self.cat_manager
        index = 0

        print("Kategorie mit Pfeiltasten auswählen und Enter drücken: ")
        while True:
            for i, cat in enumerate(categories):
                prefix = "-> " if i == index else "  "
                print(f"{prefix}{cat}")
            key = readchar.readkey()
            if key == KEY_UP:
                index = (index - 1) % len(categories)
            elif key == KEY_DOWN:
                index = (index + 1) % len(categories)
            elif key == KEY_ENTER:
                break
            print("\033c", end="")
        category = categories[index]

        self.cat_manager.delete_category(category=category)
        print(MSG_CAT_DELETED)

    def monthly_report(self):
        year = int(input("Jahr: "))
        month = int(input("Monat: "))
        self.reporter.get_monthly_report(year, month)