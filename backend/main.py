from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from datetime import datetime, timezone
import os
import random

app = FastAPI(title="Connections Game API")

# Serve static files with explicit MIME type handling
@app.get("/assets/{file_path:path}")
async def serve_assets(file_path: str):
    """Serve static assets with correct MIME types"""
    asset_path = f"static/assets/{file_path}"
    
    if not os.path.exists(asset_path):
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Set correct MIME types
    if file_path.endswith('.js'):
        return FileResponse(asset_path, media_type="application/javascript")
    elif file_path.endswith('.css'):
        return FileResponse(asset_path, media_type="text/css")
    elif file_path.endswith('.png'):
        return FileResponse(asset_path, media_type="image/png")
    elif file_path.endswith('.ico'):
        return FileResponse(asset_path, media_type="image/x-icon")
    else:
        return FileResponse(asset_path)

@app.get("/src/{file_path:path}")
async def serve_src(file_path: str):
    """Serve source files"""
    src_path = f"static/src/{file_path}"
    if os.path.exists(src_path):
        if src_path.endswith('.js') or src_path.endswith('.ts'):
            return FileResponse(src_path, media_type="application/javascript")
        return FileResponse(src_path)
    raise HTTPException(status_code=404)

# Serve index.html for root and all other routes
@app.get("/")
async def serve_index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not built"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not found"}

# API endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Game logic
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