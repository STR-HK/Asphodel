import requests
import json

from Asphodel import app

@app.get('/discord/avatar/{userid}')
async def discord_avatar(userid: str):
    header = {'authorization':open('./private/discord_token.txt','r',encoding='utf-8').read()}
    req = requests.get('https://discord.com/api/v8/users/{}'.format(userid), headers=header)
    try:
        return {'response':'https://cdn.discordapp.com/avatars/{}/{}.png?size=1024'.format(userid, json.loads(req.content)['avatar'])}
    except:
        return {'response':'Invalid userID'}