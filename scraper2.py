import requests
from bs4 import BeautifulSoup

url = "https://db.netkeiba.com/horse/2022109143"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding

print("Status code:", response.status_code)
print(response.text[:500])  # HTMLの一部を確認

soup = BeautifulSoup(response.text, "html.parser")

if soup.title:
    print("Title:", soup.title.string)
else:
    print("Titleタグが見つかりません")
