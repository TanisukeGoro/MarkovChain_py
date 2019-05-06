import os
import re
import bs4
import requests


def load(page):
    url = f'http://iyashitour.com/meigen/theme/life/{page}'
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def pickup(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    is_meigen = False
    for paragraph in paragraphs:
        text = str(paragraph)
        if text == '<p>\xa0</p>':
            is_meigen = not is_meigen
        elif is_meigen:
            yield text


def parse(html):
    meigens = '\n'.join(pickup(html))
    # bタグの排除
    meigens = re.sub(r'<(/)?\w+>?', '', meigens)
    #「」の排除
    meigens = re.sub(r'(「|」)', '', meigens)
    # 例外の開始文字から始まる文字列を排除
    meigens = re.sub(r'((\(|【|-|※|\s/)(\d|\D)+)?', '', meigens)
    # 改行の排除
    meigens = re.sub(r'\n', '', meigens)
    return meigens


def main():
    with open('meigen.txt', 'a') as f:
        for page in range(1, 16):
            html = load(page)
            meigens = parse(html)
            print(meigens)
            f.write(meigens)

if __name__ == '__main__':
    main()
