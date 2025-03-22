from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p9ugnp2wopa4yd2g3mbskexbgkgs6770"

# In-memory set to store processed order references
processed_orders = set()

@app.post("/")
async def wayforpay_webhook(request: Request):
    try:
        data = await request.json()

        order_ref = data.get("orderReference")

        if not order_ref:
            return JSONResponse(content={"status": "error", "details": "Missing orderReference"}, status_code=400)

        # Check for duplicates
        if order_ref in processed_orders:
            print(f"Ignored duplicate orderReference: {order_ref}")
            return JSONResponse(content={"status": "duplicate_ignored"}, status_code=200)

        processed_orders.add(order_ref)

        # Log received data
        print("Received data:", data)

        # Send to Make
        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=data)
            print("Response from Make:", response.status_code, response.text)

        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"status": "error", "details": str(e)}, status_code=500)