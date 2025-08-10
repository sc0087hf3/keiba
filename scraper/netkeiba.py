import pymysql
import random
import time
from bs4 import BeautifulSoup
import requests
import re

# ランダムUser-Agentリスト
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
]

DB_CONFIG = {
    'host': 'localhost',
    'user': 'youruser',
    'password': 'yourpassword',
    'db': 'yourdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

def get_html(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    r = requests.get(url, headers=headers, timeout=30)
    r.encoding = r.apparent_encoding
    r.raise_for_status()
    return r.text

def parse_race(html, race_id):
    # ここに前に作ったparse_race関数をコピペしてください
    pass

def insert_races_batch(conn, race_data_list):
    if not race_data_list:
        return
    with conn.cursor() as cursor:
        sql = """
        INSERT INTO races
        (race_id, date, start_time, venue, race_number, distance, track_type, course_shape, track_condition, race_class, num_of_horses)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        start_time=VALUES(start_time),
        venue=VALUES(venue),
        distance=VALUES(distance),
        track_type=VALUES(track_type),
        course_shape=VALUES(course_shape),
        track_condition=VALUES(track_condition),
        race_class=VALUES(race_class),
        num_of_horses=VALUES(num_of_horses)
        """
        params = []
        for race_data in race_data_list:
            params.append((
                race_data['race_id'],
                race_data['date'],
                race_data['start_time'],
                race_data['venue'],
                race_data['race_number'],
                race_data['distance'],
                race_data['track_type'],
                race_data['course_shape'],
                race_data['track_condition'],
                race_data['race_class'],
                race_data['num_of_horses']
            ))
        cursor.executemany(sql, params)
    conn.commit()

def main():
    with open("2022_race_ids.txt", "r", encoding="utf-8") as f:
        race_ids = [line.strip() for line in f if line.strip()]

    conn = pymysql.connect(**DB_CONFIG)

    batch_size = 100
    batch = []

    for idx, race_id in enumerate(race_ids, start=1):
        url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
        try:
            html = get_html(url)
            race_data = parse_race(html, race_id)
            batch.append(race_data)
            print(f"取得成功: {race_id} ({idx}/{len(race_ids)})")
        except Exception as e:
            print(f"[ERROR] race_id {race_id}: {e}")

        if len(batch) >= batch_size:
            insert_races_batch(conn, batch)
            print(f"バッチコミット: {len(batch)}件")
            batch.clear()
            time.sleep(random.uniform(1.0, 3.0))  # マナーで待機

    # 残った分をコミット
    if batch:
        insert_races_batch(conn, batch)
        print(f"最後のバッチコミット: {len(batch)}件")

    conn.close()

if __name__ == "__main__":
    main()
