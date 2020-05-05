import requests
from bs4 import BeautifulSoup

LIMIT = 50

STARTING_BUSINESS_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=1&q_rowPerPage={LIMIT}"
CAPITAL_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=2&q_rowPerPage={LIMIT}"
LEARNING_CENTER_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=3&q_rowPerPage={LIMIT}"
MARKETING_EXPORTING_URL = f"http://www.wbiz.or.kr/web/bizinfo/BD_index.do?q_mcategory_type=4&q_rowPerPage={LIMIT}"

def get_pages_by_category():
    urls = [STARTING_BUSINESS_URL, CAPITAL_URL, LEARNING_CENTER_URL, MARKETING_EXPORTING_URL]
    return get_boards(urls)

def get_boards(urls):
    boards = []
    for index, url in enumerate(urls):
        soup = get_soup(url)
        last_page = get_last_page(soup)
        boards.append(extract_wbiz_board(last_page, url, index))
    return boards

def get_soup(url):
    result = requests.get(url)
    return BeautifulSoup(result.text, "html.parser")

def get_last_page(soup):
    pagination = soup.find("div", {"class":"paginate"})
    page_links = pagination.find_all('a')

    pages = []
    for link in page_links:
        title = link.attrs['title']
        if title != '다음페이지로 가기' and title != '마지막페이지로 가기':
            pages.append(int(link.string))
    return pages[-1]



def extract_wbiz_board(last_page, url, index):
    board = []
    for page in range(last_page):
        boards = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(boards.text, "html.parser")
        tr_data = soup.find('tbody').find_all("tr")

        category = get_category(index)
        for tr in tr_data:
            td_data = tr.find_all("td")
            if td_data[0].text == '':
                continue
            else:
                board.append({"category": category, "content": extract_information(td_data, url)})

    return board

def get_category(index):
    if index == 0:
        return '창업/보육'
    if index == 1:
        return '자금'
    if index == 2:
        return '교육/일자리'
    if index == 3:
        return '수출'

def extract_information(td_data, url):
    title = td_data[1].string.strip()
    link = td_data[1].next.attrs['onclick'].split(";")[0].split("'")[1]
    team = td_data[2].text
    date = td_data[3].text
    return {'title': title, 'link': url + f'&bbsCd={link}', 'team': team, 'date': date}



