import requests
import hashlib
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

def get_page_hash(user):
    url = f"https://m.fmkorea.com/search.php?mid=stock&category=&search_target=nick_name&search_keyword={user}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    return hashlib.md5(res.text.encode()).hexdigest(), url

seen = load_seen()
for user in TARGET_USERS:
    new_hash, link = get_page_hash(user)
    old_hash = seen.get(user)
    if old_hash and old_hash != new_hash:
        send_telegram(f"📢 펨코 새글 감지\n닉네임: {user}\n{link}")
        print(f"{user}: 변화 감지! 알림 전송")
    else:
        print(f"{user}: 변화 없음")
    seen[user] = new_hash
save_seen(seen)
print("완료")
