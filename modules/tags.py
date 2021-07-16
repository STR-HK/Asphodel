import asyncio
from Asphodel import app

f = open('./assets/tags/Tags.txt','r',encoding='utf-8').read()
import json
Tags = json.loads(f)
Names = list()
for tag in Tags:
    Names.append(tag['Name'])

# @app.get('/tags/autocomplete/{fewletter}')
# async def tags_autocomplete(fewletter: str):
#     result = list()
#     for Name in Names:
#         if Name[:len(fewletter)] == fewletter:
#             result.append(Name)
#     return result

@app.get('/tags/list')
async def tags_list():
    return Tags

@app.get('/tags/detail/{name}')
async def tags_detail(name: str):
    for N, Name in enumerate(Names):
        if Name == name:
            return Tags[N]

@app.get('/tags/namelist')
async def tags_namelist():
    return Names