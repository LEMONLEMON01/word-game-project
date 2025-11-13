from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timezone
import traceback
import os
import random

app = FastAPI(title="Connections Game API")

# Serve static files with proper configuration
if os.path.exists("static"):
    # Mount assets directory with proper MIME types
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    
    # Serve index.html for the root path
    @app.get("/")
    async def serve_index():
        return FileResponse("static/index.html")
    
    # Serve other static files
    @app.get("/{filename:path}")
    async def serve_static(filename: str):
        static_path = f"static/{filename}"
        if os.path.exists(static_path):
            return FileResponse(static_path)
        
        # Fallback to index.html for SPA routing
        if os.path.exists("static/index.html"):
            return FileResponse("static/index.html")
        
        return {"error": "File not found"}

# API endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Your existing game code...
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
        print(f"Error in /api/game: {e}")
        return {"error": "Internal server error"}

@app.post("/api/check_selection")
async def check_selection(selected_words: list[str]):
    try:
        if len(selected_words) != 4:
            return {
                "valid": False,
                "message": "Выберите ровно 4 слова"
            }

        for category in current_session["categories"]:
            if set(selected_words) == set(category["words"]):
                if any(cat["name"] == category["name"] for cat in current_session["found_categories"]):
                    return {
                        "valid": False,
                        "message": f"Категория '{category['name']}' уже найдена"
                    }
                
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
        print(f"Error in /api/check_selection: {e}")
        return {"error": "Internal server error"}

@app.get("/api/game_status")
async def get_game_status():
    return {
        "found_categories": current_session["found_categories"],
        "total_categories": len(current_session["categories"]),
        "remaining": len(current_session["categories"]) - len(current_session["found_categories"]),
        "game_date": current_session["game_date"].isoformat() if current_session["game_date"] else None
    }

@app.get("/api/daily_info")
async def get_daily_info():
    return {
        "today": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "current_game_date": current_session["game_date"].strftime("%Y-%m-%d") if current_session["game_date"] else None,
        "is_new_day": False,
        "game_complete": len(current_session["found_categories"]) == 4,
        "found_count": len(current_session["found_categories"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)