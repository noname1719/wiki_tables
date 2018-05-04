import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


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



def joining_tables(tables):
    pass


def show_result(table):
    pass


def main():
    print('enter url')
    url = input()
    print('stealing tables')
    tables = steal_tables(url)
    print('joining tables')
    table = joining_tables(tables)
    print('complete')
    show_result(table)


if __name__ == "__main__":
    main()