import csv
import datetime
import os
import pytz
import requests
from requests_oauthlib import OAuth1

API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

def load_schedule(filename):
    jst = pytz.timezone("Asia/Tokyo")
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        schedule = []
        for row in reader:
            dt = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
            if dt.tzinfo is None:
                dt = jst.localize(dt)
            schedule.append((dt, row["text"]))
        return schedule

def get_now_jst():
    utc_now = datetime.datetime.utcnow()
    jst = pytz.timezone("Asia/Tokyo")
    return utc_now.replace(tzinfo=pytz.utc).astimezone(jst)

def post_tweet(text):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    res = requests.post(url, auth=auth, data={"status": text})
    print(f"[DEBUG] Twitter API レスポンスコード: {res.status_code}")
    print(f"[DEBUG] Twitter API レスポンス内容: {res.text}")
    return res.status_code == 200

def main():
    now = get_now_jst().replace(second=0, microsecond=0)
    schedule = load_schedule("schedule.csv")
    for dt, text in schedule:
        dt_jst = dt.astimezone(pytz.timezone("Asia/Tokyo"))
        delta = (now - dt_jst).total_seconds()

        print(f"[DEBUG] 現在のJST時刻: {now}")
        print(f"[DEBUG] スケジュール上の投稿時刻: {dt_jst}")
        print(f"[DEBUG] 差分（秒）: {delta}")

        if 0 <= delta <= 300:  # 現在時刻がスケジュール時刻以上かつ5分以内
            print(f"[INFO] 投稿を実行します: {text}")
            post_tweet(text)
            break
    else:
        print("No scheduled tweet for now.")

if __name__ == "__main__":
    main()
