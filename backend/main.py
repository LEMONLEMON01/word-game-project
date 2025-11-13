from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timezone
import os
import random

app = FastAPI(title="Connections Game API")

# Serve static files - this is the key fix
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html for all routes (SPA)
@app.get("/")
async def serve_index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not built"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not built"}

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Your game logic (simplified for now)
current_session = {
    "categories": [],
    "found_categories": [],
    "words": [],
    "game_date": None
}

fallback_categories = [
    {"name": "Фрукты", "words": ["Яблоко", "Апельсин", "Банан", "Виноград"]},
    {"name": "Транспорт", "words": ["Машина", "Автобус", "Поезд", "Велосипед"]},
    {"name": "Цвета", "words": ["Красный", "Синий", "Зеленый", "Желтый"]},
    {"name": "Животные", "words": ["Собака", "Кошка", "Птица", "Рыба"]}
]

def reset_game():
    all_words = []
    for category in fallback_categories:
        all_words.extend(category["words"])
    
    random.shuffle(all_words)
    
    current_session["categories"] = fallback_categories
    current_session["found_categories"] = []
    current_session["words"] = all_words
    current_session["game_date"] = datetime.now(timezone.utc)

@app.get("/api/game")
async def get_game():
    try:
        if not current_session["words"]:
            reset_game()
        
        return {
            "words": current_session["words"],
            "categories": current_session["categories"],
            "game_date": current_session["game_date"].isoformat()
        }
        
    except Exception as e:
        return {"error": "Internal server error"}

@app.post("/api/check_selection")
async def check_selection(selected_words: list[str]):
    try:
        for category in current_session["categories"]:
            if set(selected_words) == set(category["words"]):
                current_session["found_categories"].append({
                    "name": category["name"],
                    "words": selected_words
                })

                remaining = len(current_session["categories"]) - len(current_session["found_categories"])
                
                return {
                    "valid": True,
                    "category_name": category["name"],
                    "remaining": remaining,
                    "game_complete": remaining == 0
                }

        return {
            "valid": False,
            "message": "Эти слова не образуют категорию"
        }
        
    except Exception as e:
        return {"error": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)