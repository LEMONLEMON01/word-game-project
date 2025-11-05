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

current_session = {
    "categories": [],
    "found_categories": [],
    "words": []
}

@app.get("/")
async def home(request: Request):
    words, categories = game_instance.generate_game()
    
    current_session["categories"] = categories
    current_session["found_categories"] = []
    current_session["words"] = words

    return templates.TemplateResponse("index.html", {
        "request": request,
        "words": words
    })


@app.post("/check_selection")
async def check_selection(selected_words: str = Form(...)):
    try:
        words_list = json.loads(selected_words)

        if not current_session["categories"]:
            return JSONResponse({"error": "Игра не найдена"}, status_code=404)

        result = game_instance.check_selection(
            words_list,
            current_session["categories"]
        )

        if result["valid"]:
            current_session["found_categories"].append({
                "name": result["category_name"],
                "words": words_list
            })

            remaining = len(current_session["categories"]) - len(current_session["found_categories"])
            result["remaining"] = remaining
            result["game_complete"] = remaining == 0

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.get("/game_status")
async def get_game_status():
    if current_session["categories"]:
        return {
            "found_categories": current_session["found_categories"],
            "total_categories": len(current_session["categories"]),
            "remaining": len(current_session["categories"]) - len(current_session["found_categories"])
        }
    return {"error": "Игра не найдена"}

@app.get("/current_game")
async def get_current_game():
    """Возвращает текущую активную игру"""
    if current_session["words"]:
        return {
            "words": current_session["words"],
            "found_categories": current_session["found_categories"],
            "total_categories": len(current_session["categories"])
        }
    return {"error": "Нет активной игры"}

@app.post("/new_game")
async def new_game():
    words, categories = game_instance.generate_game()
    
    current_session["categories"] = categories
    current_session["found_categories"] = []
    current_session["words"] = words

    return JSONResponse({
        "words": words
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)