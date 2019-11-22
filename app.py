import urllib3
import json
from bs4 import BeautifulSoup

connection_pooling = urllib3.PoolManager()

D_stocks = {}

aditya_stock_req = connection_pooling.request('GET','https://www.valueresearchonline.com/funds/newsnapshot.asp?schemecode=15831')
# aditya_stock_req = urllib3.request('https://www.valueresearchonline.com/funds/newsnapshot.asp?schemecode=1400&utm_source=direct-click&utm_medium=funds&utm_term=aditya+birla&utm_content=Aditya+Birla+SL+Frontline+Equity&utm_campaign=vro-search')

# json_data = json.loads(aditya_stock_req.data.decode('utf-8'))

# aditya_url = urllib3.urlopen()
hdfc_stock_req = connection_pooling.request('GET','https://www.valueresearchonline.com/funds/newsnapshot.asp?schemecode=16109')

soup2 = BeautifulSoup(aditya_stock_req.data,'html.parser')
soup = BeautifulSoup(hdfc_stock_req.data,'html.parser')

# print(soup.prettify())q
all_tables= soup.find_all('table')
D_stocks['aditya_birla'] = {}
# import pdb;pdb.set_trace()
table1 = all_tables[0]
tds_t1 = table1.find_all('td')
assets = tds_t1[3].text.split()
assets_rs = " ".join(assets)
expense = tds_t1[5].text.split()
expense_rs = " ".join(expense)
D_stocks['aditya_birla'][tds_t1[2].text] = assets_rs
D_stocks['aditya_birla'][tds_t1[4].text] = expense_rs

    # print(td.text)
# import pdb;pdb.set_trace()

# headings = []
for tr in all_tables:
    # import pdb;pdb.set_trace()
    l_tr = tr.text.split()
    if 'YTD' in l_tr:
        # print(tr.text)
        # import pdb;pdb.set_trace()
        # print(tr.json())
        th = tr.find_all('th')
        tds = tr.find_all('td')
        for i in range(len(th)):
            D_stocks["aditya_birla"][th[1].text] = tds[1].text
            D_stocks["aditya_birla"][th[4].text] = tds[4].text
        import pdb;pdb.set_trace()
        # for td in tr.find_all("td"):
        #     import pdb;pdb.set_trace()
        #     headings.append(td.b.text.replace('\n', ' ').strip())
        # import pdb;pdb.set_trace()

        # print(headings)


    # print(tr.text)

all_tables_hdfc= soup2.find_all('table')

# import pdb;pdb.set_trace()