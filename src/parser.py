import requests
from bs4 import BeautifulSoup


def get_last_news_url(html):
    soup = BeautifulSoup(html, "html.parser")
    url = soup.find("h2").find("a").get("href")

    return url[6:]


def get_html(url):
    return requests.get(url).text


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")

    category = soup.find("h3").getText()
    header = soup.find("title").getText()
    text = soup.find("div", attrs={"class": "text"}).getText()
    date_time = soup.find("time").get("datetime")

    return {
        "category": category,
        "header": header,
        "text": text,
        "date_time": date_time,
    }


def main():
    main_page = "https://www.penzainform.ru/news/"
    news = get_data(get_html(main_page + get_last_news_url(get_html(main_page))))
    print(news)


if __name__ == "__main__":
    main()
