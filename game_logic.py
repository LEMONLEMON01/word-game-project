from typing import List, Dict, Tuple
import random
from models import Category
from daily_game import daily_generator

class ConnectionsGame:
    def __init__(self):
        pass

    def generate_game(self) -> Tuple[List[str], List[Category]]:
        categories = daily_generator.get_daily_categories()
        all_words = [word for c in categories for word in c.words]
        random.shuffle(all_words)
        return all_words, categories

    def check_selection(self, selected_words: List[str], categories: List[Category]) -> Dict:
        for category in categories:
            if set(selected_words) == set(category.words):
                return {"valid": True, "category_name": category.name}

        return {"valid": False, "message": "Эти слова не образуют категорию"}


game_instance = ConnectionsGame()