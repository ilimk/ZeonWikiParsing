import requests
import csv
from bs4 import BeautifulSoup

urlWikipedia = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%9A%D0%B8%D1%80%D0%B3%D0%B8%D0%B7%D0%B8%D0%B8'

headersWiki = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

reqWiki = requests.get(urlWikipedia, headers = headersWiki)
srcWiki = reqWiki.text

soup = BeautifulSoup(srcWiki, "lxml")

table_cities = soup.find('table').find('tbody').find_all('tr')

rows = [
    [
        'Ссылка на город', 'Название на русском', 'Название на кыргызском',
        'Ссылка на Флаг Герб', 'Прежние названия', 'Статус города', '2009', '2019', 'Статус', 'Область'
    ]
]


for i in table_cities:
    if i.find_all('td'):
        rows_local = []
        for j in range(len(i.find_all('td'))):
            if j == 0:
                iterr = i.find_all('td')[j]
                rows_local.append('https://ru.wikipedia.org/' + iterr.find('a')['href']) #ссылка на сам город
                rows_local.append(iterr.find('a').text) # название города
            if j == 1:
                rows_local.append(i.find_all('td')[j].text) #KG название города
            if j == 2:
                try:
                    rows_local.append('https://ru.wikipedia.org/' + i.find_all('td')[j].find('a')['href'])
                except:
                    rows_local.append('None')
            if j == 3:
                if i.find_all('td')[j].text == '':
                    rows_local.append('None')
                else:
                    rows_local.append(i.find_all('td')[j].text)
            if j == 4:
                rows_local.append(i.find_all('td')[j].text.rstrip()) #Статус города
            if j == 5:
                rows_local.append(i.find_all('td')[j].text) #2009
            if j == 6:
                rows_local.append(i.find_all('td')[j].text.rstrip()) #2019
            if j == 7:
                rows_local.append(i.find_all('td')[j].text)
            if j == 8:
                rows_local.append(i.find_all('td')[j].text.rstrip())
        rows.append(rows_local)

with open('WikiDataCities.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
