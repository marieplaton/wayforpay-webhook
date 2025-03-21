from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import httpx  # Используем для отправки HTTP-запросов

app = FastAPI()

# Укажи свой Webhook Make (замени ссылку на актуальную)
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p9ugnp2wopa4yd2g3mbskexbgkgs6770"

@app.post("/")
async def webhook(request: Request):
    try:
        # Проверяем, есть ли тело запроса
        if request.headers.get("content-length") == "0":
            return JSONResponse(content={"error": "Empty request body"}, status_code=400)

        data = await request.json()

        # Логируем полученные данные
        print("Received data:", data)

        # Отправляем данные в Make Webhook
        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=data)

        # Логируем ответ Make для проверки
        print("Response from Make:", response.status_code, response.text)

        # Возвращаем 200 OK после обработки
        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)