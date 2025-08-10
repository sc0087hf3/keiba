from playwright.sync_api import sync_playwright
import re
import random
import time

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
]

def get_race_ids_by_date(playwright, date_str, blocked_uas=set()):
    for attempt in range(len(user_agents)):
        ua = random.choice([ua for ua in user_agents if ua not in blocked_uas])
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=ua, viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        url = f"https://race.netkeiba.com/top/race_list.html?kaisai_date={date_str}"

        try:
            page.goto(url, timeout=60000)
            page.wait_for_selector("a[href*='result.html?race_id=']", timeout=10000)
        except Exception as e:
            print(f"[{date_str}] User-Agentが原因かも: {ua}")
            print(f"エラー: {e}")
            blocked_uas.add(ua)
            browser.close()
            if len(blocked_uas) == len(user_agents):
                raise Exception("全てのUser-Agentがアクセス拒否されています。処理を中断します。")
            continue

        race_ids = []
        links = page.query_selector_all("a[href*='result.html?race_id=']")
        for link in links:
            href = link.get_attribute("href")
            match = re.search(r"race_id=(\d+)", href)
            if match:
                race_id = match.group(1)
                if race_id not in race_ids:
                    race_ids.append(race_id)

        browser.close()
        return race_ids

    # ここまで来たら全UA試してもだめだった場合
    return []

def get_race_ids_by_date_with_retry(playwright, date_str, max_retry=3):
    blocked_uas = set()
    for attempt in range(max_retry):
        try:
            return get_race_ids_by_date(playwright, date_str, blocked_uas)
        except Exception as e:
            print(f"[Retry {attempt+1}/{max_retry}] {date_str} でエラー発生: {e}")
            time.sleep(5)
    print(f"[Error] {date_str} の取得に失敗しました。スキップします。")
    return []

if __name__ == "__main__":
    input_file = "2022.txt"
    output_file = "2022_race_ids.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        dates = [line.strip() for line in f if line.strip()]

    all_ids = []

    with sync_playwright() as p:
        for date_str in dates:
            ids = get_race_ids_by_date_with_retry(p, date_str)
            all_ids.extend(ids)
            print(f"{date_str}: {len(ids)}件")
            time.sleep(random.uniform(1.5, 3.5))

    all_ids = sorted(set(all_ids))

    with open(output_file, "w", encoding="utf-8") as f:
        for rid in all_ids:
            f.write(rid + "\n")

    print(f"合計 {len(all_ids)} 件のrace_idを {output_file} に保存したでござる。")
