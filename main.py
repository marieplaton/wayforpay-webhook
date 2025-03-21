from fastapi import FastAPI, Request
import logging
import httpx  # Библиотека для отправки HTTP-запросов

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Храним обработанные заказы в памяти (для предотвращения дубликатов)
processed_orders = set()

# 🔹 Вставь сюда свой Webhook Make
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p9ugnp2wopa4yd2g3mbskexbgkgs6770"

@app.post("/")
async def wayforpay_webhook(request: Request):
    try:
        data = await request.json()
        order_ref = data.get("orderReference")  # ID заказа

        # Проверяем, не обрабатывали ли мы этот заказ ранее
        if order_ref in processed_orders:
            logging.warning(f"Duplicate request detected: {order_ref}")
            return {"status": "OK"}  # Отвечаем OK, чтобы WayForPay не ретраил

        logging.info(f"Processing new transaction: {order_ref}")

        # Отправляем данные в Make
        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=data)
            logging.info(f"Response from Make: {response.status_code} {response.text}")

        processed_orders.add(order_ref)  # Запоминаем заказ как обработанный

        logging.info("Sending response: 200 OK")
        return {"status": "OK"}  # WayForPay получит 200 и прекратит ретраи
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return {"status": "error"}, 500  # Ошибка сервера