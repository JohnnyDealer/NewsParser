import requests
import json
from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())
url = 'http://mep.mosreg.ru/dokumenty/normotvorchestvo/'
for i in range(1, 4):
    params = {'page': i}
    r = requests.get(url, params)
    soup = BeautifulSoup(r.text, 'html.parser')
    mya = soup.findAll("a", {"class": "doc-label doc-label--link doc-block__doc-label"})
    # lst = []
    # lst = soup.find_all('a')
    # finall = []
    # data = []
    LinksAndData = {}
    LinksAndData['response'] = []
    for j in mya:
        NewR = requests.get(j.get('href'))
        NewSoup = BeautifulSoup(NewR.text, 'html.parser')
        NewMyA = NewSoup.findAll("a", {"class": "doc-label doc-label--link list-bar__item"})
        NewMyDiv = NewSoup.findAll("div", {"class": "relation-list__value"})
        LinksAndData['response'].append(
            {
                'link': str(NewMyA[0].get('href')),
                'data': str(NewMyDiv[-1].get_text()),
            }
        )
        print(str(NewMyA[0].get('href')))
        print(str(NewMyDiv[-1].get_text()))
        # data.append(NewMyDiv[0].get_text())
        # finall.append(NewMyA[0].get('href'))
    with open('links&data.json', 'w') as file:
        json.dump(LinksAndData, file)
