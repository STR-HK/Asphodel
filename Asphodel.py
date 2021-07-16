import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title='Asphodel API Project',
    description='It\'s all yours.',
    version='alpha 0.1'
)

@app.get('/')
async def root():
    return {'response':'I\'m all yours.'}

import os
import importlib

for module in os.listdir('./modules'):
    if module != '__pycache__':
        globals()[module[:-3]] = importlib.import_module('modules.{}'.format(module[:-3]))

if __name__ == "__main__":
    uvicorn.run('Asphodel:app', host="192.168.0.2", port=7474)