import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from time import sleep
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


df = pd.read_csv('Projeto2\precos.csv')

def get_amazon(x):
        
    url = x
    # http://www.networkinghowtos.com/howto/common-user-agent-list/
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept-Language': 'en-US, en;q=0.5'})


    # Vamos mandar um 'GET request' para a URL, para nos pegarmos o HTML
    response = requests.get(url, headers= HEADERS)
    html_content = response.text

    # BeautifulSoup object, ele que vai receber o html que pegamos
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extrair o titulo
    product_title = soup.find('span', attrs={'id': 'productTitle'}).get_text().strip()

    # Preço
    price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()

    # Colocando a data tb, ninguem é de ferro
    now = datetime.datetime.now()
    
    # Salvando no nosso dataframe do pandinhas
    new_row = {'Titulo': product_title, 'Preço': price, 'Data_request': now}
    global df
    df = df.append(new_row, ignore_index=True)

urls = pd.read_csv('Projeto2/urls.csv')
urls_1 = urls.iloc[:,0]

for i in urls_1:
    get_amazon(i)

df.to_csv('Projeto2\precos.csv', mode='a', index=False, header=False)