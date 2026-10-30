"""index.html 의 i.imgur.com 이미지를 img/ 로 내려받고 경로를 바꿈.
전부 받아졌을 때만 index.html 을 고침 (하나라도 실패하면 아무것도 안 바꿈)."""
import pathlib, re, sys, urllib.request

HTML = pathlib.Path("index.html")
DIR = pathlib.Path("img")
PAT = re.compile(r"https://i\.imgur\.com/([A-Za-z0-9]+\.(?:png|jpe?g|gif|webp))")


def main():
    html = HTML.read_text(encoding="utf-8")
    names = sorted(set(PAT.findall(html)))
    if not names:
        print("바꿀 이미지 없음"); return
    DIR.mkdir(exist_ok=True)
    for n in names:
        req = urllib.request.Request(f"https://i.imgur.com/{n}", headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        if len(data) < 200:
            sys.exit(f"{n}: 응답이 비정상 ({len(data)}B)")
        (DIR / n).write_bytes(data)
        print(n, len(data))
    HTML.write_text(PAT.sub(r"/img/\1", html), encoding="utf-8")


if __name__ == "__main__":
    main()
