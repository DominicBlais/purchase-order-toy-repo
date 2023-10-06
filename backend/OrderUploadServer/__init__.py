import os
import signal

import uvicorn
import fastapi
import fastapi.responses
import fastapi.staticfiles
import pydantic

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
    model_number: str
    unit_price: float
    quantity: int
    
class GetOrderDetailsResponseModel(GenericResponseModel):
    details: list[OrderDetailsResponseModel] = []

app = fastapi.FastAPI(openapi_tags=tags_metadata)
app.mount("/static", fastapi.staticfiles.StaticFiles(directory=(os.path.dirname(__file__) + os.sep + "html")), name="static")


def start(port=8169):
    global app
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
    return {"status": "error",
            "message": "Not implemented."}


@app.get("/po/get_order_details", tags=["Purchase Orders"])
async def po_get_order_details() -> GetOrderDetailsResponseModel:
    return {"status": "error",
            "message": "Not implemented."}

# note: will need multi-part for file upload
@app.post("/po/upload_order_details")
async def po_upload_order_details() -> GenericResponseModel:
    return {"status": "error",
            "message": "Not implemented."}


