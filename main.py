from fastapi import FastAPI, Request
import logging
import httpx

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Храним обработанные заказы (предотвращает дубликаты)
processed_orders = set()

# 🔹 Вставь сюда свой Webhook Make
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p9ugnp2wopa4yd2g3mbskexbgkgs6770"

@app.post("/")
async def wayforpay_webhook(request: Request):
    try:
        data = await request.json()
        order_ref = data.get("orderReference")  # ID заказа

        if not order_ref:
            logging.error("Missing orderReference in request data")
            return {"status": "error", "message": "Missing orderReference"}, 400

        if order_ref in processed_orders:
            logging.warning(f"Duplicate request detected: {order_ref}")
            return {"status": "OK"}  # Отвечаем OK, чтобы WayForPay не ретраил

        logging.info(f"Processing new transaction: {order_ref}")

        # ✅ Отправляем данные в Make в правильном JSON-формате
        payload = {"json": data}  # Теперь Make получит объект в `json`

        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=payload)
            logging.info(f"Response from Make: {response.status_code} {response.text}")

        processed_orders.add(order_ref)

        return {"status": "OK"}  # WayForPay прекратит повторные отправки
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return {"status": "error", "message": str(e)}, 500