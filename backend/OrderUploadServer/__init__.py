import os
import signal
import sys

import uvicorn
import fastapi
import fastapi.responses
import fastapi.staticfiles
import pydantic
import sqlite3

tags_metadata = [
    {
        "name": "Static",
        "description": "A simple static file service.",
    },
    {
        "name": "Purchase Orders",
        "description": "A simple API to upload and retrieve purchase order details."
    }
]

class GenericResponseModel(pydantic.BaseModel):
    status: str
    message: str = ""

class OrderDetailsResponseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(protected_namespaces = ())  # to suppress 'model_number' name warning
    order_id: int
    vendor_name: str
    order_date: int
    detail_id: int
    model_number: str
    unit_price: float
    quantity: int
    
class GetOrderDetailsResponseModel(GenericResponseModel):
    details: list[OrderDetailsResponseModel] = []

app = fastapi.FastAPI(openapi_tags=tags_metadata)
app.mount("/static", fastapi.staticfiles.StaticFiles(directory=(os.path.dirname(__file__) + os.sep + "html")), name="static")

conn = None


def initialize_database():
    global conn
    conn = sqlite3.connect(os.path.dirname(__file__) + os.sep + "db" + os.sep + "purchase_orders.sqlite3", isolation_level="DEFERRED")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS po_orders
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_name TEXT,
                order_date REAL,
                upload_date REAL,
                upload_ip_address TEXT);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS po_order_details
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_number TEXT,
                unit_price_cents INTEGER,
                quantity INTEGER,
                order_id INTEGER REFERENCES po_orders(id) ON DELETE CASCADE);""")
    cur.execute("CREATE INDEX IF NOT EXISTS po_order_details_order_index ON po_order_details(order_id);")
    conn.commit()
    cur.close()


def start(port=8169):
    global app
    initialize_database()
    uvicorn.run(app, host="127.0.0.1", port=port)


@app.get("/", response_class=fastapi.responses.RedirectResponse, status_code=302, tags=["Static"])
async def redirect_static_to_index():
    return "/static/index.html"


@app.get("/shutdown")
async def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return "nop"


@app.get("/po/reset_database", tags=["Purchase Orders"])
async def po_reset_database() -> GenericResponseModel:
    try:
        global conn
        cur = conn.cursor()
        cur.execute("DELETE FROM po_order_details;")
        cur.execute("DELETE FROM po_orders;")
        conn.commit()
        cur.close()
    except Exception as ex:
        print(ex)
        return {"status": "error",
                "message": "A server error occurred while resetting the database."}
    return {"status": "success"}


@app.get("/po/get_order_details", tags=["Purchase Orders"])
async def po_get_order_details() -> GetOrderDetailsResponseModel:
    try:
        global conn
        cur = conn.cursor()
        cur.execute("""SELECT orders.id, orders.vendor_name, orders.order_date, details.id, details.unit_price_cents, details.quantity FROM po_order_details details INNER JOIN po_orders orders ON details.order_id=orders.id ORDER BY orders.order_date, details.model_number;""")
        results = []
        for row in cur.fetchall():
            results.append({"order_id": row[0],
                            "vendor_name": row[1],
                            "order_date": round(row[2] * 1000.0),  # JS is milliseconds, Python is float
                            "detail_id": row[3],
                            "model_number": row[4],
                            "unit_price": row[5] * 0.01,  # convert pennies back to USD
                            "quantity": row[6] })
        cur.close()
        return {"status": "success",
                "details": results}
    except Exception as ex:
        return {"status": "error",
                "message": "A server error occured while retrieving order details."}


# note: will need multi-part for file upload
@app.post("/po/upload_order_details")
async def po_upload_order_details() -> GenericResponseModel:
    return {"status": "error",
            "message": "Not implemented."}


