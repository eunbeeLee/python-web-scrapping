import requests
import re
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_searchKey=&q_searchVal=&q_mcategory_type=1&q_rowPerPage={LIMIT}"

def extract_wbiz_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class":"paginate"})

    links = pagination.find_all('a')
    pages = []
    for link in links:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page
def extract_board(content):
    title = content.string.strip()
    link = content.attrs["onclick"].split(";")[0].split("'")[1]
    parent = content.parent
    # parent_content = parent.attrs["contents"]
    return {"title": title, "link": URL + f"&bbsCd={link}"}

def extract_wbiz_board(last_page):
    for page in range(last_page):
        boards = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(boards.text, "html.parser")
        table_datas = soup.find_all("td", {"class":"tx_l"})

        boards = []
        for data in table_datas:
            content = data.find("a", {"class":"contentTip"})
            if content is not None:
                boards.append(extract_board(content))
        return boards



