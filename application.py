import requests
from lxml import etree, html
import re
import json 

def dump_to_JSON(Currencies, page):
    
    fileName = f"data{page}.json"
    with open(fileName, "w") as f:
        json.dump(Currencies, f)

def save_to_DB(Currencies):

    pass

@click.command()
@click.option("--Save", default="json", help="Please enter a approach for saving the data : (json/db)")
def doScrape(Save="json", URL="https://coinmarketcap.com/", page_number=1):

    iterator = 1
    resp = requests.get(url=URL, headers={

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })

    print(resp.status_code)

    Currencies = []
    tree = html.fromstring(html=resp.content)
    branch_Master = tree.xpath(
        "//div[@class='tableWrapper___3utdq']/table/tbody")

    while iterator < 11:

        name_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[3]/a/div/div/p/text()")[0].strip()
        price_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[4]/div/a/text()")[0].strip()
        _24h_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[5]/span/text()")[0].strip()
        _7day_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[6]/div/span/text()")[0].strip()
        market_Cap_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[7]/p/text()")[0].strip()
        volume_of_Currency_in_Dollor = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[8]/div/a/p/text()")[0].strip()
        volume_of_Currency_in_Bitcoin = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[8]/div/p/text()")[0].strip()
        circulating_Supply_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[9]/div/div/p/text()")[0].strip()
        img_URL_of_Graph_of_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[{iterator}]/td[10]/a/img[@src]")

        Currency = {

            "Name": name_of_Currency,
            "Price": price_of_Currency,
            "_24h": _24h_of_Currency,
            "_7day": _7day_of_Currency,
            "marketCap": market_Cap_of_Currency,
            "volumeDollor": volume_of_Currency_in_Dollor,
            "volumeBitcoin": volume_of_Currency_in_Bitcoin,
            "circulating": circulating_Supply_of_Currency,
            "imgGraph": img_URL_of_Graph_of_Currency[0].attrib['src'],

        }

        Currencies.append(Currency)
        iterator += 1
    iterator -= 10

    while iterator < 90:
        
        Name_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[@class='sc-14kwl6f-0 fletOv'][{iterator}]/td[3]/span[2]/text()"
        )[0].strip()
        Price_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[@class='sc-14kwl6f-0 fletOv'][{iterator}]/td[4]/span/text()"
        )[0].strip()
        _24_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[@class='sc-14kwl6f-0 fletOv'][{iterator}]/td[5]/span/text()"
        )[0].strip()
        _7day_Currency = tree.xpath(
            f"//div[@class='tableWrapper___3utdq']/table/tbody/tr[@class='sc-14kwl6f-0 fletOv'][{iterator}]/td[6]/span/text()"
        )[0].strip()

        xCurrency = {
            "Name": Name_Currency,
            "Price": Price_Currency,
            "_24": _24_Currency,
            "_7day" : _7day_Currency,
        }

        Currencies.append(xCurrency)

        iterator += 1
        

    print(iterator)
    
    if Save == "json":
        
        dump_to_JSON(Currencies, page_number)
        Currencies.clear()

    elif Save == "db":
        save_to_DB(Currencies)
    

if "__name__" == "__main__":
    
    for page_number in range(1, 38):

        doScrape(URL=f"https://coinmarketcap.com/{page_number}/", page_number=page_number)
