import json
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sierraloaded.sl"
SIERRALOADED_NEWS_URL = f"{BASE_URL}/news"

html = requests.get(SIERRALOADED_NEWS_URL).text
news_soup = BeautifulSoup(html, "lxml")


def get_news_info(news_element: Any) -> dict[str, Any]:
    news_title = news_element.h1.text
    news_link = news_element.h1.a["href"]
    news_date = news_element.span.text
    news_summary = news_element.p.text

    return {
        "title": news_title,
        "link": news_link,
        "date": news_date,
        "summary": news_summary,
    }


latest_news: Any = news_soup.find("section", class_="category-section-2")
news_list: Any = latest_news.find("div", class_="latest-news-timeline-section")

news_json_array: list[dict[str, Any]] = []

for news in news_list.find_all("article"):
    news_info = get_news_info(news)
    news_json_array.append(news_info)

with Path("news.json") as news_file:
    news_file.write_text(json.dumps(news_json_array))
