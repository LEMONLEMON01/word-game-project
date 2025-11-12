from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from game_logic import game_instance
from datetime import datetime, timezone

app = FastAPI(title="Connections Game - Daily")

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/img", StaticFiles(directory="img"), name="img")

current_session = {
    "categories": [],
    "found_categories": [],
    "words": [],
    "game_date": None
}

def is_new_day_needed():
    if not current_session["game_date"]:
        return True
    
    today = datetime.now(timezone.utc).date()
    game_date = current_session["game_date"].date()
    return today > game_date

def reset_game():
    words, categories = game_instance.generate_game()
    
    current_session["categories"] = categories
    current_session["found_categories"] = []
    current_session["words"] = words
    current_session["game_date"] = datetime.now(timezone.utc)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/game")
async def get_game():
    if is_new_day_needed() or not current_session["categories"]:
        reset_game()

    return JSONResponse({
        "words": current_session["words"],
        "categories": [{"name": cat.name, "words": cat.words} for cat in current_session["categories"]],
        "game_date": current_session["game_date"].isoformat()
    })

@app.post("/api/check_selection")
async def check_selection(request: Request):
    data = await request.json()
    selected_words = data.get("selected_words", [])
    
    if not current_session["categories"]:
        return JSONResponse({"error": "Игра не найдена"}, status_code=404)

    result = game_instance.check_selection(
        selected_words,
        current_session["categories"]
    )

    if result["valid"]:
        current_session["found_categories"].append({
            "name": result["category_name"],
            "words": selected_words
        })

        remaining = len(current_session["categories"]) - len(current_session["found_categories"])
        result["remaining"] = remaining
        result["game_complete"] = remaining == 0

    return JSONResponse(result)

@app.get("/api/game_status")
async def get_game_status():
    if current_session["categories"]:
        return {
            "found_categories": current_session["found_categories"],
            "total_categories": len(current_session["categories"]),
            "remaining": len(current_session["categories"]) - len(current_session["found_categories"]),
            "game_date": current_session["game_date"].isoformat()
        }
    return {"error": "Игра не найдена"}

@app.get("/api/daily_info")
async def get_daily_info():
    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y-%m-%d")
    
    game_complete = len(current_session["found_categories"]) == 4 if current_session["found_categories"] else False
    
    return {
        "today": today_str,
        "current_game_date": current_session["game_date"].strftime("%Y-%m-%d") if current_session["game_date"] else None,
        "is_new_day": is_new_day_needed(),
        "game_complete": game_complete,
        "found_count": len(current_session["found_categories"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)