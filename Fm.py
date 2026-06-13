import requests
from bs4 import BeautifulSoup
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "6460142600"
TARGET_USERS = ["노라무"]
SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {}

def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_posts(user):
    url = f"https://m.fmkorea.com/search.php?mid=stock&category=&search_target=nick_name&search_keyword={user}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    posts = []
    for item in soup.select(".li_best2_pic0, .li_best2_pic1"):
        a = item.select_one("a.hx")
        if not a:
            continue
        title = a.get_text(strip=True)
        href = a.get("href", "")
        pid = href.split("/")[-1].split("?")[0]
        if title and pid:
            posts.append({"id": pid, "title": title, "link": "https://www.fmkorea.com" + href})
    return posts

seen = load_seen()
for user in TARGET_USERS:
    posts = get_posts(user)
    user_seen = seen.get(user, [])
    for p in posts:
        if p["id"] not in user_seen:
            send_telegram(f"📢 펨코 새글\n닉네임: {user}\n제목: {p['title']}\n{p['link']}")
            user_seen.append(p["id"])
    seen[user] = user_seen[-50:]
save_seen(seen)
print("완료")
