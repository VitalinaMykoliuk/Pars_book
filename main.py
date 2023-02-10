import requests
from bs4 import BeautifulSoup
import sqlite3


def func():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    query = '''CREATE TABLE IF NOT EXISTS book(
    Title TEXT, 
    Count VARCHAR(20),
    Price TEXT,
    Avtor TEXT
    )'''

    cursor.execute(query)

    url = "https://book24.ua/ua/catalog/letnee_chtenie_po_shkolnoy_programma/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    page_count = int(soup.find("div", class_="nums").find_all("a", class_="dark_link")[-1].text.strip())
    print(f"Всего страниц {page_count}")
    for page in range(1, page_count + 1):
        print(f'[INFO] Обработка {page} страницы')
        url = f"https://book24.ua/ua/catalog/letnee_chtenie_po_shkolnoy_programma/?PAGEN_1={page}"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        items = soup.select(".inner_wrap > .item_info")
        for item in items:
            try:
                title = item.select(".item-title > a > span")
                title = title[0].text
                nal = item.select(".item-stock > span")[1].text.strip()
                price = item.select(".cost > .price_matrix_wrapper > .price > span")[0].text.strip()
                avtor = item.select('.sa_block > .article_block > .muted > a')
                avtor = avtor[0].text if avtor else "Отсутствует автор"

                cursor.execute('INSERT INTO book VALUES(?,?,?,?)', (title, nal, price, avtor))
                db.commit()
            except:
                ValueError


if __name__ == '__main__':
    func()