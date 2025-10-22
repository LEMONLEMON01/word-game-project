from typing import List, Dict, Tuple
from dataclasses import dataclass
import random
import database


@dataclass
class Category:
    name: str
    words: List[str]


class ConnectionsGame:
    def __init__(self):
        pass

    def get_categories_from_db(self) -> List[Category]:
        try:
            db_categories = database.get_categories()
            categories = []

            for cat in db_categories:
                words = database.get_words_by_category(cat["category_id"])
                if len(words) >= 4:
                    categories.append(
                        Category(name=cat["category_name"], words=words[:4])
                    )

            return categories

        except Exception as e:
            print(f"Ошибка при загрузке категорий: {e}")
            return []

    def generate_game(self) -> Tuple[List[str], List[Category]]:
        categories = self.get_categories_from_db()
        if len(categories) < 4:
            return self._generate_fallback_game()

        selected = random.sample(categories, 4)
        all_words = [word for c in selected for word in c.words]
        random.shuffle(all_words)
        return all_words, selected

    def _generate_fallback_game(self):
        fallback = [
            Category("Фрукты", ["Яблоко", "Банан", "Апельсин", "Виноград"]),
            Category("Животные", ["Кошка", "Собака", "Лошадь", "Корова"]),
            Category("Цвета", ["Красный", "Синий", "Зеленый", "Желтый"]),
            Category("Города", ["Москва", "Париж", "Лондон", "Токио"]),
        ]
        all_words = [word for c in fallback for word in c.words]
        random.shuffle(all_words)
        return all_words, fallback

    def check_selection(self, selected_words: List[str], categories: List[Category]) -> Dict:
        for category in categories:
            if set(selected_words) == set(category.words):
                return {"valid": True, "category_name": category.name}

        return {"valid": False, "message": "Эти слова не образуют категорию"}


game_instance = ConnectionsGame()
