import requests
import json

from Asphodel import app

f_read = open("./private/discord_token.txt", "r", encoding="utf-8").read()


@app.get("/discord/avatar/{userid}", tags=["Extractor"])
async def discord_avatar(userid: str):
    header = {"authorization": f_read}
    req = requests.get(
        "https://discord.com/api/v8/users/{}".format(userid), headers=header
    )
    try:
        return {
            "detail": "https://cdn.discordapp.com/avatars/{}/{}.png?size=1024".format(
                userid, json.loads(req.content)["avatar"]
            )
        }
    except:
        return {"detail": "Invalid userID"}
