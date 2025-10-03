import json
from models import Category

class CategoryManager:
    def __init__(self):
        self.categories = []
        self.load_standard_categories()

    def __len__(self):
        return len(self.categories)
    
    def __getitem__(self, index):
        return self.categories[index]

    def __iter__(self):
        return iter(self.categories)
    
    def __next__(self):
        if self._index < len(self.categories):
            cat = self.categories[self._index]
            self._index += 1
            return cat
        else:
            raise StopIteration

    def load_standard_categories(self):
        json_file_path = "categories.json"

        with open(json_file_path) as f:
            categories = json.load(f)

        self.categories = [
            Category(category_name=cat["category"], limit=cat["limit"]) if isinstance(cat, dict) else cat
            for cat in categories
        ]


    def save_categories(self):
        json_file_path = "categories.json"

        categories_as_dicts = [
            {"category": cat.category, "limit": cat.limit}
            if isinstance(cat, Category) else cat
            for cat in self.categories
        ]

        with open(json_file_path, 'w') as json_file:
            json.dump(categories_as_dicts, json_file)
        
        print(f"Daten wurden gespeichert in {json_file_path}")
    
    def add_category(self, category: Category):
        self.categories.append(category)
        self.save_categories()
    
    def delete_category(self, category: Category):
        self.categories.remove(category)
        self.save_categories()