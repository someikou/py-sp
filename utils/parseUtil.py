from bs4 import BeautifulSoup
def parseCodeBox (codebox):
    soup = BeautifulSoup(codebox,'lxml')
    titleEle = soup.select('p a')[0]
    price = soup.select('p span')[0].text
    btnEle = soup.select('td div a div')[0]
    data = {
        'title':titleEle.text,
        'titleUrl':titleEle['href'],
        'price':price,
        'btnUrl':btnEle.parent['href']
    }
    return data




