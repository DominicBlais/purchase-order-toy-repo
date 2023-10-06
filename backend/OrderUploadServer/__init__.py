import os
import sys

import uvicorn
import fastapi
import fastapi.responses
import fastapi.staticfiles

tags_metadata = [
    {
        "name": "static",
        "description": "A simple static file service.",
    },
]

app = fastapi.FastAPI(openapi_tags=tags_metadata)
app.mount("/static", fastapi.staticfiles.StaticFiles(directory=(os.path.dirname(__file__) + os.sep + "html")), name="static")

def start(port=8169):
    global app
    uvicorn.run(app, host="127.0.0.1", port=port)

@app.get("/", response_class=fastapi.responses.RedirectResponse, status_code=302, tags=["static"])
async def redirect_static_to_index():
    return "/static/index.html"
