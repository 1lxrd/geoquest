from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

flags = [
    {"country": "Франция", "img": "https://flagcdn.com/w320/fr.png"},
    {"country": "Германия", "img": "https://flagcdn.com/w320/de.png"},
    {"country": "Италия", "img": "https://flagcdn.com/w320/it.png"},
    {"country": "Япония", "img": "https://flagcdn.com/w320/jp.png"},
    {"country": "Бразилия", "img": "https://flagcdn.com/w320/br.png"},
    {"country": "Канада", "img": "https://flagcdn.com/w320/ca.png"},
    {"country": "Россия", "img": "https://flagcdn.com/w320/ru.png"},
    {"country": "США", "img": "https://flagcdn.com/w320/us.png"},
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (для разработки нормально)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}

@app.get("/get-flag")
def get_flag():
    # 1. Выбираем правильный флаг
    correct_flag = random.choice(flags)

    # 2. Выбираем 3 других неправильных ответа
    wrong_flags = random.sample([f for f in flags if f != correct_flag], 3)

    # 3. Собираем варианты: правильный + неправильные
    options = [correct_flag["country"]] + [flag["country"] for flag in wrong_flags]

    # 4. Перемешиваем варианты
    random.shuffle(options)

    # 5. Возвращаем ответ
    return {
        "img": correct_flag["img"],
        "options": options,
        "answer": correct_flag["country"]  # можно скрыть на фронте, если не нужно подглядывать
    }
