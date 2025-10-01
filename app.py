from ledger import Ledger
from models import Transaction, Category
from reports import ReportGenerator
from categorymanager import CategoryManager
import readchar

class BudgetApp:
    def __init__(self):
        self.remove_category = None
        self.show_transactions = None
        self.add_transaction = None
        self.ledger = Ledger()
        self.reporter = ReportGenerator(self.ledger)
        self.cat_manager = CategoryManager()

    def run(self):
        print("Lädt Transaktionen....")
        self.ledger.load_from_json()
        """while True:
            print("\n=== Budget Tracker ===")
            print("1) Neue Transaktion hinzufügen")
            print("2) Alle Transaktionen anzeigen")
            print("3) Zusammenfassung anzeigen")
            print("4) Kategorie hinzufügen")
            print("5) Kategorie löschen")
            print("6) Monatlicher Report")
            print("7) Beenden")
        """
        ACTIONS = {
            "1": self.add_transaction,
            "2": self.show_transactions,
            "3": self.reporter.print_summary,
            "4": self.cat_manager.add_category,
            "5": self.remove_category,
            "6": self.reporter.get_monthly_report,
            "7": self.ledger.save_to_json(),
        }

        while True:
            print("\n=== Budget Tracker ===")
            print("1) Neue Transaktion hinzufügen")
            print("2) Alle Transaktionen anzeigen")
            print("3) Zusammenfassung anzeigen")
            print("4) Kategorie hinzufügen")
            print("5) Kategorie löschen")
            print("6) Monatlicher Report")
            print("7) Beenden")

            choice = input("Wähle: ").strip()
            action = ACTIONS.get(choice)
            (ACTIONS.get(choice) or (lambda: print("Ungültige Auswahl")))

            def add_category_flow(self):
                category_name = input("Neue Kategorie: ").strip()
                limit_raw = input("Kategorie Limit (Optional): ").strip().replace(",", ".")
                try:
                    limit = float(limit_raw) if limit_raw else 0.0
                    if limit < 0:
                        print("[WARN] Negatives Limit wird zu 0 gesetzt.")
                        limit = 0.0
                except ValueError:
                    print("[WARN] Ungültiges Limit – setze 0.")
                    limit = 0.0
                new_cat = Category(category_name=category_name, limit=limit)
                self.cat_manager.add_category(category=new_cat)
                print("Kategorie gespeichert.")

            def add_transaction(self):
                amount = self._read_float("Betrag: ")

                category = self._pick_from_list(self.cat_manager.categories, title="Kategorie")
                if category is None:
                    return

                # Limit prüfen (robust gegen String/None)
                try:
                    limit_val = float(getattr(category, "limit", 0) or 0)
                    if limit_val > 0 and amount > limit_val:
                        print(f"Warnung: Betrag ({amount}€) überschreitet das Limit der Kategorie ({limit_val}€)!")
                except (TypeError, ValueError):
                    pass

                t_type = self._read_type()
                description = input("Beschreibung: ").strip()

                t = Transaction(amount=amount, category=category, t_type=t_type, description=description)
                self.ledger.add_transaction(transaction=t)
                self.ledger.save_to_json()  # Autosave
                print("Transaktion gespeichert")

            def show_transactions(self):
                if not self.ledger.transactions:
                    print("Keine Transaktionen vorhanden")
                    return
                for t in self.ledger.transactions:
                    print(t)

            def remove_category(self):
                category = self._pick_from_list(self.cat_manager.categories, title="Kategorie")
                if category is None:
                    return
                self.cat_manager.delete_category(category=category)
                print("Kategorie erfolgreich gelöscht")

            def monthly_report_flow(self):
                year = self._read_int("Jahr: ", lo=1900, hi=9999)
                month = self._read_int("Monat (1-12): ", lo=1, hi=12)
                self.reporter.get_monthly_report(year, month)

            def _exit_app(self):
                print("Auf Wiedersehen!")
                self.ledger.save_to_json()
                raise SystemExit(0)
"""
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
        index = 0

        print("Kategorie mit Pfeiltasten auswählen und Enter drücken:")
        while True:
            for i, cat in enumerate(categories):
                prefix = "-> " if i == index else "  "
                print(f"{prefix}{cat}")
            key = readchar.readkey()
            if key == readchar.key.UP:
                index = (index - 1) % len(categories)
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(categories)
            elif key == readchar.key.ENTER:
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
        print("Transaktion gespeichert")

    
    def show_transactions(self):
        if not self.ledger.transactions:
            print("Keine Transaktionen vorhanden")
        for t in self.ledger.transactions:
            print(t)

    def remove_category(self):
        categories = self.cat_manager.categories
        index = 0

        print("Kategorie mit Pfeiltasten auswählen und Enter drücken:")
        while True:
            for i, cat in enumerate(categories):
                prefix = "-> " if i == index else "  "
                print(f"{prefix}{cat}")
            key = readchar.readkey()
            if key == readchar.key.UP:
                index = (index - 1) % len(categories)
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(categories)
            elif key == readchar.key.ENTER:
                break

            print("\033c", end="")
        category = categories[index]

        self.cat_manager.delete_category(category=category)
        print("Kategorie erfolgreich gelöscht")"""