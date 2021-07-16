from Asphodel import app
from fastapi.responses import FileResponse

@app.get('/file')
def ffile():
    return FileResponse('./assets/thumbnail/FC2-PPV-1500792.jpg')