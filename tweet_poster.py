import os
import requests
from requests_oauthlib import OAuth1

# 環境変数からTwitter API認証情報を取得
API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

def post_tweet(text):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    res = requests.post(url, auth=auth, data={"status": text})

    print(f"[DEBUG] HTTP ステータスコード: {res.status_code}")
    print(f"[DEBUG] レスポンス内容: {res.text}")

    if res.status_code == 200:
        print("✅ 投稿成功！")
    else:
        print("❌ 投稿失敗。")

if __name__ == "__main__":
    post_tweet("テスト投稿です（このツイートが表示されれば成功）")
