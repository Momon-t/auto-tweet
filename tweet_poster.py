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
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        schedule = []
        for row in reader:
            dt = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
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
    print(res.status_code, res.text)
    return res.status_code == 200

def main():
    now = get_now_jst().replace(second=0, microsecond=0)
    schedule = load_schedule("schedule.csv")
    for dt, text in schedule:
        dt_jst = pytz.timezone("Asia/Tokyo").localize(dt)
        if now == dt_jst:
            print(f"[INFO] Posting tweet: {text}")
            post_tweet(text)
            break
    else:
        print("No scheduled tweet for now.")

if __name__ == "__main__":
    main()
