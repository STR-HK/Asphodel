import requests
from bs4 import BeautifulSoup

from Asphodel import app


@app.get("/torrent/search/{query}")
async def torrent_search(query: str):
    if query == None or query == "":
        return {"response": "No query"}
    return {"detail": limetorrent_simple_search(query)}


def limetorrent_simple_search(query):
    res = requests.get("https://www.limetorrents.pro/search/all/{}".format(query))
    soup = BeautifulSoup(res.content, "lxml")
    table = soup.find("table", class_="table2")
    try:
        trs = table.find_all("tr")[1:]
    except:
        return {"detail": "No Result"}
    returns = []
    for tr in trs:
        try:
            name = tr.find("div", class_="tt-name").get_text()
            link = "https://www.limetorrents.pro{}".format(
                tr.find("div", class_="tt-name").find_all("a")[-1]["href"]
            )
            added = tr.find_all("td", class_="tdnormal")[0].get_text()
            size = tr.find_all("td", class_="tdnormal")[1].get_text()
            seed = tr.find("td", class_="tdseed").get_text()
            leech = tr.find("td", class_="tdleech").get_text()
            health = tr.find("td", class_="tdright").find("div").get("class")[0][-1]
            returns.append(
                {
                    "name": name,
                    "link": link,
                    "added": added,
                    "size": size,
                    "seed": seed,
                    "leech": leech,
                    "health": health,
                }
            )
        except:
            continue
    if returns == []:
        return {"detail": "No Result"}
    return returns
