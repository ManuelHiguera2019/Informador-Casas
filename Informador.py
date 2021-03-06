import requests
from bs4 import BeautifulSoup
import json
import datetime

class informador:
    def __init__(self):
        self.lista = []

    def to_json(self):
        with open(datetime.datetime.now().strftime('%Y-%m-%d')+'.json', 'w') as archivo:
            json.dump(self.lista, archivo, sort_keys =False, indent=4)

    def scrapping(self):
        url = "http://aviso.informador.com.mx/index.php/bienes_raices/busqueda?selecciono=1&ciudad_autocomplete=0&colonia_autocomplete=&transaccion=1&tipo=1&consulta=Zona+Metropolitana&precio_min=min&precio_max=max&recamaras_min=0&recamaras_max=0&metros_min=0&metros_max=0&quick-search=Zona+metropolitana-&quick-searchZap=Zapopan-3&quick-searchGdl=Guadalajara-2&quick-searchTlaq=Tlaquepaque-5&quick-searchTon=Tonal%C3%A1-4"
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all(class_='items')
        casas = items[0].find_all('li')

        url2 = "http://aviso.informador.com.mx/index.php/bienes_raices/busqueda?selecciono=0&ciudad_autocomplete=0&colonia_autocomplete=&transaccion=2&tipo=1&consulta=Zona+metropolitana&precio_min=min&precio_max=max&recamaras_min=0&recamaras_max=0&metros_min=0&metros_max=0&quick-search=Zona+metropolitana-&quick-searchZap=Zapopan-3&quick-searchGdl=Guadalajara-2&quick-searchTlaq=Tlaquepaque-5&quick-searchTon=Tonal%C3%A1-4"
        r2 = requests.get(url2)
        r2.encoding = 'utf-8'
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        items2 = soup2.find_all(class_='items')
        casas2 = items2[0].find_all('li')

        self.scrapping_casas(casas, 'Venta')
        self.scrapping_casas(casas2, 'Renta')

        paginas = soup.find(class_="pagination")
        p = paginas.find_all('li')
        urls = []

        paginas2 = soup2.find(class_="pagination")
        p2 = paginas2.find_all('li')
        urls2 = []

        i = 2
        while i < len(p):
            urls.append(p[i].a['href'])
            urls2.append(p2[i].a['href'])
            i = i + 1

        self.scrapping_paginas(urls, 'Venta')
        self.scrapping_paginas(urls2, 'Renta')

    def scrapping_paginas(self, urls, tipo):
        for url in urls:
            r = requests.get(url)
            r.encoding = 'utf-8'
            # print(r.text)

            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(class_='items')
            # print(items)
            casas = items[0].find_all('li')

            self.scrapping_casas(casas, tipo)

    def scrapping_casas(self, casas, tipo):
        for c in casas:
            casa = {
                'tipo': tipo,
                "ubicacion": c.find_all(class_='location')[0].text,
                "titulo": c.a.text,
                "precio": c.h5.text,
                "descripcion": c.p.text,
                "recamaras": c.find(class_='info-rec').text,
                "m2": c.find(class_='info-m2').text,
                "m2_2": c.find(class_='info-m2-2').text,
                "wc": c.find(class_='info-wc').text,
                "cars": c.find(class_='info-cars').text,
                "colonia": c.find(class_='info-gps').contents[1],
                "imgs": ['http:' + i['src'] for i in c.find_all('img')]
            }
            self.lista.append(casa)