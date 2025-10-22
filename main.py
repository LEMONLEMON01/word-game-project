from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List
import json

#надо через командную строку зайти в папку проекта, скачать requirements
#ввести python -m uvicorn main:app --reload и запустить http://localhost:8000/

from game_logic import game_instance, Category

app = FastAPI(title="Connections Game")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

current_games = {}


@app.get("/")
async def home(request: Request):
    game_id = "default"  # должен быть уникальный ID
    words, categories = game_instance.generate_game()

    current_games[game_id] = {
        "categories": categories,
        "found_categories": []
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "words": words,
        "game_id": game_id
    })


@app.post("/check_selection")
async def check_selection(game_id: str = Form(...), selected_words: str = Form(...)):
    try:
        words_list = json.loads(selected_words)

        if game_id not in current_games:
            return JSONResponse({"error": "Игра не найдена"}, status_code=404)

        result = game_instance.check_selection(
            words_list,
            current_games[game_id]["categories"]
        )

        if result["valid"]:
            current_games[game_id]["found_categories"].append({
                "name": result["category_name"],
                "words": words_list
            })

            remaining = len(current_games[game_id]["categories"]) - len(current_games[game_id]["found_categories"])
            result["remaining"] = remaining
            result["game_complete"] = remaining == 0

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.get("/game_status/{game_id}")
async def get_game_status(game_id: str):
    if game_id in current_games:
        return {
            "found_categories": current_games[game_id]["found_categories"],
            "total_categories": len(current_games[game_id]["categories"]),
            "remaining": len(current_games[game_id]["categories"]) - len(current_games[game_id]["found_categories"])
        }
    return {"error": "Игра не найдена"}


@app.post("/new_game")
async def new_game():
    game_id = "default"  # должен быть уникальный ID
    words, categories = game_instance.generate_game()

    current_games[game_id] = {
        "categories": categories,
        "found_categories": []
    }

    return JSONResponse({
        "words": words,
        "game_id": game_id
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)