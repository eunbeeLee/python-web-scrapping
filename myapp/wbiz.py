import requests
import re
from bs4 import BeautifulSoup

LIMIT = 50

STARTING_BUSINESS_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=1&q_rowPerPage={LIMIT}"
CAPITAL_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=2&q_rowPerPage={LIMIT}"
LEARNING_CENTER_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=3&q_rowPerPage={LIMIT}"
MARKETING_EXPORTING_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=4&q_rowPerPage={LIMIT}"

def get_pages_by_category():
    urls = [STARTING_BUSINESS_URL, CAPITAL_URL, LEARNING_CENTER_URL, MARKETING_EXPORTING_URL]
    extract_board(urls)

def extract_board(urls):
    boards = []
    for url in urls:
        soup = get_soup(url)
        last_page = get_last_page(soup)
        boards.append(extract_wbiz_board(last_page, url))

def get_soup(URL):
    result = requests.get(URL)
    return BeautifulSoup(result.text, "html.parser")

def get_last_page(soup):
    pagination = soup.find("div", {"class":"pagination"})
    page_links = pagination.find_all('a')

    pages = []
    for link in page_links:
        pages.append(int(link.string))
    return pages[-1]

def extract_board(content, url):
    title = content.string.strip()
    link = content.attrs["onclick"].split(";")[0].split("'")[1]
    parent = content.parent
    # parent_content = parent.attrs["contents"]
    return {"title": title, "link": url + f"&bbsCd={link}"}

def extract_wbiz_board(last_page, url):
    for page in range(last_page):
        boards = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(boards.text, "html.parser")
        table_datas = soup.find_all("td", {"class":"tx_l"})

        board = []

        for data in table_datas:
            content = data.find("a", {"class":"contentTip"})
            if content is not None:
                board.append(extract_board(content, url))
        return board



