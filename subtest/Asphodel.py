import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Asphodel API Project", description="It's all yours.", version="alpha 0.1"
)

@app.get("/")
async def root():
    return {"detail": "I'm all yours."}

import os

for root, dirs, files in os.walk("./modules"):
    if not '__pycache__' in root:
        for file in files:
            root = root.replace('\\','/')
            path = f'{root}/{file}'

            module = path.removeprefix('./').replace('/','.').removesuffix('.py')
            print(module)
            __import__(module)

if __name__ == "__main__":
    uvicorn.run("Asphodel:app", host="192.168.0.2", port=7474)