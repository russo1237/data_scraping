import urllib3
from bs4 import BeautifulSoup
import xlsxwriter

connection_pooling = urllib3.PoolManager()

D_stocks = {}
urls = []
input_file = open("stocks_url_list.txt")
for line in input_file:
    urls.append(line)

for url in urls :
    stock_req = connection_pooling.request('GET',url)
    soup = BeautifulSoup(stock_req.data,'html.parser')
    all_tables= soup.find_all('table')
    title_name = soup.find_all('title')
    name = title_name[0].text
    D_stocks[url] = {}
    D_stocks[url]["Name"] = name
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
                D_stocks[url][th[5].text] = tds[5].text
                D_stocks[url][th[6].text] = tds[6].text
                D_stocks[url][th[7].text] = tds[7].text

print(D_stocks)


workbook = xlsxwriter.Workbook('Report.xlsx')
report = workbook.add_worksheet()
cell_format = workbook.add_format({'bold': True,'align': 'center','fg_color': 'orange',    'border': 1,
})
cell_format_1 = workbook.add_format({'bold': True,'align': 'center','fg_color': 'yellow',    'border': 1,
})

cell_format_normal = workbook.add_format({'align': 'center'})
row = 3
col = 0
L_index = ["Name of Fund", "Assets", "Expense ratio", "Fund YTD", "Fund 1yr", "Fund 3 yr", "Fund 5 yr", "Fund 10 yr"]
row = row + 2
report.set_column(0,0,25)
report.set_column(1,1,31)
report.set_column(2,2,24)
report.set_column(3,3,12)
report.set_column(4,4,12)
report.set_column(5,5,12)
report.set_column(6,6,12)
report.set_column(7,7,12)
report.merge_range(3,3,3,6,"Analysis of Funds", cell_format_1)

for column in L_index :
    report.write(row, col, column, cell_format)
    col = col + 1

row = row +1
col = 0
for stock in D_stocks:
    report.write(row,col,D_stocks[stock]["Name"])
    report.write(row,col+1,D_stocks[stock]["Assets:"])
    report.write(row,col+2,D_stocks[stock]["Expense:"])
    report.write(row,col+3,D_stocks[stock]["YTD"],cell_format_normal)
    report.write(row,col+4,D_stocks[stock]["1-Year"],cell_format_normal)
    report.write(row,col+5,D_stocks[stock]["3-Year"],cell_format_normal)
    report.write(row,col+6,D_stocks[stock]["5-Year"],cell_format_normal)
    report.write(row,col+7,D_stocks[stock]["10-Year"],cell_format_normal)
    row = row+1

workbook.close()
