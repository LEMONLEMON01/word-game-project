from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from game_logic import game_instance

app = FastAPI(title="Connections Game")

# Serve static files from new folders
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/img", StaticFiles(directory="img"), name="img")

current_session = {
    "categories": [],
    "found_categories": [],
    "words": []
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Serve the main HTML file directly
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/game")
async def get_game():
    words, categories = game_instance.generate_game()
    
    current_session["categories"] = categories
    current_session["found_categories"] = []
    current_session["words"] = words

    return JSONResponse({
        "words": words,
        "categories": [{"name": cat.name, "words": cat.words} for cat in categories]
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
            "remaining": len(current_session["categories"]) - len(current_session["found_categories"])
        }
    return {"error": "Игра не найдена"}

@app.post("/api/new_game")
async def new_game():
    words, categories = game_instance.generate_game()
    
    current_session["categories"] = categories
    current_session["found_categories"] = []
    current_session["words"] = words

    return JSONResponse({"words": words})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)