from Asphodel import app
from fastapi.responses import FileResponse
import base64

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, File, UploadFile


@app.get("/file")
def file():
    # with open('./assets/AsphodelWallpaper.png','rb') as img:
    # img_base64 = base64.b64encode(img.read())
    return FileResponse(
        "./assets/taskmgr/[Judas] Kaifuku Jutsushi no Yarinaoshi - S01E01.mkv"
    )
    # return {'detail':img_base64.decode('utf-8')}


some_file_path = "./assets/taskmgr/[Judas] Kaifuku Jutsushi no Yarinaoshi - S01E01.mkv"


@app.get("/ft")
def fileTest():
    def iterfile():

        with open(some_file_path, mode="rb") as file_like:

            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")
