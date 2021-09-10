from Asphodel import app
import time

from fastapi.exceptions import HTTPException
import starlette


@app.get("/status")
async def status():
    latency = 1000
    time.sleep(latency / 1000)
    return {"detail": "Success!", "latency": latency}
