import math
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.kabum.com.br/tv'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',

}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('div', id='listingCount').get_text().strip()

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]
print(f'Quantidade total de itens {qtd}.')

ultima_pagina = math.ceil(int(qtd) / 20)
print(f'Quantidade total de páginas {ultima_pagina}.')
dic_produtos = {'marca': [], 'preco': []}

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/tv?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))
    print(f'Captura dos itens da página {i} iniciada.')
    for produto in produtos:
        marca = produto.find('span', class_=re.compile(
            'nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile(
            'priceCard')).get_text().strip()

        #print(marca, preco)
        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)

    print(f'Captura dos itens da página {i} finalizada.')

df = pd.DataFrame(dic_produtos)
df.to_csv('E:\projetos\Python\webscraping\preco_tv_black_friday.csv',
          encoding='utf-8', sep=';')

print("Arquivo CSV criado com sucesso!")
