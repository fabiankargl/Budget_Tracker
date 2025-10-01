import json
from models import Category

from pathlib import Path
import json
from models import Category

class CategoryManager:
    def __init__(self):
        self.categories = []
        self.load_standard_categories()

    def load_standard_categories(self):
        json_file_path = "categories.json"
        path = Path(json_file_path)

        try:
            if not path.exists():
                print("Warnung: Categories JSON fehlt")
                self.categories = []
                return

            with path.open(encoding="utf-8") as f:
                categories = json.load(f)

        except json.JSONDecodeError as e:
            print(f"Fehler: Ungültiges JSON in {json_file_path}: {e}")
            self.categories = []
            return
        except OSError as e:
            print(f"Fehler: Datei-Problem {json_file_path}: {e}")
            self.categories = []
            return

        # Liste neu aufbauen
        self.categories = []
        for cat in categories:
            try:
                if isinstance(cat, dict):
                    name = str(cat.get("category", "")).strip()
                    limit_raw = cat.get("limit", 0)
                    if isinstance(limit_raw, str):
                        limit = int(limit_raw) if limit_raw.strip().isdigit() else 0
                    else:
                        limit = int(limit_raw)
                    self.categories.append(Category(category_name=name, limit=limit))
                elif isinstance(cat, Category):
                    self.categories.append(cat)
                else:
                    print(f"[WARN] Unerwarteter Typ in categories.json: {type(cat)}")
            except Exception as e:
                print(f"[WARN] Konnte Kategorie nicht laden {cat}: {e}")

    def save_categories(self):
        json_file_path = "categories.json"
        categories_as_dicts = [
            {"category": c.category, "limit": c.limit}
            if isinstance(c, Category) else c
            for c in self.categories
        ]
        try:
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(categories_as_dicts, json_file, ensure_ascii=False, indent=2)
            print(f"Daten wurden gespeichert in {json_file_path}")
        except OSError as e:
            print(f"[ERROR] Speichern fehlgeschlagen ({json_file_path}): {e}")

    def add_category(self, category: Category):
        self.categories.append(category)
        self.save_categories()

    def delete_category(self, category: Category):
        try:
            self.categories.remove(category)
            self.save_categories()
        except ValueError:
            print(f"[WARN] Kategorie nicht vorhanden: {category}")
