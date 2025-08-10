import requests
from bs4 import BeautifulSoup
import random
import re
import json  # ★ 追加

# ランダムUser-Agentリスト
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
]

def get_html(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = res.apparent_encoding  # ★ 文字化け防止
    res.raise_for_status()
    return res.text

def parse_race(html, race_id):
    soup = BeautifulSoup(html, "html.parser")

    # meta description から開催日・競馬場・レース番号取得
    meta_tag = soup.select_one('meta[name="description"]')
    meta_desc = meta_tag["content"] if (meta_tag and meta_tag.has_attr("content")) else ""

    # 開催日
    race_date = None
    date_match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", meta_desc)
    if date_match:
        year, month, day = date_match.groups()
        race_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    # 競馬場とレース番号
    venue, race_number = None, None
    venue_match = re.search(r"\s([^\d]+?)(\d+)R", meta_desc)
    if venue_match:
        venue = venue_match.group(1).strip()
        race_number = int(venue_match.group(2))

    # レースデータ01
    race_data01_tag = soup.select_one(".RaceData01")
    race_data01 = race_data01_tag.get_text(" ", strip=True) if race_data01_tag else ""

    start_time = None
    start_time_match = re.search(r"(\d{1,2}:\d{2})発走", race_data01)
    if start_time_match:
        start_time = start_time_match.group(1)

    distance = None
    dist_match = re.search(r"(\d+)m", race_data01)
    if dist_match:
        distance = int(dist_match.group(1))

    if "芝" in race_data01:
        track_type = "芝"
    elif "ダ" in race_data01 or "ダート" in race_data01:
        track_type = "ダート"
    elif "障" in race_data01:
        track_type = "障害"
    else:
        track_type = None

    course_shape = None
    course_shape_match = re.search(r"\(([^)]+)\)", race_data01)
    if course_shape_match:
        course_shape = course_shape_match.group(1).replace('\xa0', ' ').strip()

    weather = None
    weather_match = re.search(r"天候:([^\s/]+)", race_data01)
    if weather_match:
        weather = weather_match.group(1)

    track_condition = None
    track_cond_match = re.search(r"馬場:([^\s/]+)", race_data01)
    if track_cond_match:
        track_condition = track_cond_match.group(1)

    # レースデータ02
    race_data02_spans = [x.get_text(strip=True) for x in soup.select(".RaceData02 span") if x.get_text(strip=True)]
    num_of_horses = None
    for text in race_data02_spans:
        if "頭" in text:
            num_of_horses = int(text.replace("頭", ""))
            break

    race_class = None
    for text in race_data02_spans:
        if "G" in text or "新馬" in text or "未勝利" in text or "オープン" in text:
            race_class = text
            break

    return {
        "race_id": race_id,
        "date": race_date,
        "start_time": start_time,
        "venue": venue,
        "race_number": race_number,
        "distance": distance,
        "track_type": track_type,
        "course_shape": course_shape,
        "track_condition": track_condition,
        "race_class": race_class,
        "num_of_horses": num_of_horses,
        "weather": weather
    }

if __name__ == "__main__":
    all_races = []  # ★ 結果をまとめるリスト

    with open("2022_race_ids.txt", "r") as f:
        race_ids = [line.strip() for line in f if line.strip()]

    for race_id in race_ids:
        try:
            url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
            html = get_html(url)
            race_info = parse_race(html, race_id)
            all_races.append(race_info)  # ★ 追加
            print(race_info)
        except Exception as e:
            print(f"[ERROR] {race_id}: {e}")

    # ★ JSONファイルに出力
    with open("race_2022_results.json", "w", encoding="utf-8") as jf:
        json.dump(all_races, jf, ensure_ascii=False, indent=2)

    print("✅ JSONファイル 'race_results.json' に保存しました。")
