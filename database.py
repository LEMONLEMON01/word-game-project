import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "wordsdb.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_categories() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT category_id, category_name FROM categories")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def get_words_by_category(category_id: int) -> List[str]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT word FROM words WHERE category_id = ?", (category_id,))
        rows = cur.fetchall()
        return [row["word"] for row in rows]
    
def create_game(user_id: int) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO games (user_id, score, errors) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        return cur.lastrowid

def update_game(game_id: int, score: int, errors: int): 
    with get_connection() as conn: 
        cur = conn.cursor() 
        cur.execute( "UPDATE games SET score = ?, errors = ? WHERE game_id = ?", (score, errors, game_id) ) 
        conn.commit()
        
def get_game(game_id: int): 
    with get_connection() as conn: 
        cur = conn.cursor() 
        cur.execute("SELECT * FROM games WHERE game_id = ?", (game_id,)) 
        return cur.fetchone()