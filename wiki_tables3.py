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


def get_keys(tables):
    fin_table = set()
    keys = []
    for table in tables:
        for row in table:
            fin_table.add(str.lower(row[0]))
    for key in fin_table:
        i = [key]
        keys.append(i)
    return keys


def joining_tables(tables):
    keys = get_keys(tables)
    for table in tables:
        keys_len = len(keys[0])
        table_len = len(table[0]) - 1
        fin_len = keys_len + table_len
        for key in keys:
            for row in table:
                if key[0] == str.lower(row[0]):
                    key.extend(row[1:])
            if len(key) < fin_len:
                for i in range(table_len - 1):
                    key.extend(' ')
    return keys




tables = steal_tables(html)

fin = joining_tables(tables)
for i in fin:
    print(i)