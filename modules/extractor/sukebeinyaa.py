from typing import Optional
import requests
from bs4 import BeautifulSoup


from Asphodel import app


@app.get('/nyaa/search', tags=["Extractor"])
def nyaa(query : str, trusted : Optional[bool] = False):
    return sukebei_nyaa_search(site='nyaa', query=query, trusted=trusted)

    
@app.get('/sukebei/search', tags=["Extractor"])
def sukebei(query : str, trusted : Optional[bool] = False):
    return sukebei_nyaa_search(site='sukebei', query=query, trusted=trusted)


def sukebei_nyaa_search(site, query, trusted):
    query = query.replace(' ', '+')
    if site == 'nyaa':
        url = f'https://nyaa.si/?f=2&q={query}' if trusted else f'https://nyaa.si/?f=0&q={query}'
    elif site == 'sukebei':
        url = f'https://sukebei.nyaa.si/?f=2&q={query}' if trusted else f'https://sukebei.nyaa.si/?f=0&q={query}'

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")

    tablediv = soup.find('div', class_='table-responsive')
    table = tablediv.find('table', class_='table')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')

    results = []

    for tr in trs:
        tds = tr.find_all('td')

        Category = tds[0].find('a')['title']
        Name = tds[1].find_all('a')[-1]['title']
        Link = tds[2].find_all('a')[-1]['href']
        Size = tds[3].get_text()
        Date = tds[4].get_text()
        Seeders = tds[5].get_text()
        Leachers = tds[6].get_text()
        Completed_downloads = tds[7].get_text()

        result = {
            'Category' : Category,
            'Name' : Name,
            'Link' : Link,
            'Size' : Size,
            'Date' : Date,
            'Seeders' : Seeders,
            'Leachers' : Leachers,
            'Completed_downloads' : Completed_downloads
        }

        results.append(result)

    return results