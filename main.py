from fastapi import FastAPI, Request
import httpx

app = FastAPI()

MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p9ugnp2wopa4yd2g3mbskexbgkgs6770"

@app.post("/")
async def wayforpay_webhook(request: Request):
    data = await request.json()

    # Отправляем данные в Make
    async with httpx.AsyncClient() as client:
        await client.post(MAKE_WEBHOOK_URL, json=data)

    # Возвращаем "OK"
    return "OK"