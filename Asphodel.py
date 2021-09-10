import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Asphodel API Project", description="It's all yours.", version="Alpha 0.2"
)

@app.get("/", tags=["Root"])
async def root():
    return {"detail": "I'm all yours."}

import os

from modules.certificate.authorization import auth

for root, dirs, files in os.walk("./modules"):
    if not '__pycache__' in root:
        for file in files:
            root = root.replace('\\','/')
            path = f'{root}/{file}'

            module = path.removeprefix('./').replace('/','.').removesuffix('.py')
            print(module)
            __import__(module)

from uvicorn.supervisors.watchgodreload import CustomWatcher

ignored = {
    "database",
    "generator",
}

class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(ignored)
        super(WatchgodWatcher, self).__init__(*args, **kwargs)

uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher

import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath("/app"))
    uvicorn.run("Asphodel:app", host="192.168.0.2", port=7474, reload=True)