from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime, timezone
import traceback
import os
import random

app = FastAPI(title="Connections Game API")

# Serve static files from the static directory
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Serve index.html for the root path
    @app.get("/")
    async def serve_index():
        return FileResponse("static/index.html")
    
    # Serve index.html for all other paths (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        return FileResponse("static/index.html")

# Health check endpoint - test if backend is running
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Connections Game API",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    return {"message": "Backend is working!", "test": "success"}

# Your existing game state
current_session = {
    "categories": [],
    "found_categories": [],
    "words": [],
    "game_date": None
}

# Fallback categories
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
        
        response_data = {
            "words": current_session["words"],
            "categories": current_session["categories"],
            "game_date": current_session["game_date"].isoformat()
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print(f"Error in /api/game: {e}")
        return JSONResponse({"error": "Internal server error"}, status_code=500)

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
                # Check if already found
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
        return JSONResponse({"error": "Internal server error"}, status_code=500)

@app.get("/api/game_status")
async def get_game_status():
    try:
        return {
            "found_categories": current_session["found_categories"],
            "total_categories": len(current_session["categories"]),
            "remaining": len(current_session["categories"]) - len(current_session["found_categories"]),
            "game_date": current_session["game_date"].isoformat() if current_session["game_date"] else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/daily_info")
async def get_daily_info():
    try:
        today = datetime.now(timezone.utc)
        return {
            "today": today.strftime("%Y-%m-%d"),
            "current_game_date": current_session["game_date"].strftime("%Y-%m-%d") if current_session["game_date"] else None,
            "is_new_day": False,  # Simplified for now
            "game_complete": len(current_session["found_categories"]) == 4,
            "found_count": len(current_session["found_categories"])
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True)