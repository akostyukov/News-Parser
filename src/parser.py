from hashlib import md5

import requests
from bs4 import BeautifulSoup

from dateutil.parser import parse


def get_news(html, main_page, last_news):
    soup = BeautifulSoup(html, "html.parser")

    urls = [
        main_page + url.find("a").get("href")[6:]
        for url in soup.findAll("h2")[:2] + soup.findAll("h3")
        if url.find("a").get("href").startswith("/news/")
    ]

    all_news_data = [get_data(get_html(url)) for url in urls]
    fresh_news_data = []

    if last_news:
        for news in all_news_data:
            if md5(news.get("header").encode()).hexdigest() == last_news:
                break
            fresh_news_data.append(news)
        return fresh_news_data

    return all_news_data


def get_html(url):
    return requests.get(url).text


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")

    try:
        category = soup.find("h3").getText()
    except:
        category = "Глас народа"

    header = soup.find("title").getText()
    text = soup.find("div", attrs={"class": "text"}).getText()
    date_time = parse(soup.find("time").get("datetime"))

    return {
        "category": category,
        "header": header,
        "text": text,
        "date_time": date_time,
    }


def parse_pages(last_news=None):
    main_page = "https://www.penzainform.ru/news/"
    news = get_news(get_html(main_page), main_page, last_news)
    return news
