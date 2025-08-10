import os  # ← 追加
import random
import time
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

# ▼ 追加: 失敗したURLを記録する関数
def log_failed_url(url, log_file="failed_urls.txt"):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(url + "\n")
    print(f"[ERROR] 失敗したURLをログに記録: {url}")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
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
    
    url_login = "https://regist.netkeiba.com/account/?pid=login"
    race_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202507030406"
    username = "gangshishidao@gmail.com"
    password = "yajima244"
    
    user_agent = random.choice(USER_AGENTS)
    print(f"使用User-Agent: {user_agent}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        try:
            # ログイン処理
            page.goto(url_login)
            page.wait_for_selector('input[name="pswd"]', timeout=30000)
            page.fill('input[name="login_id"]', username)
            page.fill('input[name="pswd"]', password)
            page.click('input[type="image"]')
            page.wait_for_load_state('networkidle')
            print("ログインしてページ取得完了")

            # ▼ TRY: レースページに移動
            try:
                page.goto(race_url, timeout=60000)
                page.wait_for_selector("table.Shutuba_Table tbody tr.HorseList", timeout=10000)
            except Exception as e:
                print(f"[ERROR] ページ移動失敗: {e}")
                log_failed_url(race_url)
                return  # 処理を終了

            page.wait_for_timeout(3000)

            official_time_elem = page.query_selector("#official_time")
            official_time = official_time_elem.inner_text().strip() if official_time_elem else ""
            print(f"初回オッズ更新時刻: {official_time}")

            button = page.query_selector("#act-manual_update")
            if button:
                style = button.get_attribute("style") or ""
                if "display:none" in style:
                    print("更新ボタンはあるけど非表示（レース後かも）")
                else:
                    print("強制的にボタンのdisabledを外してクリックします...")
                    page.evaluate("""
                        const btn = document.querySelector('#act-manual_update');
                        if (btn) {
                            btn.disabled = false;
                            btn.click();
                        }
                    """)
                    time.sleep(5)
            else:
                print("更新ボタンがそもそも存在しない")

            time.sleep(5)

            updated_official_time = page.query_selector("#official_time")
            updated_time = updated_official_time.inner_text().strip() if updated_official_time else ""
            print(f"更新後オッズ更新時刻: {updated_time}")

            rows = page.query_selector_all("table.Shutuba_Table tbody tr.HorseList")
            print(f"取得した行数: {len(rows)}")

            for i, row in enumerate(rows):
                cells = row.query_selector_all("td")
                waku = get_inner_text_or_none(cells[0]) if len(cells) > 0 else ""
                umaban = get_inner_text_or_none(cells[1]) if len(cells) > 1 else ""

                horse_link_elem = row.query_selector("td.HorseInfo span.HorseName a")
                horse_name = get_inner_text_or_none(horse_link_elem)
                horse_href = horse_link_elem.get_attribute("href") if horse_link_elem else ""
                horse_id = horse_href.rstrip('/').split('/')[-1] if horse_href else ""

                seirei = get_inner_text_or_none(cells[3]) if len(cells) > 3 else ""
                kinryo = get_inner_text_or_none(cells[4]) if len(cells) > 4 else ""
                kisyu = get_inner_text_or_none(cells[5]) if len(cells) > 5 else ""
                odds = get_inner_text_or_none(row.query_selector("td.Txt_R.Popular span"))
                ninki = get_inner_text_or_none(row.query_selector("td.Popular"))

                print(f"枠:{waku}, 馬番:{umaban}, 馬名:{horse_name}, horse_id:{horse_id}, 性齢:{seirei}, 斤量:{kinryo}, 騎手:{kisyu}, オッズ:{odds}, 人気:{ninki}")

        finally:
            browser.close()
            duration = time.time() - start_time
            print(f"処理時間: {duration:.2f} 秒")

if __name__ == "__main__":
    main()
