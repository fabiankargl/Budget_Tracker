from pathlib import Path
import json
from typing import Optional, Union, Dict, List
from models import Category

def norm_key(s: str) -> str:
    return (s or "").strip().casefold()

def to_float(val) -> float:
    try:
        return float(str(val).replace(",", ".").strip())
    except (TypeError, ValueError):
        return 0.0

class CategoryManager:
    def __init__(self):
        self.categories: List[Category] = []
        self._by_key: Dict[str, Category] = {}
        self.load_standard_categories()

    def _index_reset(self):
        self._by_key = {norm_key(c.category): c for c in self.categories}

    def _index_add(self, c: Category):
        self._by_key[norm_key(c.category)] = c

    def has_category(self, name: str) -> bool:
        return norm_key(name) in self._by_key

    def get_category(self, name: str) -> Optional[Category]:
        return self._by_key.get(norm_key(name))

    def load_standard_categories(self):
        json_file_path = "categories.json"
        path = Path(json_file_path)

        try:
            if not path.exists():
                print("[WARN] categories.json fehlt – starte mit leerer Liste.")
                self.categories = []
                self._index_reset()
                return

            with path.open(encoding="utf-8") as f:
                raw = json.load(f)

        except json.JSONDecodeError as e:
            print(f"[ERROR] Ungültiges JSON in {json_file_path}: {e}")
            self.categories = []
            self._index_reset()
            return
        except OSError as e:
            print(f"[ERROR] Datei-Problem {json_file_path}: {e}")
            self.categories = []
            self._index_reset()
            return

        # Liste neu aufbauen
        self.categories = []
        if not isinstance(raw, list):
            print(f"[WARN] Erwartete Liste in {json_file_path}, gefunden: {type(raw).__name__}")
            self._index_reset()
            return

        for cat in raw:
            try:
                if isinstance(cat, dict):
                    name = str(cat.get("category", "")).strip()
                    if not name:
                        print("[WARN] Kategorie ohne Namen übersprungen.")
                        continue
                    limit = to_float(cat.get("limit", 0))
                    if limit < 0:
                        print("[WARN] Negatives Limit erkannt – auf 0 gesetzt.")
                        limit = 0.0
                    self.categories.append(Category(category_name=name, limit=limit))
                elif isinstance(cat, Category):
                    self.categories.append(cat)
                else:
                    print(f"[WARN] Unerwarteter Typ in categories.json: {type(cat).__name__}")
            except (KeyError, TypeError, ValueError) as e:
                print(f"[WARN] Konnte Kategorie nicht laden {cat}: {e}")

        self._index_reset()

    def save_categories(self):
        json_file_path = "categories.json"
        payload = [{"category": c.category, "limit": c.limit} for c in self.categories]
        try:
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(payload, json_file, ensure_ascii=False, indent=2)
            print(f"Daten wurden gespeichert in {json_file_path}")
        except OSError as e:
            print(f"[ERROR] Speichern fehlgeschlagen ({json_file_path}): {e}")

    def add_category(self, category: Category):
        key = norm_key(category.category)
        if key in self._by_key:
            print("[INFO] Kategorie existiert bereits (case-insensitive).")
            return
        # Limit sanitisieren (falls von außen String/negativ kommt)
        category.limit = max(0.0, to_float(getattr(category, "limit", 0)))
        self.categories.append(category)
        self._index_add(category)
        self.save_categories()

    def delete_category(self, category: Union[Category, str]):
        # sowohl Objekt als auch Name erlauben
        if isinstance(category, Category):
            key = norm_key(category.category)
            obj = self._by_key.get(key)
        else:
            key = norm_key(category)
            obj = self._by_key.get(key)

        if not obj:
            print(f"[WARN] Kategorie nicht vorhanden: {category}")
            return

        self.categories.remove(obj)
        self._by_key.pop(key, None)
        self.save_categories()

