import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


html = "https://en.wikipedia.org/wiki/List_of_Unified_Modeling_Language_tools"


def steal_tables(url):
    s_tables = []
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', 'wikitable')
    for table in tables:
        s_table = []
        for row in table.find_all('tr', 'sortbottom'):
            row.decompose()
        rows = table.find_all('tr')
        for row in rows:
            s_row = []
            for cell in row.find_all(['td', 'th']):
                try:
                    cell.sup.decompose()
                except AttributeError:
                    pass
                s_cell = cell.get_text()
                s_row.append(s_cell)
            s_table.append(s_row)
        s_tables.append(s_table)
    return s_tables


def get_keys(table):
    keys = set()
    for key in table:
        keys.add(str.lower(key[0]))
    return keys


def joining_tables(tables):
    fin_table = []
    all_keys = set()
    for table in tables:
        all_keys.update(get_keys(table))
    for key in all_keys:
        fin_table.append([key])
    for table in tables:
        table_len = len(table[0])-1
        not_in_table = all_keys.difference(get_keys(table))
        for row in fin_table:
            if row[0] in not_in_table:
                row.extend([None]*table_len)
            for item in table:
                if str.lower(item[0]) == row[0]:
                    row.extend(item[1:])
    return fin_table

tables = steal_tables(html)

table = joining_tables(tables)

outfile = open('table.csv', 'w', encoding='utf-8')
writer = csv.writer(outfile)
for row in table:
    writer.writerow(row)
outfile.close()