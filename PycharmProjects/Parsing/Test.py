import requests
import json
from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())


def get_anchors(page):
    all_anchors = []
    for i in range(1, page):
        params = {'page': i}
        request = requests.get(url, params)
        soup = BeautifulSoup(request.text, 'html.parser')
        my_anchors = soup.findAll("a", {"class": "doc-label doc-label--link doc-block__doc-label"})
        all_anchors = all_anchors + my_anchors
    return all_anchors


def second_page_info(my_anchors):
    for anchor in my_anchors:
        new_request = requests.get(anchor.get('href'))
        new_soup = BeautifulSoup(new_request.text, 'html.parser')
        new_headers = new_soup.findAll("h1", {"class": "page__title page__title--small"})
        new_anchors = new_soup.findAll("a", {"class": "doc-label doc-label--link list-bar__item"})
        new_divs = new_soup.findAll("div", {"class": "relation-list__value"})
        if len(my_anchors) == 1:
            dic = {
                    'title': str(new_headers[0].get_text()),
                    'link': str(new_anchors[0].get('href')),
                    'data': str(new_divs[-1].get_text()),
                  }
            information['response'].insert(0, dic)
        else:
            information['response'].append(
                {
                    'title': str(new_headers[0].get_text()),
                    'link': str(new_anchors[0].get('href')),
                    'data': str(new_divs[-1].get_text()),
                }
            )
        print(str(new_headers[0].get_text()))
        print(str(new_anchors[0].get('href')))
        print(str(new_divs[-1].get_text()))
        with open('information.json', 'w') as file:
            json.dump(information, file)


def last_data():                   # Берёт последнюю дату со страниц
    first_page = 'http://mep.mosreg.ru/dokumenty/normotvorchestvo?page=1'
    first_page_request = requests.get(first_page)
    first_page_soup = BeautifulSoup(first_page_request.text, 'html.parser')
    first_page_spans = first_page_soup.findAll("span", {"class": "doc-block__date"})
    last_date = str(first_page_spans[0].get_text())
    return last_date


def find_new(static_date):
    date = last_data()
    day, month, year = date[0:2], date[3:5], date[6:10]
    static_day, static_month, static_year = static_date[0:2], static_date[3:5], static_date[6:10]
    if year >= static_year:
        if month >= static_month:
            if day >= static_day:
                a = get_anchors(2)
                need_anchor = []
                need_anchor.append(a[0])
                second_page_info(need_anchor)
                print("it works")
            else:
                print("nothing new")


url = 'http://mep.mosreg.ru/dokumenty/normotvorchestvo/'
information = {}
information['response'] = []
anchors = get_anchors(2)
second_page_info(anchors)
find_new("19.05.2019")

