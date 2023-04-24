import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import os.path
import json

file_dir = os.path.dirname(__file__)

url = "https://ja.wikinews.org/wiki/%E7%89%B9%E5%88%A5:%E3%83%9A%E3%83%BC%E3%82%B8%E4%B8%80%E8%A6%A7"
base_url = "https://ja.wikinews.org"

def get_article_content(article_url):
    response = requests.get(article_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1", {"class": "firstHeading"}).text
    content = "".join([x.text for x in soup.find("div", {"id": "mw-content-text"}).find_all("p")[1:]])
    return title, content.replace("\n", "")

def get_article_urls(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    article_urls = []
    for link in soup.find("ul", {"class": "mw-allpages-chunk"}).find_all("a"):
        href = link.get("href")
        if href and href.startswith("/wiki/") and not href.startswith("/wiki/%E5%88%A5%E7%A8%AE:") and not href.startswith("/wiki/%E5%8D%8A%E9%9A%8E%E5%8F%8A%E3%81%B3%E5%8D%8A%E9%9A%8E%E3%82%92%E5%90%AB%E3%82%80"):
            article_urls.append(base_url + href)
    next_url_cands = soup.find("div", {"class": "mw-allpages-nav"}).find_all("a")
    next_url_cands = [x for x in next_url_cands if "次のページ" in x.text]
    if len(next_url_cands) > 1:
        print(next_url_cands)
        raise AssertionError
    if len(next_url_cands) == 0:
        next_url = None
    else:
        next_url = base_url + next_url_cands[0].get("href")
    return article_urls, next_url

# ページング機能の実装
page_url = url
article_urls = []
while True:
    print("paging for index:", page_url)
    article_urls_new, page_url = get_article_urls(page_url)
    article_urls.extend(article_urls_new)
    if not page_url:
        break
    time.sleep(1)

data_list = []
for article_url in tqdm(article_urls):
    title, content = get_article_content(article_url)
    data_list.append({"instruction": "次のニュース記事にタイトルをつけてください。", "input": content, "output": title, "url": article_url})
    time.sleep(1)

n = len(data_list) // 1000 + 1
for i in range(n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )