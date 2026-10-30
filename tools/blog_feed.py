"""네이버 블로그 RSS -> blog.json (홈페이지 '최근 소식' 데이터)."""
import json, re, sys, urllib.request
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

FEED = "https://rss.blog.naver.com/snm_english.xml"
OUT = "blog.json"
LIMIT = 3


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def clean_link(link):
    # 추적 파라미터 제거: ...?fromRss=true&trackingCode=rss
    return re.sub(r"\?.*$", "", link.strip())


def parse(xml):
    items = []
    for it in ET.fromstring(xml).iter("item"):
        get = lambda t: (it.findtext(t) or "").strip()
        items.append({
            "title": get("title"),
            "link": clean_link(get("link")),
            "category": get("category"),
            "date": parsedate_to_datetime(get("pubDate")).strftime("%Y.%m.%d"),
        })
    return items[:LIMIT]


def main():
    posts = parse(fetch(FEED))
    if not posts:
        sys.exit("피드에 글이 없음. 기존 blog.json 유지")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=1)
    print(json.dumps(posts, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
