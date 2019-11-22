import urllib3
from bs4 import BeautifulSoup

connection_pooling = urllib3.PoolManager()

D_stocks = {}
num_funds = input("How many mutual funds you want to compare: " )
urls = input("Enter the urls of mutual funds one by one ")
import pdb;pdb.set_trace()
urls = urls.split()

for url in urls :
    stock_req = connection_pooling.request('GET',url)
    soup = BeautifulSoup(stock_req.data,'html.parser')
    all_tables= soup.find_all('table')
    D_stocks[url] = {}
    table1 = all_tables[0]
    tds_t1 = table1.find_all('td')
    assets = tds_t1[3].text.split()
    assets_rs = " ".join(assets)
    expense = tds_t1[5].text.split()
    expense_rs = " ".join(expense)
    D_stocks[url][tds_t1[2].text] = assets_rs
    D_stocks[url][tds_t1[4].text] = expense_rs

    for tr in all_tables:
        l_tr = tr.text.split()
        if 'YTD' in l_tr:
            th = tr.find_all('th')
            tds = tr.find_all('td')
            for i in range(len(th)):
                D_stocks[url][th[1].text] = tds[1].text
                D_stocks[url][th[4].text] = tds[4].text

print(D_stocks)



# import pdb;pdb.set_trace()
