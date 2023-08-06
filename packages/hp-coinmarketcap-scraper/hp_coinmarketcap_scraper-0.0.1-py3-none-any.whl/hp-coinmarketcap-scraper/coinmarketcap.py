import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import json
from optparse import OptionParser
from colorama import *
init(autoreset=True)

usage = "usage: %prog --download-logos"
parser = OptionParser(usage=usage)

parser.add_option("-d", "--download-logos", dest="logo",
        action="store_true",
        default=False,
        help="download the top 10 coinmarketcap.com coin logos")

(options , args) = parser.parse_args()

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result , "html.parser")

tbody = doc.tbody
trs = tbody.contents
data = [{},{},{},{},{},{},{},{},{},{}]
listname = []
listsymbol = []
listprice = []
os.makedirs("logos",exist_ok=True)
os.chdir("logos")
for tr in trs[:10]:
    name , price = tr.contents[2:4]
    symbol = name.find('p' , class_="sc-e225a64a-0 dfeAJi coin-item-symbol")
    if options.logo == True:
        logo = tr.find("img", class_="coin-logo")
        filename = f"logo-{symbol.string}.jpg"
        reqlogo = requests.get(logo['src'])
        print(f'{Fore.LIGHTGREEN_EX} downloaded {symbol.string} LOGO successfully')
        with open(filename , 'wb') as f:
            f.write(reqlogo.content)
        f.close()
    listsymbol.append(symbol.string)
    listname.append(name.p.string)
    listprice.append(price.a.string)
    print(f"{Fore.LIGHTGREEN_EX} {name.p.string} coin data extracted successfully")
    for i in range(10):
        try:
            data[i]['name'] = listname[i]
            data[i]['symbol'] = listsymbol[i]
            data[i]['price'] = listprice[i]
        except:
            pass
    



os.chdir('../')
os.makedirs('data',exist_ok=True)
os.chdir('data')
with open('data.json' , 'w') as f:
    json.dump(data , f ,ensure_ascii=False)