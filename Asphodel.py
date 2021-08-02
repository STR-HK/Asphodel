import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Asphodel API Project", description="It's all yours.", version="alpha 0.1"
)


@app.get("/")
async def root():
    return {"detail": "I'm all yours."}


import os

for module in os.listdir("./modules"):
    print(module)
    if module != "__pycache__":
        __import__("modules.{}".format(module[:-3]))

# import modules.token

if __name__ == "__main__":
    uvicorn.run("Asphodel:app", host="192.168.0.2", port=7474)
