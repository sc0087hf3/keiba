import random
import time
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
]

def get_inner_text_or_none(element):
    if element is None:
        return ""
    try:
        return element.inner_text().strip()
    except Exception:
        return ""

def main():
    start_time = time.time()

    url_login = "https://regist.netkeiba.com/account/?pid=login"  # ログインページURLを正確にセットしてください
    race_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202504020609&rf=race_list"
    username = "gangshishidao@gmail.com"  # ここにログインID
    password = "yajima244"           # ここにパスワード

    user_agent = random.choice(USER_AGENTS)
    print(f"使用User-Agent: {user_agent}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # ログイン処理
        page.goto(url_login)
        page.wait_for_selector('input[name="pswd"]', timeout=30000)
        page.fill('input[name="login_id"]', username)
        page.fill('input[name="pswd"]', password)
        page.click('input[type="image"]')  # ログインボタンが画像タイプの場合の例
        page.wait_for_load_state('networkidle')  # ログイン後の読み込み完了を待つ

        print("ログインしてページ取得完了")

        # レースページに移動
        page.goto(race_url)
        page.wait_for_selector("table.Shutuba_Table tbody tr.HorseList", timeout=30000)
        page.wait_for_timeout(3000)  # Ajax等の読み込み待ち

        # オッズ更新時刻の取得
        official_time_elem = page.query_selector("#official_time")
        official_time = official_time_elem.inner_text().strip() if official_time_elem else ""
        print(f"オッズ更新時刻: {official_time}")

        rows = page.query_selector_all("table.Shutuba_Table tbody tr.HorseList")
        print(f"取得した行数: {len(rows)}")

        for idx, row in enumerate(rows):
            cells = row.query_selector_all("td")
            if len(cells) != 15:
                print(f"行 {idx} は列数が15ではないためスキップします。")
                continue

            waku = get_inner_text_or_none(cells[0])
            umaban = get_inner_text_or_none(cells[1])
            horse_name = get_inner_text_or_none(row.query_selector("td.HorseInfo span.HorseName a"))
            seirei = get_inner_text_or_none(row.query_selector("td.Barei"))
            kinryo = get_inner_text_or_none(row.query_selector("td:nth-child(6)"))
            jockey = get_inner_text_or_none(row.query_selector("td.Jockey a"))
            trainer = get_inner_text_or_none(row.query_selector("td.Trainer a"))
            weight = get_inner_text_or_none(row.query_selector("td.Weight"))
            odds = get_inner_text_or_none(row.query_selector("td.Txt_R.Popular span"))
            ninki = get_inner_text_or_none(row.query_selector("td.Popular_Ninki span"))

            print(f"枠:{waku}, 馬番:{umaban}, 馬名:{horse_name}, 性齢:{seirei}, 斤量:{kinryo}, 騎手:{jockey}, 厩舎:{trainer}, 馬体重:{weight}, オッズ:{odds}, 人気:{ninki}")

        browser.close()

    elapsed = time.time() - start_time
    print(f"処理時間: {elapsed:.2f}秒")

if __name__ == "__main__":
    main()
