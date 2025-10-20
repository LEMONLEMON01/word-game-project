from typing import List, Dict, Tuple
import random
from dataclasses import dataclass


@dataclass
class Category:
    name: str
    words: List[str]
    description: str


class ConnectionsGame:
    def __init__(self):
        self.categories_pool = [
            Category(
                name="Фрукты",
                words=["яблоко", "банан", "апельсин", "виноград"],
                description="Сочные съедобные плоды"
            ),
            Category(
                name="Животные",
                words=["собака", "кошка", "лошадь", "корова"],
                description="Домашние питомцы"
            ),
            Category(
                name="Цвета",
                words=["красный", "синий", "зеленый", "желтый"],
                description="Основные цвета"
            ),
            Category(
                name="Города",
                words=["Москва", "Париж", "Лондон", "Токио"],
                description="Столицы мира"
            ),
            Category(
                name="Профессии",
                words=["врач", "учитель", "инженер", "повар"],
                description="Виды занятости"
            ),
            Category(
                name="Спорт",
                words=["футбол", "баскетбол", "теннис", "бокс"],
                description="Виды спорта"
            ),
            Category(
                name="Технологии",
                words=["компьютер", "смартфон", "планшет", "ноутбук"],
                description="Электронные устройства"
            ),
            Category(
                name="Напитки",
                words=["кофе", "чай", "сок", "вода"],
                description="Жидкости для питья"
            )
        ]

    def generate_game(self) -> Tuple[List[str], List[Category]]:
        """Генерирует новую игру с 4 случайными категориями"""
        selected_categories = random.sample(self.categories_pool, 4)

        # Собираем все слова из выбранных категорий
        all_words = []
        for category in selected_categories:
            all_words.extend(category.words)

        # Перемешиваем слова
        random.shuffle(all_words)

        return all_words, selected_categories

    def check_selection(self, selected_words: List[str], categories: List[Category]) -> Dict:
        """Проверяет, образуют ли выбранные слова валидную категорию"""
        for category in categories:
            if set(selected_words) == set(category.words):
                return {
                    "valid": True,
                    "category_name": category.name,
                    "description": category.description
                }

        return {"valid": False, "message": "Эти слова не образуют категорию"}

    def calculate_difficulty(self, category: Category) -> str:
        """Определяет сложность категории (простая реализация)"""
        difficulties = ["🟨 Легко", "🟩 Средне", "🟦 Сложно", "🟪 Очень сложно"]
        return random.choice(difficulties)


game_instance = ConnectionsGame()