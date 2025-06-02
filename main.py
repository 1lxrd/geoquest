from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

flags = [
    {"country": "Францiя", "img": "https://flagcdn.com/w320/fr.png"},
    {"country": "Нiмеччина", "img": "https://flagcdn.com/w320/de.png"},
    {"country": "Iталiя", "img": "https://flagcdn.com/w320/it.png"},
    {"country": "Японiя", "img": "https://flagcdn.com/w320/jp.png"},
    {"country": "Бразилiя", "img": "https://flagcdn.com/w320/br.png"},
    {"country": "Канада", "img": "https://flagcdn.com/w320/ca.png"},
    {"country": "США", "img": "https://flagcdn.com/w320/us.png"},
    {"country": "Велика Британiя", "img": "https://flagcdn.com/w320/gb.png"},
    {"country": "Австралiя", "img": "https://flagcdn.com/w320/au.png"},
    {"country": "Китай", "img": "https://flagcdn.com/w320/cn.png"},
    {"country": "Iндiя", "img": "https://flagcdn.com/w320/in.png"},
    {"country": "Пiвденна Корея", "img": "https://flagcdn.com/w320/kr.png"},
    {"country": "Мексика", "img": "https://flagcdn.com/w320/mx.png"},
    {"country": "Аргентина", "img": "https://flagcdn.com/w320/ar.png"},
    {"country": "Швецiя", "img": "https://flagcdn.com/w320/se.png"},
    {"country": "Норвегiя", "img": "https://flagcdn.com/w320/no.png"},
    {"country": "Фiнляндія", "img": "https://flagcdn.com/w320/fi.png"},
    {"country": "Туреччина", "img": "https://flagcdn.com/w320/tr.png"},
    {"country": "Єгипет", "img": "https://flagcdn.com/w320/eg.png"},
    {"country": "Польща", "img": "https://flagcdn.com/w320/pl.png"},
    {"country": "Грецiя", "img": "https://flagcdn.com/w320/gr.png"}
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "answer": correct_flag["country"]
    }
