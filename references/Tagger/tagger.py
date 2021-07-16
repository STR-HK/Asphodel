import requests
from bs4 import BeautifulSoup
import json

tags = open('helper/tag/tags.txt','r',encoding='utf-8').read().split('\n')

def getData(select):
    url = 'https://ehwiki.org/wiki/{}'.format(select)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    cutted = [{'Name':soup.find('h1', class_='firstHeading').get_text()}]
    contents = soup.find('div',class_='mw-parser-output').find_all('li')
    for content in contents:
        cut = content.get_text().split(': ')
        if cut[0] == 'Type':
            cut = {'Type':cut[1].split(' / ')}
        elif cut[0] == 'Sub-Type':
            cut = {'Sub-Type':cut[1].split(', ')}
        elif cut[0] == 'Description':
            cut = {'Description':cut[1]}
        elif cut[0] == 'Gender':
            cut = {'Gender':cut[1]}
        elif cut[0] == 'Japanese':
            cut = {'Japanese':cut[1]}
        elif cut[0] == 'Slave Tags':
            cut = {'Slave Tags':cut[1].replace(u'\xa0', u' ').split(', ')}
        elif cut[0] == 'Notes':
            cut = {'Notes':cut[1]}
        elif cut[0] == 'Power Requirement':
            cut = {'Power Requirement':cut[1]}
        elif cut[0] == 'Factoid':
            cut = {'Factoid':cut[1]}
        elif cut[0] == 'Examples':
            cut = {'Examples':cut[1].split(', ')}
        elif cut[0] == 'Name Indication':
            cut = {'Name Indication':cut[1]}
        elif cut[0] == 'Japanese Indication':
            cut = {'Japanese Indication':cut[1]}
        elif cut[0] == 'Series':
            cut = {'Series':cut[1]}
        elif cut[0] == 'Viewing':
            cut = {'Viewing':cut[1]}

        # print(cut)

        cutted.append(cut)

        dictionary = {}
        for c in cutted:
            dictionary.update(c)

    return dictionary

togs = list()

for t, tag in enumerate(tags):
    togs.append(getData(tag))
    print(t)

# print(getData(tags[319]))

f = open('result.txt','w',encoding='utf-8')
f.write(json.dumps(togs))
f.close()