import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS для мобильного приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-dc5dbf8ef341419897210d6ae9f3ab84")

@app.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    prompt = (
        f"Найди похожие товары по запросу '{query}' на сайтах Ozon, Wildberries, AliExpress, СберМаркет, Яндекс Маркет. "
        "Верни результат в виде массива JSON, где каждый элемент содержит: "
        "'imageUrl' (ссылка на фото), 'title' (название), 'shop' (магазин), 'price' (цена), "
        "'boughtCount' (сколько купили), 'rating' (рейтинг)."
    )
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты агрегатор товаров."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    import json
    try:
        products = json.loads(content)
    except Exception:
        import re
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            products = json.loads(match.group(0))
        else:
            products = []
    return {"products": products}

@app.get("/barcode-to-name")
async def barcode_to_name(barcode: str):
    # Здесь можно реализовать реальное определение названия по штрихкоду через сторонние сервисы
    # Пока просто возвращаем заглушку
    # Например, если штрихкод == "4601234567890", вернуть "Кока-Кола 0.5л"
    if barcode == "4601234567890":
        return "Кока-Кола 0.5л"
    return f"Товар по коду {barcode}"